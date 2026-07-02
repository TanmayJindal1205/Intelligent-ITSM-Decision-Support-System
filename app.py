import streamlit as st
import joblib
import json
from pathlib import Path
import pandas as pd
from components.prediction import get_prediction_result
from components.recommendations import get_recommendations
from components.cards import metric_card
from database.database import create_database, save_prediction
from components.ui import dropdown

def load_css():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

create_database()

# ==========================================================
# LOAD MODEL
# ==========================================================

@st.cache_resource
def load_model():
    return joblib.load("model/final_model.pkl")

model = load_model()

# ==========================================================
# LOAD DROPDOWN VALUES
# ==========================================================

@st.cache_data
def load_metadata():
    with open(Path("model") / "metadata.json", "r") as f:
        return json.load(f)

metadata = load_metadata()

# ==========================================================
# ORDER DAYS AND MONTHS CHRONOLOGICALLY
# ==========================================================

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

metadata["Created_Day"] = [
    day for day in day_order
    if day in metadata["Created_Day"]
]

metadata["Created_Month"] = [
    month for month in month_order
    if month in metadata["Created_Month"]
]

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Intelligent ITSM Decision Support System",
    page_icon="🛠️",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🛠️ Intelligent ITSM Decision Support System")

st.caption(
    "AI-Powered IT Service Ticket Risk Assessment"
)

st.divider()

# --------------------------------------------------
# Prediction Form Section
# --------------------------------------------------
st.subheader("📋 New Ticket Prediction")

st.write(
    "Fill in the ticket details below to assess the likelihood of an SLA breach "
    "and receive proactive recommendations."
)

st.divider()

# ==========================================================
# Ticket Information
# ==========================================================

st.subheader("📋 Ticket Information")

col1, col2 = st.columns(2)

with col1:

    priority = dropdown(
        "Priority",
        metadata["Priority"],
        "Select Priority"
    )

    category = dropdown(
        "Category",
        metadata["Category"],
        "Select Category"
    )

    sub_category = dropdown(
        "Sub Category",
        metadata["Sub Category"],
        "Select Sub Category"
    )

    request_type = dropdown(
        "Request Type",
        metadata["Request Type"],
        "Select Request Type"
    )

with col2:

    department = dropdown(
        "Department",
        metadata["Department"],
        "Select Department"
    )

    group = dropdown(
        "Group",
        metadata["Group"],
        "Select Group"
    )

    site = dropdown(
        "Site",
        metadata["Site"],
        "Select Site"
    )

st.divider()

# ==========================================================
# Ticket Creation
# ==========================================================

st.subheader("🕒 Ticket Creation")

col1, col2 = st.columns(2)

with col1:

    created_month = dropdown(
        "Created Month",
        metadata["Created_Month"],
        "Select Month"
    )

    created_day = dropdown(
        "Created Day",
        metadata["Created_Day"],
        "Select Day"
    )

with col2:

    # Create 12-hour display labels while keeping 24-hour values
    hour_mapping = {}

    for hour in range(24):

        if hour == 0:
            label = "12 AM"

        elif hour < 12:
            label = f"{hour} AM"

        elif hour == 12:
            label = "12 PM"

        else:
            label = f"{hour - 12} PM"

        hour_mapping[label] = hour

    selected_hour = st.selectbox(
        "Created Hour",
        list(hour_mapping.keys()),
        index=None,
        placeholder="Select Hour"
    )

    created_hour = (
        None
        if selected_hour is None
        else hour_mapping[selected_hour]
    )

st.divider()

predict_button = st.button(
    "🔍 Predict SLA Risk",
    use_container_width=True
)

# ==========================================================
# PREDICTION
# ==========================================================

if predict_button:

    # -------------------------------
    # Validate Input
    # -------------------------------

    required_fields = [
        priority,
        category,
        sub_category,
        department,
        group,
        site,
        request_type,
        created_day,
        created_month,
        created_hour
    ]

    if any(field is None for field in required_fields):
        st.warning("⚠️ Please select all fields before making a prediction.")
        st.stop()

    # -------------------------------
    # Prepare Input Data
    # -------------------------------

    input_data = pd.DataFrame({
        "Priority": [priority],
        "Category": [category],
        "Sub Category": [sub_category],
        "Department": [department],
        "Group": [group],
        "Site": [site],
        "Request Type": [request_type],
        "Created_Day": [created_day],
        "Created_Month": [created_month],
        "Created_Hour": [created_hour]
    })

    # -------------------------------
    # Make Prediction
    # -------------------------------

    (
        prediction,
        probability,
        breach_probability,
        prediction_text,
        prediction_color,
        risk_level,
        risk_color
    ) = get_prediction_result(model, input_data)

    save_prediction(
        priority,
        category,
        sub_category,
        department,
        group,
        site,
        request_type,
        created_day,
        created_month,
        created_hour,
        prediction,
        breach_probability,
        risk_level
    )

    recommendations = get_recommendations(
        priority,
        breach_probability
    )

    # ==========================================================
    # Prediction Result
    # ==========================================================

    st.divider()

    st.subheader("📊 Prediction Result")

    col1, col2, col3 = st.columns(3)

    with col1:

        metric_card(
            "Prediction",
            ("🟢 " + prediction_text) if prediction == 0 else ("🔴 " + prediction_text),
            prediction_color
        )

    with col2:

        metric_card(
            "SLA Breach Probability",
            f"{breach_probability:.1f}%",
            "#ffffff"
        )

    with col3:

        metric_card(
            "Risk Level",
            risk_level,
            risk_color
        )

    st.markdown("## 📌 Recommended Operational Actions")
    for recommendation in recommendations:
        st.success(recommendation, icon="✅")