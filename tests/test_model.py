import joblib

print("Loading model...")

model = joblib.load("model/final_model.pkl")

print("✅ Model Loaded Successfully!")
print(type(model))
