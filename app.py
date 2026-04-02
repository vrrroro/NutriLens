from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.stats import norm
from data.nutrition_db import NUTRIENTS, RISK_THRESHOLDS, FOOD_SUGGESTIONS
app = Flask(__name__)

def calculate_deficiency_probability(intake_value, rda_value):
    mean = intake_value
    std_dev = rda_value * 0.15
    if std_dev == 0:
        return 0.0 if intake_value >= rda_value else 100.0
    probability = norm.cdf(rda_value, loc=mean, scale=std_dev)
    return round(probability * 100, 2)

def classify_risk(probability):
    if probability < RISK_THRESHOLDS['LOW']['max']:
        return 'LOW'
    elif probability < RISK_THRESHOLDS['MODERATE']['max']:
        return 'MODERATE'
    else:
        return 'HIGH'

@app.route('/')
def home():
    return render_template('index.html', nutrients=NUTRIENTS)

@app.route('/analyze', methods=['POST'])
def analyze():
    results = []
    errors = []
    total_probability = 0
    field_map = {'protein': 'Protein', 'iron': 'Iron', 'calcium': 'Calcium', 'vitamin_c': 'Vitamin C', 'magnesium': 'Magnesium', 'zinc': 'Zinc', 'vitamin_d': 'Vitamin D', 'vitamin_b12': 'Vitamin B12'}
    for field_name, nutrient_name in field_map.items():
        raw_value = request.form.get(field_name, '')
        try:
            intake = float(raw_value)
            if intake < 0:
                errors.append(f'{nutrient_name}: value cannot be negative.')
                intake = 0.0
        except (ValueError, TypeError):
            errors.append(f'{nutrient_name}: invalid input — using 0.')
            intake = 0.0
        info = NUTRIENTS[nutrient_name]
        rda = info['rda']
        probability = calculate_deficiency_probability(intake, rda)
        risk_level = classify_risk(probability)
        intake_pct = min(round(intake / rda * 100, 1), 100) if rda > 0 else 0
        result_entry = {'name': nutrient_name, 'icon': info['icon'], 'intake': round(intake, 2), 'rda': rda, 'unit': info['unit'], 'probability': probability, 'risk_level': risk_level, 'risk_color': RISK_THRESHOLDS[risk_level]['color'], 'message': RISK_THRESHOLDS[risk_level]['message'], 'description': info['description'], 'intake_pct': intake_pct, 'suggestions': FOOD_SUGGESTIONS.get(nutrient_name, [])}
        results.append(result_entry)
        total_probability += probability
    overall_score = round(total_probability / len(results), 1) if results else 0
    overall_risk = classify_risk(overall_score)
    risk_counts = {'HIGH': 0, 'MODERATE': 0, 'LOW': 0}
    for r in results:
        risk_counts[r['risk_level']] += 1
    insights = []
    for r in results:
        if r['risk_level'] == 'HIGH':
            food_list = ', '.join(r['suggestions'][:3])
            insights.append({'text': f"Your {r['name']} intake is critically low — consider adding {food_list}", 'level': 'HIGH', 'color': RISK_THRESHOLDS['HIGH']['color'], 'icon': '⚠️'})
        elif r['risk_level'] == 'MODERATE':
            food_list = ', '.join(r['suggestions'][:2])
            insights.append({'text': f"Your {r['name']} could use a boost — try {food_list}", 'level': 'MODERATE', 'color': RISK_THRESHOLDS['MODERATE']['color'], 'icon': '🔔'})
        else:
            insights.append({'text': f"Your {r['name']} levels look great — keep it up!", 'level': 'LOW', 'color': RISK_THRESHOLDS['LOW']['color'], 'icon': '✅'})
    return render_template('results.html', results=results, overall_score=overall_score, overall_risk=overall_risk, overall_color=RISK_THRESHOLDS[overall_risk]['color'], risk_counts=risk_counts, insights=insights, errors=errors)

@app.route('/api/analyze')
def api_analyze():
    results = []
    for nutrient_name, info in NUTRIENTS.items():
        field_name = nutrient_name.lower().replace(' ', '_')
        raw_value = request.args.get(field_name, '0')
        try:
            intake = max(float(raw_value), 0)
        except (ValueError, TypeError):
            intake = 0.0
        rda = info['rda']
        probability = calculate_deficiency_probability(intake, rda)
        risk_level = classify_risk(probability)
        results.append({'nutrient': nutrient_name, 'intake': intake, 'rda': rda, 'unit': info['unit'], 'probability': probability, 'risk_level': risk_level})
    return jsonify({'results': results})
if __name__ == '__main__':
    app.run(debug=True, port=5000)