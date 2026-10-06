from environment import CampusEnvironment
from utility_agent import UtilityBasedPatrolAgent


class MultiAgentPatrolSystem:
    """
    Coordinates multiple autonomous patrol agents
    using territory-based coverage.
    """

    def __init__(self, campus):
        self.campus = campus

        # Create two autonomous patrol agents
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

        # Divide campus into territories
        locations = self.campus.get_locations()
        midpoint = len(locations) // 2

        self.territories = {
            "Agent 1": set(locations[:midpoint]),
            "Agent 2": set(locations[midpoint:]),
        }

        # Backward-compatible name used by earlier tests/code
        self.assigned_zones = self.territories

        # Track locations actually visited by each agent
        self.coverage = {
            "Agent 1": set(),
            "Agent 2": set(),
        }

        self.step_count = 0

    # --------------------------------------------------
    # TERRITORY MANAGEMENT
    # --------------------------------------------------

    def display_territories(self):
        print("\n=== CAMPUS TERRITORIES ===")

        for agent_name, zones in self.territories.items():
            print(f"\n{agent_name}:")

            for zone in sorted(zones):
                print(f"  - {zone}")

    def get_agent_territory(self, agent_name):
        """Return the territory assigned to an agent."""

        if agent_name not in self.territories:
            raise ValueError(f"Unknown agent: {agent_name}")

        return self.territories[agent_name]

    def assign_zone(self, agent_name, destination):
        """Assign an additional campus zone to an agent."""

        if agent_name not in self.territories:
            raise ValueError(f"Unknown agent: {agent_name}")

        if destination not in self.campus.graph:
            raise ValueError(
                f"Unknown campus location: {destination}"
            )

        self.territories[agent_name].add(destination)

    # --------------------------------------------------
    # COVERAGE MANAGEMENT
    # --------------------------------------------------

    def update_coverage(self, agent_name, location):
        """Record a successfully visited location."""

        if agent_name not in self.coverage:
            raise ValueError(f"Unknown agent: {agent_name}")

        self.coverage[agent_name].add(location)

    def calculate_coverage_percentage(self, agent_name):
        """Calculate coverage percentage within an agent's territory."""

        territory = self.get_agent_territory(agent_name)

        if not territory:
            return 0.0

        visited = self.coverage[agent_name].intersection(
            territory
        )

        return (len(visited) / len(territory)) * 100

    def calculate_total_coverage(self):
        """Calculate total campus coverage."""

        all_locations = set(
            self.campus.get_locations()
        )

        visited_locations = (
            self.coverage["Agent 1"]
            | self.coverage["Agent 2"]
        )

        if not all_locations:
            return 0.0

        return (
            len(visited_locations)
            / len(all_locations)
        ) * 100

    def display_coverage(self):
        print("\n=== TERRITORY COVERAGE ===")

        for agent_name in self.coverage:

            percentage = (
                self.calculate_coverage_percentage(
                    agent_name
                )
            )

            print(
                f"{agent_name}: "
                f"{percentage:.1f}% coverage"
            )

            print(
                f"Visited: "
                f"{sorted(self.coverage[agent_name])}"
            )

        print(
            f"\nTotal Campus Coverage: "
            f"{self.calculate_total_coverage():.1f}%"
        )

    # --------------------------------------------------
    # DESTINATION SELECTION
    # --------------------------------------------------

    def choose_territory_destination(
        self,
        agent,
        agent_name,
    ):
        """
        Select the highest-utility destination
        inside the agent's assigned territory.

        If no territory destination is available,
        fall back to the agent's normal utility decision.
        """

        destination, scores = (
            agent.choose_best_destination()
        )

        territory = self.get_agent_territory(
            agent_name
        )

        territory_scores = {
            location: score
            for location, score in scores.items()
            if location in territory
        }

        if territory_scores:
            return max(
                territory_scores,
                key=territory_scores.get,
            )

        return destination

    # --------------------------------------------------
    # PATROL STEP
    # --------------------------------------------------

    def patrol_step(self):

        self.step_count += 1

        print("\n======================================")
        print(
            f"       MULTI-AGENT PATROL STEP "
            f"{self.step_count}"
        )
        print("======================================")

        # -----------------------------
        # Agent 1 decision
        # -----------------------------

        destination_1 = (
            self.choose_territory_destination(
                self.agent_1,
                "Agent 1",
            )
        )

        # -----------------------------
        # Agent 2 decision
        # -----------------------------

        destination_2 = (
            self.choose_territory_destination(
                self.agent_2,
                "Agent 2",
            )
        )

        # -----------------------------
        # Avoid destination collision
        # -----------------------------

        if (
            destination_1 is not None
            and destination_2 is not None
            and destination_1 == destination_2
        ):

            print(
                f"\n⚠️ Both agents selected "
                f"{destination_1}."
            )

            # Get Agent 2's current utility scores
            _, agent_2_scores = (
                self.agent_2.choose_best_destination()
            )

            alternatives = {
                location: score
                for location, score
                in agent_2_scores.items()
                if (
                    location != destination_1
                    and location
                    in self.territories["Agent 2"]
                )
            }

            if alternatives:

                destination_2 = max(
                    alternatives,
                    key=alternatives.get,
                )

                print(
                    f"🔄 Agent 2 redirected to "
                    f"{destination_2}."
                )

        # -----------------------------
        # Move Agent 1
        # -----------------------------

        if destination_1 is not None:

            print(
                f"\n🤖 Agent 1 → "
                f"{destination_1}"
            )

            success = self.agent_1.move_to(
                destination_1
            )

            if success:
                self.update_coverage(
                    "Agent 1",
                    destination_1,
                )

        # -----------------------------
        # Move Agent 2
        # -----------------------------

        if destination_2 is not None:

            print(
                f"\n🤖 Agent 2 → "
                f"{destination_2}"
            )

            success = self.agent_2.move_to(
                destination_2
            )

            if success:
                self.update_coverage(
                    "Agent 2",
                    destination_2,
                )

        # Display coverage after every step
        self.display_coverage()

    # --------------------------------------------------
    # STATUS
    # --------------------------------------------------

    def display_status(self):

        print("\n======================================")
        print("       MULTI-AGENT SYSTEM STATUS")
        print("======================================")

        print("\n--- Agent 1 ---")
        self.agent_1.status()

        print("\n--- Agent 2 ---")
        self.agent_2.status()

        self.display_territories()
        self.display_coverage()


# ------------------------------------------------------
# TEST THE MULTI-AGENT SYSTEM
# ------------------------------------------------------

if __name__ == "__main__":

    campus = CampusEnvironment()

    system = MultiAgentPatrolSystem(campus)

    print("======================================")
    print("   AUTONOMOUS MULTI-AGENT PATROL")
    print("======================================")

    system.display_territories()

    print("\n\n========== INITIAL STATUS ==========")

    system.display_status()

    # Run multiple coordinated patrol steps
    for step in range(5):
        system.patrol_step()

    print("\n\n========== FINAL STATUS ==========")

    system.display_status()