from environment import CampusEnvironment
from agent import SecurityAgent
from incidents import IncidentManager
from explainability import DecisionExplainer


class UtilityBasedPatrolAgent(SecurityAgent):
    """Security agent that selects destinations using utility scores."""

    def __init__(
        self,
        campus,
        start_location="Main Gate",
        battery=100,
        initial_charge=None,
    ):
        super().__init__(
            campus=campus,
            start_location=start_location,
            battery=battery,
            initial_charge=initial_charge,
        )

        # ========================================================
        # SECURITY RISK
        # ========================================================

        # Base security risk for each campus zone.
        self.incident_risk = {
            "Main Gate": 7,
            "Academic Block": 5,
            "Library": 3,
            "Hostel": 8,
            "Canteen": 4,
            "Parking": 6,
            "Sports Ground": 5,
            "Administration": 4,
            "Security Office": 2,
        }

        # ========================================================
        # PATROL STATE
        # ========================================================

        # Patrol step counter.
        self.patrol_step = 0

        # Stores the last patrol step at which each location
        # was visited.
        # -1 means the location has not been visited yet.
        self.last_visited = {
            location: -1
            for location in self.campus.get_locations()
        }

        # The agent starts at the starting location.
        self.last_visited[start_location] = 0

        # ========================================================
        # LIVE ALERTS
        # ========================================================

        # Live alert score for each campus location.
        self.live_alerts = {
            location: 0
            for location in self.campus.get_locations()
        }

        # ========================================================
        # UTILITY FUNCTION
        # ========================================================

        # Utility function weights.
        #
        # Total = 1.00
        #
        # Alert has the highest weight because an active
        # security incident should receive strong priority.
        self.weights = {
            "risk": 0.25,
            "coverage": 0.20,
            "alert": 0.40,
            "travel": 0.10,
            "battery": 0.05,
        }

        # ========================================================
        # EXPLAINABILITY
        # ========================================================

        self.explainer = DecisionExplainer(
            self.weights
        )

        # Stores the complete latest AI decision.
        # This is used by the dashboard to explain
        # why the agent selected a destination.
        self.last_decision = {}

        # ========================================================
        # INCIDENT MANAGEMENT
        # ========================================================

        self.incident_manager = IncidentManager(
            campus
        )

    # ============================================================
    # INCIDENT / ALERT MANAGEMENT
    # ============================================================

    def update_alerts_from_incidents(self):
        """Update live alert scores from active incidents."""

        # Reset current alerts.
        for location in self.live_alerts:
            self.live_alerts[location] = 0

        # Get all active incidents.
        active_incidents = (
            self.incident_manager.get_active_incidents()
        )

        # Apply the highest priority incident
        # to each location.
        for incident in active_incidents:
            self.live_alerts[incident.location] = max(
                self.live_alerts[incident.location],
                incident.priority,
            )

    # ============================================================
    # COVERAGE / REVISIT CALCULATION
    # ============================================================

    def calculate_revisit_time(self, location):
        """Calculate patrol steps since a location was last visited."""

        last_visit = self.last_visited[location]

        # If the location has never been visited,
        # give it a high revisit value.
        if last_visit == -1:
            return self.patrol_step + 1

        return self.patrol_step - last_visit

    # ============================================================
    # UTILITY CALCULATION
    # ============================================================

    def calculate_utility(self, destination):
        """Calculate the utility score for a possible destination."""

        # Distance from current location to destination.
        distance = self.campus.get_distance(
            self.current_location,
            destination,
        )

        # Base security risk.
        risk_score = self.incident_risk[
            destination
        ]

        # Dynamic coverage score based on revisit time.
        revisit_time = self.calculate_revisit_time(
            destination
        )

        # Limit coverage score to a maximum of 10.
        coverage_score = min(
            revisit_time,
            10,
        )

        # Current live security alert.
        alert_score = self.live_alerts[
            destination
        ]

        # Travel and battery costs.
        travel_cost = distance
        battery_cost = distance

        # Overall utility calculation.
        utility = (
            self.weights["risk"] * risk_score
            + self.weights["coverage"]
            * coverage_score
            + self.weights["alert"]
            * alert_score
            - self.weights["travel"]
            * travel_cost
            - self.weights["battery"]
            * battery_cost
        )

        return utility

    # ============================================================
    # DESTINATION SELECTION
    # ============================================================

    def choose_best_destination(self):
        """Evaluate reachable destinations and select the highest utility."""

        # Update live alerts before making a decision.
        self.update_alerts_from_incidents()

        locations = self.campus.get_locations()

        # Do not select the current location.
        available_locations = [
            location
            for location in locations
            if location != self.current_location
        ]

        utility_scores = {}

        for location in available_locations:

            try:

                distance = self.campus.get_distance(
                    self.current_location,
                    location,
                )

                # Only consider locations that the agent
                # can reach with its current battery.
                if distance <= self.battery:

                    utility_scores[location] = (
                        self.calculate_utility(
                            location
                        )
                    )

            except Exception:
                continue

        # No reachable destination.
        if not utility_scores:
            return None, {}

        # Select the highest utility destination.
        best_destination = max(
            utility_scores,
            key=utility_scores.get,
        )

        return (
            best_destination,
            utility_scores,
        )

    # ============================================================
    # PATROL DECISION
    # ============================================================

    def patrol_once(self):
        """Perform one utility-based patrol decision."""

        # --------------------------------------------------------
        # BATTERY CHECK
        # --------------------------------------------------------

        if not self.check_battery():
            return self.go_to_charging_station()

        # --------------------------------------------------------
        # INCREMENT PATROL STEP
        # --------------------------------------------------------

        self.patrol_step += 1

        # --------------------------------------------------------
        # SELECT DESTINATION
        # --------------------------------------------------------

        destination, utility_scores = (
            self.choose_best_destination()
        )

        if destination is None:
            print(
                "No reachable destination available."
            )
            return False

        # --------------------------------------------------------
        # DISPLAY DECISION
        # --------------------------------------------------------

        print(
            "\n--- Utility-Based Patrol Decision ---"
        )

        print(
            f"Patrol step: {self.patrol_step}"
        )

        print(
            f"Current location: "
            f"{self.current_location}"
        )

        print("\nUtility scores:")

        # Display destinations from highest
        # to lowest utility.
        for location, score in sorted(
            utility_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        ):

            alert = self.live_alerts[
                location
            ]

            revisit_time = (
                self.calculate_revisit_time(
                    location
                )
            )

            print(
                f"{location}: {score:.2f} "
                f"(Revisit Time: {revisit_time}, "
                f"Live Alert: {alert})"
            )

        print(
            f"\nSelected destination: "
            f"{destination}"
        )

        # --------------------------------------------------------
        # CALCULATE DECISION FACTORS
        # --------------------------------------------------------

        distance = self.campus.get_distance(
            self.current_location,
            destination,
        )

        risk_score = self.incident_risk[
            destination
        ]

        revisit_time = (
            self.calculate_revisit_time(
                destination
            )
        )

        coverage_score = min(
            revisit_time,
            10,
        )

        alert_score = self.live_alerts[
            destination
        ]

        travel_cost = distance
        battery_cost = distance

        # Save battery level before movement.
        battery_before = self.battery

        # --------------------------------------------------------
        # STORE AI DECISION
        # --------------------------------------------------------

        self.last_decision = {
            "destination": destination,
            "utility_score": utility_scores[
                destination
            ],
            "risk_score": risk_score,
            "coverage_score": coverage_score,
            "alert_score": alert_score,
            "revisit_time": revisit_time,
            "travel_cost": travel_cost,
            "battery_cost": battery_cost,
            "battery_before": battery_before,
            "battery_after": battery_before,
            "patrol_step": self.patrol_step,
            "utility_scores": utility_scores.copy(),
        }

        # --------------------------------------------------------
        # EXPLAIN DECISION
        # --------------------------------------------------------

        self.explainer.explain_decision(
            destination=destination,
            utility_score=utility_scores[
                destination
            ],
            risk_score=risk_score,
            coverage_score=coverage_score,
            alert_score=alert_score,
            travel_cost=travel_cost,
            battery_cost=battery_cost,
            revisit_time=revisit_time,
        )

        # --------------------------------------------------------
        # MOVE AGENT
        # --------------------------------------------------------

        success = self.move_to(
            destination
        )

        # --------------------------------------------------------
        # UPDATE PATROL HISTORY
        # --------------------------------------------------------

        if success:

            self.last_visited[destination] = (
                self.patrol_step
            )

            # Store battery after movement.
            self.last_decision["battery_after"] = (
                self.battery
            )

            # ----------------------------------------------------
            # AUTOMATIC INCIDENT RESPONSE
            # ----------------------------------------------------

            active_incidents = (
                self.incident_manager
                .get_active_incidents()
            )

            for incident in active_incidents:

                if (
                    incident.location
                    == self.current_location
                ):

                    print(
                        "\n🚨 INCIDENT LOCATION REACHED"
                    )

                    print(
                        f"Incident: "
                        f"{incident.incident_type}"
                    )

                    print(
                        f"Location: "
                        f"{incident.location}"
                    )

                    # Resolve the incident.
                    self.incident_manager.resolve_incident(
                        incident,
                        current_step=self.patrol_step,
                    )

                    print(
                        f"⏱️ Response time: "
                        f"{incident.get_response_time()} "
                        f"patrol steps"
                    )

        return success

    # ============================================================
    # INCIDENT DISPLAY
    # ============================================================

    def display_incidents(self):
        """Display currently active incidents."""

        self.incident_manager.display_active_incidents()


# ================================================================
# MAIN TEST
# ================================================================

if __name__ == "__main__":

    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
        initial_charge=15,
    )

    print(
        "=== UTILITY-BASED PATROL "
        "WITH EXPLAINABILITY ==="
    )

    # Display initial agent status.
    agent.status()

    # ------------------------------------------------------------
    # CREATE FIRE ALERT
    # ------------------------------------------------------------

    agent.incident_manager.create_incident(
        "Fire Alert",
        "Canteen",
        "Possible fire detected near the canteen.",
        detected_at_step=agent.patrol_step,
    )

    # ------------------------------------------------------------
    # CREATE UNAUTHORIZED ENTRY ALERT
    # ------------------------------------------------------------

    agent.incident_manager.create_incident(
        "Unauthorized Entry",
        "Main Gate",
        "Unauthorized person detected "
        "at the main entrance.",
        detected_at_step=agent.patrol_step,
    )

    # Display active incidents.
    agent.display_incidents()

    print("\n=== AGENT RESPONSE ===")

    # Run three patrol decisions.
    for step in range(3):

        print(
            f"\n========== "
            f"Patrol Step {step + 1} "
            f"=========="
        )

        success = agent.patrol_once()

        if not success:

            print(
                "Patrol stopped."
            )

            break

    print(
        "\n=== FINAL AGENT STATUS ==="
    )

    agent.status()
