import numpy as np

# Recommended Daily Intake (RDA) values
rda = {
    "Protein": 50,       # grams
    "Iron": 18,          # mg
    "Calcium": 1000,     # mg
    "Vitamin C": 90,     # mg
    "Magnesium": 400,    # mg
    "Zinc": 11,          # mg
    "Vitamin D": 20,     # mcg
    "Vitamin B12": 2.4   # mcg
}

# User input for daily nutrient intake
protein = float(input("Enter protein intake (g): "))
iron = float(input("Enter iron intake (mg): "))
calcium = float(input("Enter calcium intake (mg): "))
vitamin_c = float(input("Enter vitamin C intake (mg): "))
magnesium = float(input("Enter magnesium intake (mg): "))
zinc = float(input("Enter zinc intake (mg): "))
vitamin_d = float(input("Enter vitamin D intake (mcg): "))
vitamin_b12 = float(input("Enter vitamin B12 intake (mcg): "))

# Store user intake values
intake = {
    "Protein": protein,
    "Iron": iron,
    "Calcium": calcium,
    "Vitamin C": vitamin_c,
    "Magnesium": magnesium,
    "Zinc": zinc,
    "Vitamin D": vitamin_d,
    "Vitamin B12": vitamin_b12
}

print("\nNutritional Deficiency Analysis:\n")

# Calculate deficiency probability
for nutrient in rda:
    deficiency = (rda[nutrient] - intake[nutrient]) / rda[nutrient]
    
    deficiency = max(deficiency, 0)

    probability = deficiency * 100

    if probability < 30:
        risk = "LOW"
    elif probability < 60:
        risk = "MODERATE"
    else:
        risk = "HIGH"

    print(nutrient)
    print("Deficiency probability:", round(probability,2), "%")
    print("Risk level:", risk)
    print()