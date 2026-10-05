from environment import CampusEnvironment
from agent import SecurityAgent


class FixedRoutePatrolAgent(SecurityAgent):
    """Security agent that follows a predefined patrol route."""

    def __init__(self, campus, route, start_location=None, battery=100):
        if not route:
            raise ValueError("Patrol route cannot be empty.")

        if start_location is None:
            start_location = route[0]

        super().__init__(
            campus=campus,
            start_location=start_location,
            battery=battery,
        )

        self.route = route
        self.route_index = self.route.index(start_location)

    def choose_next_destination(self):
        """Choose the next destination in the fixed patrol route."""

        self.route_index = (self.route_index + 1) % len(self.route)

        return self.route[self.route_index]

    def patrol_once(self):
        """Perform one fixed-route patrol step."""

        destination = self.choose_next_destination()

        print("\n--- Fixed Route Patrol Decision ---")
        print(f"Current location: {self.current_location}")
        print(f"Next route destination: {destination}")

        return self.move_to(destination)


if __name__ == "__main__":
    campus = CampusEnvironment()

    patrol_route = [
        "Main Gate",
        "Academic Block",
        "Library",
        "Canteen",
        "Hostel",
        "Sports Ground",
        "Parking",
    ]

    agent = FixedRoutePatrolAgent(
        campus=campus,
        route=patrol_route,
        start_location="Main Gate",
        battery=100,
    )

    print("=== FIXED ROUTE PATROL SIMULATION ===")

    agent.status()

    for step in range(7):
        print(f"\n========== Patrol Step {step + 1} ==========")

        success = agent.patrol_once()

        if not success:
            print("Patrol stopped because the agent cannot continue.")
            break

    print("\n=== FINAL AGENT STATUS ===")
    agent.status()