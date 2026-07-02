def get_prediction_result(model, input_data):
    """
    Runs the trained model and returns prediction,
    probability, prediction text, risk level and colours.
    """

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1]

    breach_probability = probability * 100

    prediction_text = (
        "SLA Breach Expected"
        if prediction == 1
        else "No SLA Breach Expected"
    )

    if breach_probability < 25:
        risk_level = "LOW"
    elif breach_probability < 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    prediction_color = (
        "#ef4444"
        if prediction == 1
        else "#22c55e"
    )

    risk_color = {
        "LOW": "#22c55e",
        "MEDIUM": "#facc15",
        "HIGH": "#ef4444"
    }[risk_level]

    return (
        prediction,
        probability,
        breach_probability,
        prediction_text,
        prediction_color,
        risk_level,
        risk_color
    )