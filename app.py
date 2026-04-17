from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib
import json
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm
import io
import base64
from data.nutrition_db import NUTRIENTS, RISK_THRESHOLDS, FOOD_SUGGESTIONS, FOOD_DB

app = Flask(__name__)


def calculate_deficiency_probability(intake_value, rda_value):
    mean = intake_value
    std_dev = rda_value * 0.15
    if std_dev == 0:
        return 0.0 if intake_value >= rda_value else 100.0
    z_score = (rda_value - mean) / std_dev
    probability = norm.cdf(z_score)
    return round(probability * 100, 2)


def classify_risk(probability):
    if probability < RISK_THRESHOLDS["LOW"]["max"]:
        return "LOW"
    elif probability < RISK_THRESHOLDS["MODERATE"]["max"]:
        return "MODERATE"
    else:
        return "HIGH"


def generate_comparison_plot(nutrient_name, user_intake, rda_value, unit):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0a0f19")
    ax.set_facecolor("#0a0f19")
    
    STD_norm = 15
    RDA_norm = 100
    x = np.linspace(0, 200, 500)
    
    base_users = [
        {"name": "User A (Low)", "mu": 60, "color": "red"},
        {"name": "User B (Moderate)", "mu": 85, "color": "orange"},
        {"name": "User C (Optimal)", "mu": 115, "color": "green"},
    ]
    
    user_mu = (user_intake / rda_value) * 100 if rda_value > 0 else 0
    user_prob = calculate_deficiency_probability(user_intake, rda_value) / 100

    hypothetical_users = []
    for user in base_users:
        z_score = (RDA_norm - user["mu"]) / STD_norm
        prob = norm.cdf(z_score)
        hypothetical_users.append({
            "label": f"{user['name']} (risk={prob:.0%})",
            "mu": user["mu"],
            "color": user["color"]
        })
    
    hypothetical_users.append({
        "label": f"You ({round(user_intake,1)}{unit}, risk={user_prob:.0%})",
        "mu": user_mu,
        "color": "purple"
    })
    
    for user in hypothetical_users:
        y = norm.pdf(x, user["mu"], STD_norm)
        ax.plot(x, y, color=user["color"], lw=2.5, label=user["label"])
        ax.fill_between(x, y, where=x < RDA_norm, color=user["color"], alpha=0.1)
        
    ax.axvline(RDA_norm, color="#e0f2fe", lw=2.5, linestyle="--", label="RDA = 100%")
    ax.set_xlabel("Daily Intake (% of RDA)", fontsize=13, color="#e0f2fe")
    ax.set_ylabel("Probability Density", fontsize=13, color="#e0f2fe")
    ax.set_title(f"{nutrient_name} Comparison — Different Users\nShaded area (left of RDA) = Deficiency Risk", fontsize=13, fontweight="bold", color="#e0f2fe")
    ax.tick_params(colors="#e0f2fe")
    
    legend = ax.legend(fontsize=10, framealpha=0.9, loc="center left", bbox_to_anchor=(1, 0.5))
    legend.get_frame().set_facecolor("#141c2d")
    legend.get_frame().set_edgecolor("#00ffcc")
    for text in legend.get_texts():
        text.set_color("#e0f2fe")
        
    ax.grid(alpha=0.2, color="#e0f2fe")
    
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format="png", dpi=150, bbox_inches="tight")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    return plot_url


@app.route("/")
def home():
    # Pass FOOD_DB down to render initial available foods
    return render_template("index.html", food_db=FOOD_DB)


@app.route("/analyze", methods=["POST"])
def analyze():
    payload_str = request.form.get("payload")
    try:
        data = json.loads(payload_str)
    except:
        data = {"gender": "Female", "foods": []}

    gender = data.get("gender", "Female")
    foods = data.get("foods", [])

    if gender == "Male":
        NUTRIENTS["Calories"]["rda"] = 2500
    else:
        NUTRIENTS["Calories"]["rda"] = 2000

    totals = {k: 0.0 for k in NUTRIENTS.keys()}
    
    for f in foods:
        food_name = f.get("name")
        weight = float(f.get("weight", 0))
        # if ml toggle was used, practically for given DB foods like milk it's ~1g/ml. We just treat weight as grams equivalent.
        if food_name in FOOD_DB:
            for nutrient, val_per_100 in FOOD_DB[food_name].items():
                if nutrient in totals:
                    totals[nutrient] += val_per_100 * (weight / 100.0)

    results = []
    total_probability = 0
    errors = []

    for nutrient_name, info in NUTRIENTS.items():
        intake = totals[nutrient_name]
        rda = info["rda"]
        probability = calculate_deficiency_probability(intake, rda)
        risk_level = classify_risk(probability)
        intake_pct = min(round(intake / rda * 100, 1), 100) if rda > 0 else 0
        
        result_entry = {
            "name": nutrient_name,
            "icon": info["icon"],
            "intake": round(intake, 2),
            "rda": rda,
            "unit": info["unit"],
            "probability": probability,
            "risk_level": risk_level,
            "risk_color": RISK_THRESHOLDS[risk_level]["color"],
            "message": RISK_THRESHOLDS[risk_level]["message"],
            "description": info["description"],
            "intake_pct": intake_pct,
            "suggestions": FOOD_SUGGESTIONS.get(nutrient_name, []),
        }
        results.append(result_entry)
        total_probability += probability

    overall_score = round(total_probability / len(results), 1) if results else 0
    overall_risk = classify_risk(overall_score)
    risk_counts = {"HIGH": 0, "MODERATE": 0, "LOW": 0}
    for r in results:
        risk_counts[r["risk_level"]] += 1

    insights = []
    for r in results:
        if r["risk_level"] == "HIGH":
            food_list = ", ".join(r["suggestions"][:3])
            insights.append({
                "text": f"Your {r['name']} intake is critically low — consider adding {food_list}",
                "level": "HIGH",
                "color": RISK_THRESHOLDS["HIGH"]["color"],
                "icon": "⚠️",
            })
        elif r["risk_level"] == "MODERATE":
            food_list = ", ".join(r["suggestions"][:2])
            insights.append({
                "text": f"Your {r['name']} could use a boost — try {food_list}",
                "level": "MODERATE",
                "color": RISK_THRESHOLDS["MODERATE"]["color"],
                "icon": "🔔",
            })

    # Add insight for LOW risk broadly
    if risk_counts["HIGH"] == 0 and risk_counts["MODERATE"] == 0:
        insights.append({
            "text": f"Your overall levels look great — keep it up!",
            "level": "LOW",
            "color": RISK_THRESHOLDS["LOW"]["color"],
            "icon": "✅",
        })

    # Combined PDF Graph
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0a0f19")
    ax.set_facecolor("#0a0f19")
    colors = ["red", "blue", "green", "orange", "purple", "cyan", "magenta", "brown", "darkkhaki", "teal", "navy"]
    x = np.linspace(0, 200, 500)
    RDA_norm = 100
    STD_norm = 15
    for idx, r in enumerate(results):
        if r["rda"] > 0:
            color = colors[idx % len(colors)]
            mu = r["intake"] / r["rda"] * 100
            y = norm.pdf(x, mu, STD_norm)
            prob = r["probability"] / 100
            ax.plot(x, y, color=color, lw=2.5, label=f"{r['name']} (risk={prob:.0%})")
            ax.fill_between(x, y, where=x < RDA_norm, color=color, alpha=0.1)
            
    ax.axvline(RDA_norm, color="#e0f2fe", lw=2.5, linestyle="--", label="RDA = 100%")
    ax.set_xlabel("Daily Intake (% of RDA)", fontsize=13, color="#e0f2fe")
    ax.set_ylabel("Probability Density", fontsize=13, color="#e0f2fe")
    ax.set_title("Probability Density Function — ALL Nutrients\nShaded area (left of RDA) = Probability of Deficiency", fontsize=13, fontweight="bold", color="#e0f2fe")
    ax.tick_params(colors="#e0f2fe")
    
    # Place legend outside
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
    legend = ax.legend(fontsize=9, framealpha=0.9, loc="center left", bbox_to_anchor=(1, 0.5))
    legend.get_frame().set_facecolor("#141c2d")
    legend.get_frame().set_edgecolor("#00ffcc")
    for text in legend.get_texts():
        text.set_color("#e0f2fe")
        
    ax.grid(alpha=0.2, color="#e0f2fe")
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format="png", dpi=150, bbox_inches="tight")
    img.seek(0)
    combined_plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)

    # Comparison Plots
    comparison_plots = {}
    for nutrient in ["Calories", "Protein", "Vitamin D"]:
        res = next((r for r in results if r["name"] == nutrient), None)
        if res and res["rda"] > 0:
            comparison_plots[nutrient] = generate_comparison_plot(nutrient, res["intake"], res["rda"], res["unit"])

    return render_template(
        "results.html",
        results=results,
        overall_score=overall_score,
        overall_risk=overall_risk,
        overall_color=RISK_THRESHOLDS[overall_risk]["color"],
        risk_counts=risk_counts,
        insights=insights,
        errors=errors,
        combined_plot_url=combined_plot_url,
        comparison_plots=comparison_plots,
    )


@app.route("/api/foods")
def api_foods():
    return jsonify({"foods": FOOD_DB})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
