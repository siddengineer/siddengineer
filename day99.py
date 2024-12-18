import matplotlib.pyplot as plt

# Waste segregation and recommendation logic
def categorize_waste(waste_type):
    organic = ["vegetable peels", "fruit scraps", "food leftovers", "garden waste"]
    recyclable = ["plastic", "paper", "metal", "glass"]
    hazardous = ["batteries", "chemicals", "electronics"]

    if waste_type.lower() in organic:
        return "Organic"
    elif waste_type.lower() in recyclable:
        return "Recyclable"
    elif waste_type.lower() in hazardous:
        return "Hazardous"
    else:
        return "Unknown"

def calculate_biogas(weight):
    return weight * 50  # 50 liters per kg

def recommend_disposal(category):
    if category == "Organic":
        return "Use for composting or biogas production."
    elif category == "Recyclable":
        return "Take to the nearest recycling center."
    elif category == "Hazardous":
        return "Dispose of at a hazardous waste collection facility."
    else:
        return "Cannot identify waste category."

# Input data
waste_data = {
    "Vegetable Peels": 5,
    "Plastic": 2,
    "Batteries": 1
}

# Process data
categories = {"Organic": 0, "Recyclable": 0, "Hazardous": 0}
for waste, weight in waste_data.items():
    category = categorize_waste(waste)
    categories[category] += weight

# Output results
print("Waste Categorization and Recommendations:")
for waste, weight in waste_data.items():
    category = categorize_waste(waste)
    recommendation = recommend_disposal(category)
    print(f"- {waste} ({weight} kg): {category} - {recommendation}")

# Visualization
plt.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", colors=["green", "blue", "red"])
plt.title("Waste Distribution")
plt.show()
