import sys
from pathlib import Path

# Allow this file to import modules from the src folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from environment import CampusEnvironment
from random_patrol import RandomPatrolAgent
from fixed_patrol import FixedRoutePatrolAgent
from utility_agent import UtilityBasedPatrolAgent


def calculate_metrics(agent):
    """Calculate basic performance metrics for a patrol agent."""

    unique_locations = len(set(agent.patrol_history))

    return {
        "total_distance": agent.total_distance,
        "locations_visited": unique_locations,
        "total_visits": len(agent.patrol_history),
        "final_battery": agent.battery,
    }


def run_random_patrol(steps=10):
    """Run the random patrol strategy."""

    campus = CampusEnvironment()

    agent = RandomPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    for _ in range(steps):
        if not agent.patrol_once():
            break

    return calculate_metrics(agent)


def run_fixed_patrol(steps=10):
    """Run the fixed-route patrol strategy."""

    campus = CampusEnvironment()

    route = [
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
        route=route,
        start_location="Main Gate",
        battery=100,
    )

    for _ in range(steps):
        if not agent.patrol_once():
            break

    return calculate_metrics(agent)


def run_utility_patrol(steps=10):
    """Run the utility-based patrol strategy."""

    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
        initial_charge=100,
    )

    # Add a simulated security incident.
    agent.incident_manager.create_incident(
        "Fire Alert",
        "Canteen",
        "Simulated fire alert for evaluation.",
    )

    for _ in range(steps):
        if not agent.patrol_once():
            break

    return calculate_metrics(agent)


def display_results(results):
    """Display comparison results."""

    print("\n" + "=" * 70)
    print("PATROL STRATEGY EVALUATION")
    print("=" * 70)

    print(
        f"{'Strategy':<20}"
        f"{'Distance':<15}"
        f"{'Unique Areas':<15}"
        f"{'Total Visits':<15}"
        f"{'Final Battery':<15}"
    )

    print("-" * 80)

    for strategy, metrics in results.items():
        print(
            f"{strategy:<20}"
            f"{metrics['total_distance']:<15}"
            f"{metrics['locations_visited']:<15}"
            f"{metrics['total_visits']:<15}"
            f"{metrics['final_battery']:<15}"
        )


if __name__ == "__main__":
    results = {
        "Random Patrol": run_random_patrol(),
        "Fixed Route": run_fixed_patrol(),
        "Utility Based": run_utility_patrol(),
    }

    display_results(results)
    