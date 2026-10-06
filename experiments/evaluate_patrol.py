import os
import sys
import random
import io
import csv

from contextlib import redirect_stdout


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SRC_PATH = os.path.join(
    PROJECT_ROOT,
    "src"
)

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


from environment import CampusEnvironment
from random_patrol import RandomPatrolAgent
from fixed_patrol import FixedRoutePatrolAgent
from utility_agent import UtilityBasedPatrolAgent


# ============================================================
# EXPERIMENT SETTINGS
# ============================================================

NUM_TRIALS = 10
PATROL_STEPS = 10

RESULTS_DIR = os.path.join(
    PROJECT_ROOT,
    "results"
)

RESULTS_FILE = os.path.join(
    RESULTS_DIR,
    "patrol_results.csv"
)


# ============================================================
# METRICS
# ============================================================

def calculate_metrics(agent):
    """Calculate performance metrics for one patrol run."""

    unique_areas = len(
        set(agent.patrol_history)
    )

    total_visits = (
        len(agent.patrol_history) - 1
    )

    return {
        "distance": agent.total_distance,
        "unique_areas": unique_areas,
        "visits": total_visits,
        "final_battery": agent.battery,
    }


# ============================================================
# RANDOM PATROL
# ============================================================

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


# ============================================================
# FIXED ROUTE
# ============================================================

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


# ============================================================
# UTILITY-BASED PATROL
# ============================================================

def run_utility_patrol():
    """Run one utility-based patrol experiment."""

    campus = CampusEnvironment()

    agent = UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )

    # Simulated security incidents.
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


# ============================================================
# AVERAGE RESULTS
# ============================================================

def average_results(results):
    """Calculate average metrics across trials."""

    count = len(results)

    return {
        "distance":
            sum(
                r["distance"]
                for r in results
            ) / count,

        "unique_areas":
            sum(
                r["unique_areas"]
                for r in results
            ) / count,

        "visits":
            sum(
                r["visits"]
                for r in results
            ) / count,

        "final_battery":
            sum(
                r["final_battery"]
                for r in results
            ) / count,
    }


# ============================================================
# SAVE RESULTS
# ============================================================

def save_results(all_results):
    """Save every trial result to CSV."""

    os.makedirs(
        RESULTS_DIR,
        exist_ok=True,
    )

    with open(
        RESULTS_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Strategy",
            "Trial",
            "Distance",
            "Unique Areas",
            "Total Visits",
            "Final Battery",
        ])

        for strategy, results in all_results.items():

            for index, result in enumerate(
                results,
                start=1,
            ):

                writer.writerow([
                    strategy,
                    index,
                    result["distance"],
                    result["unique_areas"],
                    result["visits"],
                    result["final_battery"],
                ])

    print(
        f"\nResults saved to:"
        f"\n{RESULTS_FILE}"
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(all_results):

    print("\n")

    print("=" * 80)
    print(
        "MULTI-TRIAL PATROL STRATEGY EVALUATION"
    )
    print("=" * 80)

    print(
        f"\nNumber of trials per strategy: "
        f"{NUM_TRIALS}"
    )

    print(
        f"Patrol steps per trial: "
        f"{PATROL_STEPS}"
    )

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


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 80)
    print(
        "STARTING MULTI-TRIAL PATROL EVALUATION"
    )
    print("=" * 80)


    all_results = {
        "Random Patrol": [],
        "Fixed Route": [],
        "Utility Based": [],
    }


    # --------------------------------------------------------
    # RANDOM PATROL
    # --------------------------------------------------------

    print(
        "\nRunning Random Patrol trials..."
    )

    for trial in range(NUM_TRIALS):

        seed = 100 + trial

        output = io.StringIO()

        with redirect_stdout(output):

            result = run_random_patrol(
                seed
            )

        all_results[
            "Random Patrol"
        ].append(result)

    print(
        "Random Patrol: "
        f"{NUM_TRIALS} trials completed."
    )


    # --------------------------------------------------------
    # FIXED ROUTE
    # --------------------------------------------------------

    print(
        "\nRunning Fixed Route trials..."
    )

    for _ in range(NUM_TRIALS):

        output = io.StringIO()

        with redirect_stdout(output):

            result = run_fixed_patrol()

        all_results[
            "Fixed Route"
        ].append(result)

    print(
        "Fixed Route: "
        f"{NUM_TRIALS} trials completed."
    )


    # --------------------------------------------------------
    # UTILITY BASED
    # --------------------------------------------------------

    print(
        "\nRunning Utility Based trials..."
    )

    for _ in range(NUM_TRIALS):

        output = io.StringIO()

        with redirect_stdout(output):

            result = run_utility_patrol()

        all_results[
            "Utility Based"
        ].append(result)

    print(
        "Utility Based: "
        f"{NUM_TRIALS} trials completed."
    )


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    display_results(
        all_results
    )


    # --------------------------------------------------------
    # SAVE CSV
    # --------------------------------------------------------

    save_results(
        all_results
    )


    print(
        "\nEvaluation completed successfully."
    )