import streamlit as st
import pandas as pd
from components.ui import dropdown
import requests
from datetime import datetime
from io import BytesIO

API_BASE_URL = "https://intelligent-itsm-api.onrender.com"

HISTORY_API = f"{API_BASE_URL}/history"

st.set_page_config(
    page_title="Prediction History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Prediction History")

try:
    response = requests.get(HISTORY_API, timeout=30)
    response.raise_for_status()
    history = response.json()

except Exception as e:
    st.error(f"Unable to fetch prediction history.\n\n{e}")
    st.stop()

if len(history) == 0:

    st.info("No predictions available.")

else:

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

    df = pd.DataFrame(history)

    # ==========================================================
    # FILTER CONFIGURATION
    # ==========================================================

    FILTER_SECTIONS = {

        "Ticket Information": [

            ("Priority", "Priority", "Select Priority"),
            ("Category", "Category", "Select Category"),
            ("Sub Category", "Sub Category", "Select Sub Category"),
            ("Department", "Department", "Select Department"),
            ("Group", "Group", "Select Group"),
            ("Site", "Site", "Select Site"),
            ("Request Type", "Request Type", "Select Request Type")

        ],

        "Ticket Creation": [

            ("Created Day", "Created Day", "Select Day"),
            ("Created Month", "Created Month", "Select Month"),
            ("Created Hour", "Created Hour", "Select Hour")

        ],

        "Prediction": [

            ("Risk Level", "Risk Level", "Select Risk Level"),
            ("Prediction", "Prediction", "Select Prediction")

        ]
    }


    # Format probability
    df["Probability"] = df["Probability"].round(2)

    # Show latest predictions first
    df = (
        df
        .sort_values("ID", ascending=False)
        .reset_index(drop=True)
    )

    # ==========================================================
    # FILTER SIDEBAR
    # ==========================================================

    selected_filters = {}

    month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    day_order = [
        "Monday","Tuesday","Wednesday",
        "Thursday","Friday","Saturday","Sunday"
    ]

    with st.sidebar:

        st.header("⚙️ Filters")

        for section, filters in FILTER_SECTIONS.items():

            with st.expander(section, expanded=False):

                for column, label, placeholder in filters:

                    values = sorted(df[column].dropna().unique().tolist())

                    # ---------------- Month ---------------- #

                    if column == "Created Month":

                        values = [
                            month
                            for month in month_order
                            if month in values
                        ]

                    # ---------------- Day ---------------- #

                    elif column == "Created Day":

                        values = [
                            day
                            for day in day_order
                            if day in values
                        ]

                    # ---------------- Hour ---------------- #

                    elif column == "Created Hour":

                        labels = []

                        hour_map = {}

                        for hour in values:

                            if hour == 0:
                                display = "12 AM"

                            elif hour < 12:
                                display = f"{hour} AM"

                            elif hour == 12:
                                display = "12 PM"

                            else:
                                display = f"{hour-12} PM"

                            labels.append(display)
                            hour_map[display] = hour

                        selected = dropdown(
                            label,
                            labels,
                            placeholder
                        )

                        if selected is not None:
                            selected_filters[column] = hour_map[selected]

                        continue

                    # ---------------- Prediction ---------------- #

                    elif column == "Prediction":

                        values = [
                            "No Breach",
                            "Breach"
                        ]

                    # ---------------- Risk ---------------- #

                    elif column == "Risk Level":

                        values = [
                            "LOW",
                            "MEDIUM",
                            "HIGH"
                        ]

                    selected = dropdown(
                        label,
                        values,
                        placeholder
                    )

                    if selected is not None:
                        selected_filters[column] = selected

    # ==========================================================
    # APPLY FILTERS
    # ==========================================================

    filtered_df = df.copy()

    for column, value in selected_filters.items():

        filtered_df = filtered_df[
            filtered_df[column] == value
        ]

    # ==========================================================
    # SUMMARY CARDS
    # ==========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Predictions",
            len(filtered_df)
        )

    with col2:

        if len(filtered_df) > 0:

            breach_rate = (
                (filtered_df["Prediction"] == "Breach").mean() * 100
            )

            st.metric(
                "Breach Rate",
                f"{breach_rate:.1f}%"
            )

        else:

            st.metric(
                "Breach Rate",
                "0%"
            )

    with col3:

        st.metric(
            "High Risk",
            (filtered_df["Risk Level"] == "HIGH").sum()
        )

    # ==========================================================
    # DISPLAY TABLE
    # ==========================================================

    if filtered_df.empty:

        st.info(
            "No predictions match the selected filters. "
            "Try changing or clearing one or more filters."
        )

    else:

        display_df = filtered_df.copy()

        display_df = display_df[
            [
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
                "Risk Level",
            ]
        ]

        csv = display_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            label="⬇️ Download Prediction History (CSV)",

            data=csv,

            file_name=f"Prediction_History_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",

            mime="text/csv",

            use_container_width=True

        )

        display_df["Probability"] = display_df["Probability"]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:

            display_df.to_excel(
                writer,
                index=False,
                sheet_name="Prediction History"
            )

        excel_buffer.seek(0)

        st.download_button(

            label="📥 Download Prediction History (Excel)",

            data=excel_buffer,

            file_name=f"Prediction_History_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )
