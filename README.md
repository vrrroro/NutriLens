# 🥗 NutriLens — Nutrition Intake Risk Estimator

> **Probability-Driven Deficiency Modeling & Real-Time Diet Tracking**

---

## 📌 Overview

NutriLens is a web-based nutrition risk estimator that goes beyond raw nutrient counting. Instead of simply telling you *how much* of a nutrient you consumed, NutriLens answers the clinically meaningful question:

> **"Given the amount I've consumed, what is the mathematical probability that I am deficient in this nutrient?"**

It uses statistical principles from nutritional epidemiology — **Normal Distribution**, **Z-Score calculations**, and the **Cumulative Distribution Function (CDF)** — to compare a user's recorded intake against established RDA (Recommended Daily Allowance) standards and produce a personalised deficiency risk score.

---

## 🚨 The Problem

Traditional nutrition apps report raw totals (e.g., *"You consumed 42 g of protein"*), but provide no statistical context. A simple binary check against the RDA (above = safe, below = deficient) ignores the probabilistic nature of nutrient requirements:

- Someone consuming 90% of the iron RDA is not just *"10% short"* — they occupy a specific position on the population's probability distribution.
- The most common deficiencies worldwide — **Iron, Vitamin D, Calcium, Zinc, and Magnesium** — lead to conditions like anemia, bone fragility, weakened immunity, and metabolic disorders, most of which are preventable with actionable dietary knowledge.

---

## 🧠 Statistical Methodology

NutriLens applies three interrelated statistical concepts:

### 1. Normal Distribution (Gaussian Model)
Each nutrient's population requirement is modelled as a bell curve where:
- **μ (mean)** = the RDA for that nutrient
- **σ (std. dev.)** = 15% of the RDA *(consistent with nutritional epidemiology literature)*

### 2. Z-Score Calculation
The user's observed intake `x` is standardised:

```
Z = (x − μ) / σ
```

A negative Z-score means intake is below the population mean; positive means above-average.

### 3. Cumulative Distribution Function (CDF)
The Z-score is fed into the CDF of the standard normal distribution:

```
P(Deficiency) = CDF(−Z) = 1 − CDF(Z)
```

This yields the **Probability of Deficiency** — the proportion of the population whose nutritional requirements exceed the user's intake.

### Risk Classification

| Deficiency Probability | Risk Level   |
|------------------------|--------------|
| < 30%                  | 🟢 LOW       |
| 30% – 60%              | 🟡 MODERATE  |
| > 60%                  | 🔴 HIGH      |

---

## ⚙️ Technology Stack

| Technology     | Role in NutriLens                                                                 |
|----------------|-----------------------------------------------------------------------------------|
| **Python 3.x** | Core programming language; business logic and server-side computation             |
| **Flask**      | Lightweight web framework; routing, template rendering, and request handling      |
| **NumPy**      | Efficient numerical array operations and distribution plotting support            |
| **SciPy**      | Provides `scipy.stats.norm.cdf()` — the primary deficiency probability function  |
| **Matplotlib** | Backend generation of Normal Distribution PDF charts, Base64-encoded             |
| **Jinja2**     | Flask's templating engine; renders dynamic HTML result pages                      |
| **Chart.js**   | Client-side interactive Bar and Radar chart visualisations in the browser         |

---

## 🏗️ System Architecture

NutriLens uses an **MVC (Model-View-Controller)** architecture:

```
Browser (JSON payload)
        │
        ▼
  Flask Controller (app.py)
  ├── JSON Deserialisation
  ├── Nutrient Aggregation
  ├── Dynamic RDA Adjustment (by gender)
  ├── Z-Score & CDF Computation (SciPy)
  ├── Risk Classification
  └── Matplotlib Chart Generation
        │
        ▼
  Jinja2 Template Rendering
        │
        ▼
  Browser Dashboard (Chart.js visualisations)
```

| Tier           | File                   | Responsibility                                                                 |
|----------------|------------------------|--------------------------------------------------------------------------------|
| **Model**      | `nutrition_db.py`      | RDA values, nutrient metadata, FOOD_DB (24 foods), risk thresholds             |
| **Controller** | `app.py`               | HTTP request handling, statistical computation, chart generation               |
| **View**       | `index.html` / `results.html` | User input forms, Chart.js visualisation scripts, results dashboard   |

---

## 🖥️ Application Features

### Step 1 — Biological Profile
Users select their biological sex, which dynamically adjusts the Calorie RDA baseline:
- **Male:** 2,500 kcal
- **Female:** 2,000 kcal

### Step 2 — Interactive Meal Tracker
Users build their daily meals by:
- Selecting a meal category (Breakfast / Lunch / Dinner / Snacks)
- Choosing from **24 Indian and international foods** via dropdown
- Specifying quantity in grams or millilitres
- Adding items as visual cards to the tracker

A **Quick Fill Demo** button pre-populates a realistic Indian meal plan (Dosa, Milk, Rice, Paneer, etc.) that yields ~50% moderate overall risk — ideal for exploring the full analysis pipeline.

### Tracked Nutrients
`Protein` · `Iron` · `Calcium` · `Vitamin C` · `Magnesium` · `Zinc` · `Vitamin D` · `Carbohydrates` · `Fat` · `Calories`

---

## 📊 Visualisations

### Backend — Matplotlib (Static Charts)
Generated server-side, Base64-encoded, and embedded directly in HTML:

- **Combined PDF Chart:** Overlapping probability density curves for all tracked nutrients on one grid, with a vertical reference line at 100% RDA.
- **Comparison PDF Chart:** Focuses on Calories, Protein, and Vitamin D — plots 4 bell curves per nutrient (Low / Moderate / Optimal hypothetical users + the actual user in purple) for direct comparative context.

### Frontend — Chart.js (Interactive)
- **Bar Chart (Dual-Axis):** Actual intake as a % of RDA per nutrient; supports hover tooltips with real values.
- **Radar Chart:** Deficiency probability (%) of all nutrients on a spider-web grid for an at-a-glance risk profile shape.
- **Progress-Bar Risk Cards:** Per-nutrient cards with colour-coded severity bars and personalised dietary recommendations for MODERATE/HIGH risk nutrients.

---

## 📁 Project Structure

```
nutrilens/
├── app.py                  # Flask controller — routing, computation, chart generation
├── nutrition_db.py         # Model — RDA values, FOOD_DB, risk thresholds
├── templates/
│   ├── index.html          # Meal tracker input interface
│   └── results.html        # Analysis dashboard with Chart.js visualisations
└── README.md
```

---

## 🔮 Future Improvements

- **Expanded Food Database** — Scale from 24 to hundreds of items, including user-defined custom foods.
- **Age & Health Condition Profiling** — Differentiated RDA values for subpopulations (age groups, pregnancy, health conditions) per ICMR and IOM guidelines.
- **Longitudinal Tracking** — Backend database (SQLite / PostgreSQL) with user authentication for multi-day meal history and trend analysis.
- **Clinical Validation** — Compare probabilistic outputs against validated dietary assessment methods (24-hour Recall Studies, Food Frequency Questionnaires).
- **Mobile App** — Progressive Web Application (PWA) or native mobile app for improved real-world accessibility.

---


## ⚠️ Disclaimer

NutriLens is an academic project and a principled statistical approximation. It is **not a clinically verified diagnostic tool** and should not replace professional medical or dietary advice. The Normal Distribution model with a 15% coefficient of variation is consistent with nutritional epidemiology literature and produces qualitatively valid risk estimates, but results are for educational and exploratory purposes only.

---

*Confidential — For Academic Submission Only | April 2026*
