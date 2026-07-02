def get_recommendations(priority, breach_probability):
    """
    Returns operational recommendations based on
    breach probability and ticket priority.
    """

    priority = priority.lower()

    # ---------------- LOW ---------------- #

    if breach_probability < 30:

        recommendations = [
            "Follow the standard ticket assignment workflow.",
            "Assign the ticket according to the normal support queue.",
            "Continue routine SLA monitoring."
        ]

        if "severity - 1" in priority:
            recommendations.append(
                "Although breach risk is low, assign promptly due to business criticality."
            )

    # ---------------- MEDIUM ---------------- #

    elif breach_probability < 70:

        if "severity - 1" in priority:

            recommendations = [
                "Assign the ticket immediately.",
                "Monitor ticket progress frequently.",
                "Keep the department lead informed.",
                "Prepare for escalation if progress stalls."
            ]

        elif "severity - 2" in priority:

            recommendations = [
                "Prioritize ticket assignment.",
                "Monitor SLA progress periodically.",
                "Review the ticket if delays are observed."
            ]

        else:

            recommendations = [
                "Assign through the priority queue.",
                "Monitor SLA progress.",
                "Escalate only if delays are observed."
            ]

    # ---------------- HIGH ---------------- #

    else:

        if "severity - 1" in priority:

            recommendations = [
                "Assign immediately.",
                "Escalate to a senior engineer.",
                "Notify the department manager.",
                "Continuously monitor SLA progress.",
                "Allocate additional resources if required."
            ]

        elif "severity - 2" in priority:

            recommendations = [
                "Prioritize immediate assignment.",
                "Escalate to Level-2 support.",
                "Review ticket status every hour.",
                "Monitor SLA continuously."
            ]

        else:

            recommendations = [
                "Move the ticket to the top of the queue.",
                "Closely monitor progress.",
                "Escalate if meaningful progress is not observed.",
                "Keep the requester updated."
            ]

    return recommendations