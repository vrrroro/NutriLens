NUTRIENTS = {
    "Calories": {
        "rda": 2000, # Base, will dynamically adjust for gender
        "unit": "kcal",
        "icon": "🔥",
        "description": "Energy provided by food",
    },
    "Protein": {
        "rda": 50,
        "unit": "g",
        "icon": "🥩",
        "description": "Essential for muscle repair and immune function",
    },
    "Carbs": {
        "rda": 275,
        "unit": "g",
        "icon": "🍞",
        "description": "Main source of energy for the body",
    },
    "Fat": {
        "rda": 78,
        "unit": "g",
        "icon": "🥑",
        "description": "Aids nutrient absorption and hormone production",
    },
    "Iron": {
        "rda": 18,
        "unit": "mg",
        "icon": "🩸",
        "description": "Carries oxygen in red blood cells",
    },
    "Calcium": {
        "rda": 1000,
        "unit": "mg",
        "icon": "🦴",
        "description": "Builds strong bones and teeth",
    },
    "Vitamin C": {
        "rda": 90,
        "unit": "mg",
        "icon": "🍊",
        "description": "Antioxidant, boosts immunity",
    },
    "Magnesium": {
        "rda": 400,
        "unit": "mg",
        "icon": "💪",
        "description": "Supports nerve and muscle function",
    },
    "Zinc": {
        "rda": 11,
        "unit": "mg",
        "icon": "⚡",
        "description": "Immune defense and wound healing",
    },
    "Vitamin D": {
        "rda": 800,  # 20 mcg = 800 IU
        "unit": "IU",
        "icon": "☀️",
        "description": "Bone health and immune regulation",
    },
}

RISK_THRESHOLDS = {
    "LOW": {
        "max": 30,
        "color": "#7ec832",
        "message": "Your intake looks good! Maintain your current diet.",
    },
    "MODERATE": {
        "max": 60,
        "color": "#f0a500",
        "message": "Consider adding more of this nutrient to your diet.",
    },
    "HIGH": {
        "max": 100,
        "color": "#f85149",
        "message": "Significant deficiency risk. Consult a healthcare provider.",
    },
}

FOOD_SUGGESTIONS = {
    "Calories": ["Nuts", "Avocado", "Olive oil", "Rice"],
    "Protein": ["Chicken breast", "Greek yogurt", "Eggs", "Cottage cheese"],
    "Carbs": ["Oats", "Sweet potatoes", "Brown rice", "Quinoa"],
    "Fat": ["Salmon", "Avocado", "Walnuts", "Chia seeds"],
    "Iron": ["Spinach", "Lentils", "Red meat", "Tofu"],
    "Calcium": ["Milk", "Yogurt", "Broccoli", "Almonds"],
    "Vitamin C": ["Oranges", "Bell peppers", "Strawberries", "Kiwi"],
    "Magnesium": ["Pumpkin seeds", "Dark chocolate", "Avocado", "Bananas"],
    "Zinc": ["Oysters", "Beef", "Chickpeas", "Cashews"],
    "Vitamin D": ["Salmon", "Egg yolks", "Fortified milk", "Sunlight ☀️"],
}

FOOD_DB = {
    "Idli": {"Protein": 7.0, "Carbs": 28, "Fat": 1.0, "Calories": 140, "Iron": 0.9, "Calcium": 10, "Vitamin C": 0, "Magnesium": 15, "Zinc": 0.5, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Dosa": {"Protein": 5.0, "Carbs": 28, "Fat": 3.0, "Calories": 168, "Iron": 2.1, "Calcium": 20, "Vitamin C": 0, "Magnesium": 20, "Zinc": 0.7, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Upma": {"Protein": 6.0, "Carbs": 26, "Fat": 5.0, "Calories": 170, "Iron": 1.5, "Calcium": 15, "Vitamin C": 2, "Magnesium": 25, "Zinc": 0.8, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Poha": {"Protein": 3.0, "Carbs": 28, "Fat": 2.0, "Calories": 130, "Iron": 1.2, "Calcium": 10, "Vitamin C": 5, "Magnesium": 20, "Zinc": 0.6, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Paratha": {"Protein": 6.0, "Carbs": 30, "Fat": 10.0, "Calories": 260, "Iron": 2.5, "Calcium": 20, "Vitamin C": 0, "Magnesium": 25, "Zinc": 1.0, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Rice": {"Protein": 2.7, "Carbs": 28, "Fat": 0.3, "Calories": 130, "Iron": 0.2, "Calcium": 10, "Vitamin C": 0, "Magnesium": 12, "Zinc": 0.4, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Dal": {"Protein": 9.0, "Carbs": 20, "Fat": 1.0, "Calories": 116, "Iron": 3.0, "Calcium": 30, "Vitamin C": 2, "Magnesium": 40, "Zinc": 1.2, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Roti": {"Protein": 9.0, "Carbs": 45, "Fat": 3.0, "Calories": 290, "Iron": 2.7, "Calcium": 20, "Vitamin C": 0, "Magnesium": 40, "Zinc": 1.5, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Sabzi": {"Protein": 2.0, "Carbs": 10, "Fat": 5.0, "Calories": 90, "Iron": 1.5, "Calcium": 40, "Vitamin C": 15, "Magnesium": 30, "Zinc": 0.5, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Sambar": {"Protein": 4.0, "Carbs": 12, "Fat": 3.0, "Calories": 80, "Iron": 2.0, "Calcium": 40, "Vitamin C": 10, "Magnesium": 30, "Zinc": 0.8, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Khichdi": {"Protein": 6.0, "Carbs": 20, "Fat": 3.0, "Calories": 120, "Iron": 1.8, "Calcium": 20, "Vitamin C": 2, "Magnesium": 25, "Zinc": 0.7, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Curry": {"Protein": 5.0, "Carbs": 10, "Fat": 8.0, "Calories": 120, "Iron": 2.0, "Calcium": 30, "Vitamin C": 5, "Magnesium": 25, "Zinc": 1.0, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Chapati": {"Protein": 9.0, "Carbs": 45, "Fat": 3.0, "Calories": 290, "Iron": 2.7, "Calcium": 20, "Vitamin C": 0, "Magnesium": 40, "Zinc": 1.5, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Paneer": {"Protein": 18.0, "Carbs": 3, "Fat": 20.0, "Calories": 265, "Iron": 0.2, "Calcium": 200, "Vitamin C": 0, "Magnesium": 25, "Zinc": 2.0, "Vitamin D": 20, "Vitamin B12": 1.0},
    "Biryani": {"Protein": 8.0, "Carbs": 25, "Fat": 10.0, "Calories": 220, "Iron": 2.0, "Calcium": 30, "Vitamin C": 2, "Magnesium": 30, "Zinc": 1.2, "Vitamin D": 5, "Vitamin B12": 0.5},
    "Samosa": {"Protein": 6.0, "Carbs": 30, "Fat": 17.0, "Calories": 308, "Iron": 2.0, "Calcium": 20, "Vitamin C": 2, "Magnesium": 25, "Zinc": 1.0, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Pakora": {"Protein": 6.0, "Carbs": 20, "Fat": 15.0, "Calories": 270, "Iron": 2.5, "Calcium": 30, "Vitamin C": 5, "Magnesium": 30, "Zinc": 1.2, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Chutney": {"Protein": 2.0, "Carbs": 8, "Fat": 10.0, "Calories": 120, "Iron": 1.5, "Calcium": 40, "Vitamin C": 10, "Magnesium": 25, "Zinc": 0.8, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Biscuit": {"Protein": 6.0, "Carbs": 70, "Fat": 12.0, "Calories": 450, "Iron": 2.5, "Calcium": 30, "Vitamin C": 0, "Magnesium": 20, "Zinc": 0.7, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Namkeen": {"Protein": 8.0, "Carbs": 50, "Fat": 25.0, "Calories": 550, "Iron": 3.0, "Calcium": 40, "Vitamin C": 0, "Magnesium": 40, "Zinc": 1.5, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Milk": {"Protein": 3.4, "Carbs": 5, "Fat": 3.3, "Calories": 60, "Iron": 0.03, "Calcium": 120, "Vitamin C": 0, "Magnesium": 10, "Zinc": 0.4, "Vitamin D": 40, "Vitamin B12": 0.5},
    "Coffee": {"Protein": 0.1, "Carbs": 0, "Fat": 0.0, "Calories": 2, "Iron": 0.01, "Calcium": 2, "Vitamin C": 0, "Magnesium": 3, "Zinc": 0.02, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Tea": {"Protein": 0.0, "Carbs": 0, "Fat": 0.0, "Calories": 2, "Iron": 0.02, "Calcium": 3, "Vitamin C": 0, "Magnesium": 2, "Zinc": 0.02, "Vitamin D": 0, "Vitamin B12": 0.0},
    "Egg": {"Protein": 13.0, "Carbs": 1, "Fat": 11.0, "Calories": 155, "Iron": 1.8, "Calcium": 50, "Vitamin C": 0, "Magnesium": 10, "Zinc": 1.3, "Vitamin D": 80, "Vitamin B12": 1.1},
    "Chicken": {"Protein": 27.0, "Carbs": 0, "Fat": 14.0, "Calories": 239, "Iron": 1.3, "Calcium": 15, "Vitamin C": 0, "Magnesium": 25, "Zinc": 2.0, "Vitamin D": 10, "Vitamin B12": 0.3},
}
