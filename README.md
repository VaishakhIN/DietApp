# DietApp
It is an ML based diet prediction model with Web Design
A simple Flask + Machine Learning app that generates a personalized diet plan based on:

Height & Weight (BMI)

Goal: Gain / Lose / Maintain

Food Preference: Veg / Non-Veg

🚀 Features

Predicts diet type using BMI

Generates meal plan: Breakfast, Snack1, Lunch, Snack2, Dinner

Shows calories, protein, fat, carbs for each dish

Works with your own dataset (fooddataset.csv)

📂 Project Files
DietplanAPP/
│── app.py            # Flask backend
│── tempcoderunner.py # ML model testing
│── templates/
│    └── index.html   # Frontend page
│── fooddataset.csv   # Dataset
│── README.md         # Project docs

⚡ Setup

Clone the repo

Install requirements

pip install flask pandas scikit-learn

📊 Dataset Format

Your CSV file must have:

dish_name,meal_type,diet,calories,protein,fat,carbohydrate

✅ Example Output
BMI: 26.5
Goal: Lose
Predicted Diet: Low-Calorie
Target Calories: 1500 kcal
Meal Plan: Breakfast, Lunch, Snacks, Dinner with nutrition details
