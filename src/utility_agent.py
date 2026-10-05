from environment import CampusEnvironment
from agent import SecurityAgent


class UtilityBasedPatrolAgent(SecurityAgent):
    """Security agent that selects destinations using a utility score."""

    def __init__(self, campus, start_location="Main Gate", battery=100):
        super().__init__(
            campus=campus,
            start_location=start_location,
            battery=battery,
        )

        # Simulated security information for each campus zone.
        # Higher values mean greater priority.
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

        # How much each zone needs to be visited.
        self.coverage_need = {
            "Main Gate": 5,
            "Academic Block": 6,
            "Library": 4,
            "Hostel": 8,
            "Canteen": 5,
            "Parking": 7,
            "Sports Ground": 6,
            "Administration": 4,
            "Security Office": 2,
        }

        # Simulated live alerts.
        # 0 means no active alert.
        self.live_alerts = {
            location: 0
            for location in self.campus.get_locations()
        }

        # Weights determine how important each factor is.
        self.weights = {
            "risk": 0.35,
            "coverage": 0.25,
            "alert": 0.25,
            "travel": 0.10,
            "battery": 0.05,
        }

    def calculate_utility(self, destination):
        """Calculate the utility score for a possible destination."""

        distance = self.campus.get_distance(
            self.current_location,
            destination,
        )

        risk_score = self.incident_risk[destination]
        coverage_score = self.coverage_need[destination]
        alert_score = self.live_alerts[destination]

        # Higher distance means higher travel cost.
        travel_cost = distance

        # Higher distance also consumes more battery.
        battery_cost = distance

        utility = (
            self.weights["risk"] * risk_score
            + self.weights["coverage"] * coverage_score
            + self.weights["alert"] * alert_score
            - self.weights["travel"] * travel_cost
            - self.weights["battery"] * battery_cost
        )

        return utility

    def choose_best_destination(self):
        """Evaluate possible destinations and select the highest utility."""

        locations = self.campus.get_locations()

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

                # Ignore destinations that cannot currently be reached.
                if distance <= self.battery:
                    utility_scores[location] = self.calculate_utility(location)

            except Exception:
                continue

        if not utility_scores:
            return None, {}

        best_destination = max(
            utility_scores,
            key=utility_scores.get,
        )

        return best_destination, utility_scores

    def patrol_once(self):
        """Perform one utility-based patrol decision."""

        destination, utility_scores = self.choose_best_destination()

        if destination is None:
            print("No reachable destination available.")
            return False

        print("\n--- Utility-Based Patrol Decision ---")
        print(f"Current location: {self.current_location}")

        print("\nUtility scores:")

        for location, score in sorted(
            utility_scores.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            print(f"{location}: {score:.2f}")

        print(f"\nSelected destination: {destination}")

        return self.move_to(destination)


if __name__ == "__main__":
    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    print("=== UTILITY-BASED PATROL SIMULATION ===")

    agent.status()

    for step in range(5):
        print(f"\n========== Patrol Step {step + 1} ==========")

        success = agent.patrol_once()

        if not success:
            print("Patrol stopped.")
            break

    print("\n=== FINAL AGENT STATUS ===")
    agent.status()