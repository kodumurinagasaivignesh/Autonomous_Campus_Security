import random

from environment import CampusEnvironment
from agent import SecurityAgent


class RandomPatrolAgent(SecurityAgent):
    """Security agent that randomly selects patrol destinations."""

    def choose_random_destination(self):
        """Choose a random campus location different from the current one."""

        locations = self.campus.get_locations()

        available_locations = [
            location
            for location in locations
            if location != self.current_location
        ]

        return random.choice(available_locations)

    def patrol_once(self):
        """Perform one random patrol decision."""

        destination = self.choose_random_destination()

        print("\n--- Random Patrol Decision ---")
        print(f"Current location: {self.current_location}")
        print(f"Random destination: {destination}")

        return self.move_to(destination)


if __name__ == "__main__":
    campus = CampusEnvironment()

    agent = RandomPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    print("=== RANDOM PATROL SIMULATION ===")

    agent.status()

    for step in range(5):
        print(f"\n========== Patrol Step {step + 1} ==========")

        success = agent.patrol_once()

        if not success:
            print("Patrol stopped because the agent cannot continue.")
            break

    print("\n=== FINAL AGENT STATUS ===")
    agent.status()