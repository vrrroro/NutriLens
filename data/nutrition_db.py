# ============================================================
# nutrition_db.py — The Nutrient Database
# ============================================================
#
# WHAT IS THIS FILE?
# This is a Python "module" — a .py file that holds data and
# functions other files can import and use. Think of it as a
# reference book that app.py will look up whenever it needs
# nutrient information.
#
# WHY A SEPARATE FILE?
# "Separation of concerns" — we keep data in one place and
# logic in another. If the RDA values ever change (e.g., a
# new WHO guideline), we only edit THIS file, not the whole app.
#
# WHAT IS A PYTHON DICTIONARY?
# A dictionary ({}) stores data as key-value pairs:
#   {"name": "Iron", "rda": 18}
# You look things up by key, just like a real dictionary.
# Here we use "nested" dicts — a dict inside another dict —
# to group related info for each nutrient.
# ============================================================

# ----- RDA = Recommended Daily Allowance -----
# These are standard adult values from WHO / NIH guidelines.
# Each nutrient entry contains:
#   rda         → how much you should consume daily
#   unit        → measurement unit (g = grams, mg = milligrams, mcg = micrograms)
#   icon        → emoji for the UI
#   description → short health role explanation

NUTRIENTS = {
    "Protein": {
        "rda": 50,
        "unit": "g",
        "icon": "🥩",
        "description": "Essential for muscle repair and immune function"
    },
    "Iron": {
        "rda": 18,
        "unit": "mg",
        "icon": "🩸",
        "description": "Carries oxygen in red blood cells"
    },
    "Calcium": {
        "rda": 1000,
        "unit": "mg",
        "icon": "🦴",
        "description": "Builds strong bones and teeth"
    },
    "Vitamin C": {
        "rda": 90,
        "unit": "mg",
        "icon": "🍊",
        "description": "Antioxidant, boosts immunity"
    },
    "Magnesium": {
        "rda": 400,
        "unit": "mg",
        "icon": "💪",
        "description": "Supports nerve and muscle function"
    },
    "Zinc": {
        "rda": 11,
        "unit": "mg",
        "icon": "⚡",
        "description": "Immune defense and wound healing"
    },
    "Vitamin D": {
        "rda": 20,
        "unit": "mcg",
        "icon": "☀️",
        "description": "Bone health and immune regulation"
    },
    "Vitamin B12": {
        "rda": 2.4,
        "unit": "mcg",
        "icon": "🧠",
        "description": "Nerve function and red blood cell formation"
    }
}

# ----- Risk Thresholds -----
# After we compute a deficiency probability (0–100%), we
# classify it into one of three "risk levels."
# Each level has a max boundary, a display color, and a message.

RISK_THRESHOLDS = {
    "LOW": {
        "max": 30,
        "color": "#7ec832",
        "message": "Your intake looks good! Maintain your current diet."
    },
    "MODERATE": {
        "max": 60,
        "color": "#f0a500",
        "message": "Consider adding more of this nutrient to your diet."
    },
    "HIGH": {
        "max": 100,
        "color": "#f85149",
        "message": "Significant deficiency risk. Consult a healthcare provider."
    }
}


FOOD_SUGGESTIONS = {
    "Protein":     ["Chicken breast", "Greek yogurt", "Eggs", "Cottage cheese"],
    "Iron":        ["Spinach", "Lentils", "Red meat", "Tofu"],
    "Calcium":     ["Milk", "Yogurt", "Broccoli", "Almonds"],
    "Vitamin C":   ["Oranges", "Bell peppers", "Strawberries", "Kiwi"],
    "Magnesium":   ["Pumpkin seeds", "Dark chocolate", "Avocado", "Bananas"],
    "Zinc":        ["Oysters", "Beef", "Chickpeas", "Cashews"],
    "Vitamin D":   ["Salmon", "Egg yolks", "Fortified milk", "Sunlight ☀️"],
    "Vitamin B12": ["Clams", "Beef liver", "Fortified cereal", "Nutritional yeast"]
}
