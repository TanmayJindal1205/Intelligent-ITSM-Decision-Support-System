import streamlit as st
import pandas as pd
from components.charts import (
    create_risk_distribution_chart,
    create_department_chart,
    create_category_chart,
    create_site_chart,
    create_monthly_trend_chart,
    create_hour_distribution_chart,
    create_high_risk_chart
)
from database.database import get_all_predictions
from io import BytesIO
from datetime import datetime

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analytics Dashboard")

st.caption(
    "Interactive analytics and operational insights for ITSM SLA predictions."
)

st.divider()

# ==========================================================
# LOAD DATA
# ==========================================================

records = get_all_predictions()

if len(records) == 0:

    st.info("No prediction history available.")

    st.stop()

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

df = pd.DataFrame(records, columns=columns)

# ==========================================================
# DATA PREPARATION
# ==========================================================

df["Prediction"] = df["Prediction"].map({
    0: "No Breach",
    1: "Breach"
})

df["Probability"] = df["Probability"].round(2)

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.subheader("📈 Executive Summary")

total_predictions = len(df)

breach_rate = (
    (df["Prediction"] == "Breach").mean() * 100
)

high_risk = (
    df["Risk Level"] == "HIGH"
).sum()

average_probability = df["Probability"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Predictions",
        total_predictions
    )

with col2:

    st.metric(
        "Breach Rate",
        f"{breach_rate:.1f}%"
    )

with col3:

    st.metric(
        "High Risk Tickets",
        high_risk
    )

with col4:

    st.metric(
        "Average Probability",
        f"{average_probability:.1f}%"
    )

# ==========================================================
# DOWNLOAD ANALYTICS REPORT
# ==========================================================

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    summary_df = pd.DataFrame({

        "Metric": [

            "Total Predictions",
            "Breach Rate (%)",
            "High Risk Tickets",
            "Average Probability (%)"

        ],

        "Value": [

            total_predictions,
            round(breach_rate, 2),
            high_risk,
            round(average_probability, 2)

        ]

    })

    summary_df.to_excel(
        writer,
        sheet_name="Executive Summary",
        index=False
    )

    risk_distribution = (
        df["Risk Level"]
        .value_counts()
        .reindex(
            ["LOW", "MEDIUM", "HIGH"],
            fill_value=0
        )
        .reset_index()
    )

    risk_distribution.columns = [
        "Risk Level",
        "Count"
    ]

    risk_distribution.to_excel(
        writer,
        sheet_name="Risk Distribution",
        index=False
    )

    department_analysis = (
        df[df["Prediction"] == "Breach"]
        .groupby("Department")
        .size()
        .reset_index(name="Breach Count")
        .sort_values(
            "Breach Count",
            ascending=False
        )
    )

    department_analysis.to_excel(
        writer,
        sheet_name="Department Analysis",
        index=False
    )

excel_buffer.seek(0)

st.download_button(

    label="📥 Download Analytics Report",

    data=excel_buffer,

    file_name=f"Analytics_Report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

    use_container_width=True

)

st.divider()

# ==========================================================
# RISK DISTRIBUTION & DEPARTMENT-WISE BREACH ANALYSIS
# ==========================================================

left_col, right_col = st.columns([1, 2])

with left_col:

    st.subheader("🎯 Risk Distribution")

    st.plotly_chart(
        create_risk_distribution_chart(df),
        use_container_width=True,
        key="risk_distribution_chart",
        config={"displayModeBar": False}
    )

with right_col:

    st.subheader("🏢 Department-wise Breach Analysis")

    st.plotly_chart(
        create_department_chart(df),
        use_container_width=True,
        key="department_chart",
        config={
            "displayModeBar": False
        }
    )

# ==========================================================
# CATEGORY & SITE ANALYSIS
# ==========================================================

left_col, right_col = st.columns(2)

# ----------------------------------------------------------
# CATEGORY ANALYSIS
# ----------------------------------------------------------

with left_col:

    st.subheader("📂 Category-wise Breach Analysis")

    st.plotly_chart(
        create_category_chart(df),
        use_container_width=True,
        key="category_chart",
        config={
            "displayModeBar": False
        }
    )

# ----------------------------------------------------------
# SITE ANALYSIS
# ----------------------------------------------------------

with right_col:

    st.subheader("📍 Site-wise Breach Analysis")

    st.plotly_chart(
        create_site_chart(df),
        use_container_width=True,
        key="site_chart",
        config={
            "displayModeBar": False
        }
    )

# ==========================================================
# MONTHLY TREND & HOUR-WISE DISTRIBUTION
# ==========================================================

left_col, right_col = st.columns(2)

# ----------------------------------------------------------
# MONTHLY TREND
# ----------------------------------------------------------

with left_col:

    st.subheader("📈 Monthly Ticket Trend")

    st.plotly_chart(
        create_monthly_trend_chart(df),
        use_container_width=True,
        key="monthly_trend_chart",
        config={
            "displayModeBar": False
        }
    )

# ----------------------------------------------------------
# HOUR-WISE DISTRIBUTION
# ----------------------------------------------------------

with right_col:

    st.subheader("🕒 Hour-wise Ticket Distribution")

    st.plotly_chart(
        create_hour_distribution_chart(df),
        use_container_width=True,
        key="hour_distribution_chart",
        config={
            "displayModeBar": False
        }
    )

# ==========================================================
# TOP HIGH-RISK CATEGORIES
# ==========================================================

st.subheader("🚨 Top High-Risk Categories")

st.plotly_chart(
    create_high_risk_chart(df),
    use_container_width=True,
    key="high_risk_categories_chart",
    config={
        "displayModeBar": False
    }
)   
