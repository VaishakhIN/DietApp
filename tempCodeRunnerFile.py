import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
food_df = pd.read_csv("DietplanAPP/fooddataset.csv")

# Clean column names
food_df.columns = (
    food_df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

# Ensure numeric
for col in ["calories", "protein", "fat", "carbohydrate"]:
    food_df[col] = pd.to_numeric(food_df[col], errors="coerce").fillna(0)

# Train classifier
data = []
for i in range(1000):
    h = np.random.randint(150, 190)
    w = np.random.randint(40, 100)
    bmi = w / ((h / 100) ** 2)
    if bmi < 18.5:
        d = "High-Calorie"
    elif bmi < 25:
        d = "Normal"
    else:
        d = "Low-Calorie"
    data.append([h, w, bmi, d])

df = pd.DataFrame(data, columns=["Height", "Weight", "BMI", "Diet_Label"])
X = df[["Height", "Weight", "BMI"]]
y = df["Diet_Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

print("ML Model trained successfully ✅")

# Example test
height = 170
weight = 80
bmi = weight / ((height / 100) ** 2)
predicted_diet = model.predict([[height, weight, bmi]])[0]

goal = "lose"
if goal == "gain":
    target_calories = 2200
elif goal == "lose":
    target_calories = 1500
else:
    target_calories = 1800

print(f"\nBMI: {bmi:.2f}, Predicted Diet: {predicted_diet}, Goal: {goal}")
print(f"Target Total Calories: {target_calories} kcal\n")

meal_plan = {}
meals = ["breakfast", "snack1", "lunch", "snack2", "dinner"]

available_meals = food_df[food_df["diet"].str.contains("Veg", case=False, na=False)]

total_calories = 0
for meal in meals:
    options = available_meals[available_meals["meal_type"].str.lower() == meal.lower()]
    if not options.empty:
        items = options.sample(n=min(2, len(options)), replace=False)
        meal_plan[meal] = items
        print(f"\n{meal.capitalize()}:")
        for _, row in items.iterrows():
            print(f" - {row['dish_name']} ({row['calories']} kcal)")
            total_calories += row["calories"]

print(f"\nTotal Calories Planned: {total_calories:.2f} kcal")
