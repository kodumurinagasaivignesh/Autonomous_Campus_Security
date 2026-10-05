import os
import sys
import random
import io
from contextlib import redirect_stdout

# Allow Python to import files from the src folder.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from environment import CampusEnvironment
from random_patrol import RandomPatrolAgent
from fixed_patrol import FixedRoutePatrolAgent
from utility_agent import UtilityBasedPatrolAgent


# Number of trials for each patrol strategy.
NUM_TRIALS = 10

# Number of patrol decisions in each trial.
PATROL_STEPS = 10


def calculate_metrics(agent):
    """Calculate performance metrics for a completed patrol."""

    unique_areas = len(set(agent.patrol_history))

    total_visits = len(agent.patrol_history) - 1

    return {
        "distance": agent.total_distance,
        "unique_areas": unique_areas,
        "visits": total_visits,
        "final_battery": agent.battery,
    }


def run_random_patrol(seed):
    """Run one random patrol experiment."""

    random.seed(seed)

    campus = CampusEnvironment()

    agent = RandomPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    for _ in range(PATROL_STEPS):
        success = agent.patrol_once()

        if not success:
            break

    return calculate_metrics(agent)


def run_fixed_patrol():
    """Run one fixed-route patrol experiment."""

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

    for _ in range(PATROL_STEPS):
        success = agent.patrol_once()

        if not success:
            break

    return calculate_metrics(agent)


def run_utility_patrol():
    """Run one utility-based patrol experiment."""

    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    # Add simulated live security incidents.
    agent.incident_manager.create_incident(
        "Fire Alert",
        "Canteen",
        "Possible fire detected near the canteen.",
    )

    agent.incident_manager.create_incident(
        "Unauthorized Entry",
        "Main Gate",
        "Unauthorized person detected at the main entrance.",
    )

    for _ in range(PATROL_STEPS):
        success = agent.patrol_once()

        if not success:
            break

    return calculate_metrics(agent)


def average_results(results):
    """Calculate average values across multiple trials."""

    count = len(results)

    return {
        "distance": sum(r["distance"] for r in results) / count,
        "unique_areas": sum(r["unique_areas"] for r in results) / count,
        "visits": sum(r["visits"] for r in results) / count,
        "final_battery": sum(r["final_battery"] for r in results) / count,
    }


def display_results(all_results):
    """Display the final evaluation table."""

    print("\n")
    print("=" * 80)
    print("MULTI-TRIAL PATROL STRATEGY EVALUATION")
    print("=" * 80)

    print(f"\nNumber of trials per strategy: {NUM_TRIALS}")
    print(f"Patrol steps per trial: {PATROL_STEPS}")

    print("\nAverage Performance:")
    print("-" * 80)

    print(
        f"{'Strategy':<20}"
        f"{'Distance':<15}"
        f"{'Unique Areas':<15}"
        f"{'Total Visits':<15}"
        f"{'Final Battery':<15}"
    )

    print("-" * 80)

    for strategy, results in all_results.items():

        avg = average_results(results)

        print(
            f"{strategy:<20}"
            f"{avg['distance']:<15.2f}"
            f"{avg['unique_areas']:<15.2f}"
            f"{avg['visits']:<15.2f}"
            f"{avg['final_battery']:<15.2f}"
        )

    print("-" * 80)

    print("\nIndividual Trial Results:")
    print("-" * 80)

    for strategy, results in all_results.items():

        print(f"\n{strategy}")

        for index, result in enumerate(results, start=1):

            print(
                f"Trial {index:02d}: "
                f"Distance={result['distance']}, "
                f"Unique Areas={result['unique_areas']}, "
                f"Visits={result['visits']}, "
                f"Battery={result['final_battery']}"
            )


if __name__ == "__main__":

    print("=" * 80)
    print("STARTING MULTI-TRIAL PATROL EVALUATION")
    print("=" * 80)

    all_results = {
        "Random Patrol": [],
        "Fixed Route": [],
        "Utility Based": [],
    }

    # ---------------------------------------------------------
    # RANDOM PATROL
    # ---------------------------------------------------------

    print("\nRunning Random Patrol trials...")

    for trial in range(NUM_TRIALS):

        seed = 100 + trial

        # Hide detailed patrol output.
        output = io.StringIO()

        with redirect_stdout(output):
            result = run_random_patrol(seed)

        all_results["Random Patrol"].append(result)

    print("Random Patrol: 10 trials completed.")

    # ---------------------------------------------------------
    # FIXED ROUTE
    # ---------------------------------------------------------

    print("\nRunning Fixed Route trials...")

    for _ in range(NUM_TRIALS):

        output = io.StringIO()

        with redirect_stdout(output):
            result = run_fixed_patrol()

        all_results["Fixed Route"].append(result)

    print("Fixed Route: 10 trials completed.")

    # ---------------------------------------------------------
    # UTILITY BASED
    # ---------------------------------------------------------

    print("\nRunning Utility Based trials...")

    for _ in range(NUM_TRIALS):

        output = io.StringIO()

        with redirect_stdout(output):
            result = run_utility_patrol()

        all_results["Utility Based"].append(result)

    print("Utility Based: 10 trials completed.")

    # ---------------------------------------------------------
    # DISPLAY RESULTS
    # ---------------------------------------------------------

    display_results(all_results)

    print("\nEvaluation completed successfully.")