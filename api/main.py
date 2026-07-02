from fastapi import FastAPI
from api.schemas import TicketRequest
import joblib
from pathlib import Path
import pandas as pd

from components.prediction import get_prediction_result
from components.recommendations import get_recommendations
from database.database import save_prediction
from database.database import get_all_predictions

app = FastAPI(
    title="ITMS Decision Support API",
    description="REST API for Intelligent IT Service Management Decision Support System",
    version="1.0.0"
)

# ==========================================================
# LOAD MODEL
# ==========================================================

model = joblib.load(
    Path("model") / "final_model.pkl"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to the ITMS Decision Support API!"
    }


@app.get("/health")
def health():
    return {
        "status": "running"
    }

@app.post("/predict")
def predict(ticket: TicketRequest):

    input_data = pd.DataFrame({

        "Priority": [ticket.Priority],
        "Category": [ticket.Category],
        "Sub Category": [ticket.Sub_Category],
        "Department": [ticket.Department],
        "Group": [ticket.Group],
        "Site": [ticket.Site],
        "Request Type": [ticket.Request_Type],
        "Created_Day": [ticket.Created_Day],
        "Created_Month": [ticket.Created_Month],
        "Created_Hour": [ticket.Created_Hour]

    })

    (
        prediction,
        probability,
        breach_probability,
        prediction_text,
        prediction_color,
        risk_level,
        risk_color

    ) = get_prediction_result(
        model,
        input_data
    )

    recommendations = get_recommendations(
        ticket.Priority,
        breach_probability
    )

    save_prediction(
        ticket.Priority,
        ticket.Category,
        ticket.Sub_Category,
        ticket.Department,
        ticket.Group,
        ticket.Site,
        ticket.Request_Type,
        ticket.Created_Day,
        ticket.Created_Month,
        ticket.Created_Hour,
        prediction,
        breach_probability,
        risk_level
    )

    return {

        "prediction": prediction_text,

        "breach_probability": round(
            breach_probability,
            2
        ),

        "risk_level": risk_level,

        "recommendations": recommendations

    }

@app.get("/history")
def get_history():

    records = get_all_predictions()

    columns = [
        "ID",
        "Timestamp",
        "Priority",
        "Category",
        "Sub Category",
        "Department",
        "Group",
        "Site",
        "Request Type",
        "Created Day",
        "Created Month",
        "Created Hour",
        "Prediction",
        "Probability",
        "Risk Level"
    ]

    history = []

    for record in records:

        item = dict(zip(columns, record))

        item["Prediction"] = (
            "Breach"
            if item["Prediction"] == 1
            else "No Breach"
        )

        item["Probability"] = (
            f"{item['Probability']:.2f}%"
        )

        history.append(item)

    return history

@app.get("/analytics")
def get_analytics():

    records = get_all_predictions()

    columns = [
        "ID",
        "Timestamp",
        "Priority",
        "Category",
        "Sub Category",
        "Department",
        "Group",
        "Site",
        "Request Type",
        "Created Day",
        "Created Month",
        "Created Hour",
        "Prediction",
        "Probability",
        "Risk Level"
    ]

    df = pd.DataFrame(
        records,
        columns=columns
    )

    # Convert predictions to readable text
    df["Prediction"] = df["Prediction"].map({
        0: "No Breach",
        1: "Breach"
    })

    # Total Predictions
    total_predictions = len(df)

    # Breach Rate
    breach_rate = (
        (df["Prediction"] == "Breach").mean() * 100
    )

    # High Risk Tickets
    high_risk_tickets = (
        df["Risk Level"] == "HIGH"
    ).sum()

    # Average Probability
    average_probability = (
        df["Probability"].mean()
    )

    return {

        "total_predictions": total_predictions,

        "breach_rate": round(
            float(breach_rate),
            2
        ),

        "high_risk_tickets": int(
            high_risk_tickets
        ),

        "average_probability": round(
            average_probability,
            2
        )

    }