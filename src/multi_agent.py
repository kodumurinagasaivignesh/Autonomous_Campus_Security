from environment import CampusEnvironment
from utility_agent import UtilityBasedPatrolAgent


class MultiAgentPatrolSystem:
    """Coordinates multiple autonomous patrol agents."""

    def __init__(self, campus):
        self.campus = campus

        self.agent_1 = UtilityBasedPatrolAgent(
            campus=campus,
            start_location="Main Gate",
            battery=100,
        )

        self.agent_2 = UtilityBasedPatrolAgent(
            campus=campus,
            start_location="Security Office",
            battery=100,
        )

        self.assigned_zones = {
            "Agent 1": set(),
            "Agent 2": set(),
        }

    def get_available_destinations(self, agent):
        """Return locations that the agent can reach."""
        locations = self.campus.get_locations()

        return [
            location
            for location in locations
            if location != agent.current_location
        ]

    def assign_zone(self, agent_name, destination):
        """Record a zone assignment for an agent."""
        self.assigned_zones[agent_name].add(destination)

    def display_assignments(self):
        print("\n=== TERRITORY ASSIGNMENTS ===")

        for agent_name, zones in self.assigned_zones.items():
            if zones:
                print(f"{agent_name}: {sorted(zones)}")
            else:
                print(f"{agent_name}: No zones assigned")

    def patrol_step(self):
        """Perform one coordinated patrol step."""

        print("\n======================================")
        print("       MULTI-AGENT PATROL STEP")
        print("======================================")

        # Agent 1 selects its best destination.
        destination_1, scores_1 = (
            self.agent_1.choose_best_destination()
        )

        # Agent 2 selects its best destination.
        destination_2, scores_2 = (
            self.agent_2.choose_best_destination()
        )

        # Prevent both agents from selecting the same destination.
        if (
            destination_1 is not None
            and destination_2 is not None
            and destination_1 == destination_2
        ):
            print(
                f"\n⚠️ Both agents selected {destination_1}."
            )

            alternative_destinations = {
                location: score
                for location, score in scores_2.items()
                if location != destination_1
            }

            if alternative_destinations:
                destination_2 = max(
                    alternative_destinations,
                    key=alternative_destinations.get,
                )

                print(
                    f"🔄 Agent 2 redirected to "
                    f"{destination_2} to avoid overlap."
                )

        # Move Agent 1.
        if destination_1 is not None:
            print(
                f"\n🤖 Agent 1 → {destination_1}"
            )

            self.agent_1.move_to(destination_1)
            self.assign_zone("Agent 1", destination_1)

        # Move Agent 2.
        if destination_2 is not None:
            print(
                f"\n🤖 Agent 2 → {destination_2}"
            )

            self.agent_2.move_to(destination_2)
            self.assign_zone("Agent 2", destination_2)

        self.display_assignments()

    def display_status(self):
        print("\n======================================")
        print("       MULTI-AGENT SYSTEM STATUS")
        print("======================================")

        print("\n--- Agent 1 ---")
        self.agent_1.status()

        print("\n--- Agent 2 ---")
        self.agent_2.status()

        self.display_assignments()


if __name__ == "__main__":

    campus = CampusEnvironment()

    system = MultiAgentPatrolSystem(campus)

    print("======================================")
    print("   AUTONOMOUS MULTI-AGENT PATROL")
    print("======================================")

    system.display_status()

    for step in range(5):

        print(
            f"\n\n========== SYSTEM STEP {step + 1} =========="
        )

        system.patrol_step()

    print("\n\n========== FINAL SYSTEM STATUS ==========")

    system.display_status()