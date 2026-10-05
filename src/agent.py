from environment import CampusEnvironment


class SecurityAgent:
    """Basic autonomous security patrol agent."""

    def __init__(self, campus, start_location="Main Gate", battery=100):
        self.campus = campus
        self.current_location = start_location
        self.battery = battery
        self.patrol_history = [start_location]
        self.total_distance = 0

    def move_to(self, destination):
        """Move the agent to a connected destination."""

        if destination not in self.campus.graph:
            raise ValueError(f"Unknown destination: {destination}")

        distance = self.campus.get_distance(
            self.current_location,
            destination
        )

        if distance > self.battery:
            print("Not enough battery to reach the destination.")
            return False

        path = self.campus.get_shortest_path(
            self.current_location,
            destination
        )

        self.current_location = destination
        self.battery -= distance
        self.total_distance += distance
        self.patrol_history.append(destination)

        print(f"Agent moved: {' -> '.join(path)}")
        print(f"Current location: {self.current_location}")
        print(f"Battery remaining: {self.battery}")
        print(f"Total distance: {self.total_distance}")

        return True

    def status(self):
        """Display the current agent status."""

        print("\n--- Security Agent Status ---")
        print(f"Location: {self.current_location}")
        print(f"Battery: {self.battery}")
        print(f"Total distance: {self.total_distance}")
        print(f"Patrol history: {self.patrol_history}")


if __name__ == "__main__":
    campus = CampusEnvironment()

    agent = SecurityAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100
    )

    agent.status()

    print("\nMoving to Library...")
    agent.move_to("Library")

    print("\nMoving to Hostel...")
    agent.move_to("Hostel")

    agent.status()