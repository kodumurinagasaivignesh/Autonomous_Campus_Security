class DecisionExplainer:
    """Explains why the autonomous patrol agent selected a destination."""

    def __init__(self, weights):
        self.weights = weights

    def explain_decision(
        self,
        destination,
        utility_score,
        risk_score,
        coverage_score,
        alert_score,
        travel_cost,
        battery_cost,
        revisit_time,
    ):
        print("\n=== DECISION EXPLANATION ===")

        print(f"Selected destination: {destination}")
        print(f"Final utility score: {utility_score:.2f}")

        print("\nDecision factors:")

        print(
            f"- Security risk score: {risk_score}"
        )

        print(
            f"- Coverage need score: {coverage_score}"
        )

        print(
            f"- Live alert score: {alert_score}"
        )

        print(
            f"- Revisit time: {revisit_time}"
        )

        print(
            f"- Travel cost: {travel_cost}"
        )

        print(
            f"- Battery cost: {battery_cost}"
        )

        print("\nUtility weights:")

        for factor, weight in self.weights.items():
            print(
                f"- {factor}: {weight}"
            )

        print("\nReason:")

        reasons = []

        if alert_score > 0:
            reasons.append(
                "an active security alert is present"
            )

        if risk_score >= 7:
            reasons.append(
                "the area has high security risk"
            )

        if coverage_score >= 7:
            reasons.append(
                "the area requires greater patrol coverage"
            )

        if revisit_time >= 3:
            reasons.append(
                "the area has not been visited recently"
            )

        if travel_cost <= 3:
            reasons.append(
                "the destination is relatively close"
            )

        if battery_cost > 5:
            reasons.append(
                "the destination requires significant battery usage"
            )

        if reasons:
            print(
                "The destination was selected because "
                + ", ".join(reasons)
                + "."
            )
        else:
            print(
                "The destination achieved the highest "
                "overall utility score among reachable locations."
            )