import plotly.express as px

def create_risk_distribution_chart(df):

    risk_counts = (
        df["Risk Level"]
        .value_counts()
        .reindex(["LOW", "MEDIUM", "HIGH"], fill_value=0)
        .reset_index()
    )

    risk_counts.columns = ["Risk Level", "Count"]

    fig = px.pie(
        risk_counts,
        names="Risk Level",
        values="Count",
        hole=0.55,
        title="Risk Level Distribution",
        color="Risk Level",
        color_discrete_map={
            "LOW": "#22c55e",
            "MEDIUM": "#facc15",
            "HIGH": "#ef4444"
        }
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=50, b=10),
        legend_title_text=""
    )

    return fig


def create_department_chart(df):

    department_data = (
        df[df["Prediction"] == "Breach"]
        .groupby("Department")
        .size()
        .reset_index(name="Breach Count")
        .sort_values("Breach Count", ascending=False)
    )

    fig = px.bar(
        department_data,
        x="Department",
        y="Breach Count",
        title="Predicted SLA Breaches by Department",
        text="Breach Count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        xaxis_title="Department",
        yaxis_title="Number of Breaches",
        xaxis_tickangle=-30,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def create_category_chart(df):

    category_data = (
        df[df["Prediction"] == "Breach"]
        .groupby("Category")
        .size()
        .reset_index(name="Breach Count")
        .sort_values("Breach Count", ascending=False)
        .head(10)
    )

    fig = px.bar(
        category_data,
        x="Category",
        y="Breach Count",
        text="Breach Count",
        title="Top 10 Categories with Predicted SLA Breaches"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        xaxis_title="Category",
        yaxis_title="Number of Breaches",
        xaxis_tickangle=-30,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def create_site_chart(df):

    site_data = (
        df[df["Prediction"] == "Breach"]
        .groupby("Site")
        .size()
        .reset_index(name="Breach Count")
        .sort_values("Breach Count", ascending=False)
    )

    fig = px.bar(
        site_data,
        x="Site",
        y="Breach Count",
        text="Breach Count",
        title="Predicted SLA Breaches by Site"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        xaxis_title="Site",
        yaxis_title="Number of Breaches",
        xaxis_tickangle=-30,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def create_monthly_trend_chart(df):

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

    monthly_data = (
        df.groupby("Created Month")
        .size()
        .reindex(month_order, fill_value=0)
        .reset_index(name="Tickets")
    )

    fig = px.line(
        monthly_data,
        x="Created Month",
        y="Tickets",
        markers=True,
        title="Tickets Created per Month"
    )

    fig.update_layout(
        height=430,
        xaxis_title="Month",
        yaxis_title="Number of Tickets",
        xaxis_tickangle=-30,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def create_hour_distribution_chart(df):

    hour_data = (
        df.groupby("Created Hour")
        .size()
        .reset_index(name="Tickets")
        .sort_values("Created Hour")
    )

    hour_data["Hour"] = hour_data["Created Hour"].apply(
        lambda h:
        "12 AM" if h == 0 else
        f"{h} AM" if h < 12 else
        "12 PM" if h == 12 else
        f"{h-12} PM"
    )

    fig = px.bar(
        hour_data,
        x="Hour",
        y="Tickets",
        text="Tickets",
        title="Tickets by Creation Hour"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        xaxis_title="Hour",
        yaxis_title="Number of Tickets",
        xaxis_tickangle=-45,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


def create_high_risk_chart(df):

    high_risk_data = (
        df[df["Risk Level"] == "HIGH"]
        .groupby("Category")
        .size()
        .reset_index(name="High Risk Tickets")
        .sort_values("High Risk Tickets", ascending=False)
        .head(10)
    )

    fig = px.bar(
        high_risk_data,
        x="High Risk Tickets",
        y="Category",
        orientation="h",
        text="High Risk Tickets",
        title="Top Categories Requiring Immediate Attention"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Number of High Risk Tickets",
        yaxis_title="Category",
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(categoryorder="total ascending")
    )

    return fig