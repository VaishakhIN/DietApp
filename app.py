from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# ---------------- LOAD DATASET ----------------
food_df = pd.read_csv("DietplanAPP/fooddataset.csv")

# Clean column names
food_df.columns = (
    food_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

# Ensure required columns exist
required_columns = ["dish_name", "meal_type", "diet", "calories", "protein", "fat", "carbohydrate"]
missing = [col for col in required_columns if col not in food_df.columns]
if missing:
    raise RuntimeError("Dataset missing required columns: " + ", ".join(missing))

# Convert to numeric
for col in ["calories", "protein", "fat", "carbohydrate"]:
    food_df[col] = pd.to_numeric(food_df[col], errors="coerce").fillna(0)

# ---------------- TRAIN ML MODEL ----------------
data = []
for i in range(1000):
    height = np.random.randint(150, 190)
    weight = np.random.randint(40, 100)
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        diet = "High-Calorie"
    elif bmi < 25:
        diet = "Normal"
    else:
        diet = "Low-Calorie"
    data.append([height, weight, bmi, diet])

user_df = pd.DataFrame(data, columns=["Height", "Weight", "BMI", "Diet_Label"])

X = user_df[["Height", "Weight", "BMI"]]
y = user_df["Diet_Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    meal_plan = {}
    bmi = 0
    predicted_diet = None
    target_calories = 0
    total_calories = 0

    if request.method == "POST":
        try:
            height = float(request.form.get("height"))
            weight = float(request.form.get("weight"))
            goal = request.form.get("goal")
            pref = request.form.get("preference")

            # BMI calculation
            bmi = weight / ((height / 100) ** 2)
            predicted_diet = model.predict([[height, weight, bmi]])[0]

            # Target calories
            if goal == "gain":
                target_calories = 2200
            elif goal == "lose":
                target_calories = 1500
            else:
                target_calories = 1800

            # Filter based on veg/non-veg
            available_meals = food_df[
                food_df["diet"].str.contains(pref, case=False, na=False)
            ]

            # Meals including snack2
            meals = ["breakfast", "snack1", "lunch", "snack2", "dinner"]

            for meal in meals:
                options = available_meals[available_meals["meal_type"].str.lower() == meal.lower()]
                if not options.empty:
                    meal_items = options.sample(n=min(2, len(options)), replace=False)
                    meal_plan[meal] = meal_items.to_dict(orient="records")

            total_calories = sum(
                sum(item["calories"] for item in items) for items in meal_plan.values()
            )

        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template(
        "index.html",
        bmi=round(bmi, 2),
        predicted_diet=predicted_diet,
        target_calories=target_calories,
        total_calories=round(total_calories, 2),
        meal_plan=meal_plan,
    )


if __name__ == "__main__":
    app.run(debug=True)
