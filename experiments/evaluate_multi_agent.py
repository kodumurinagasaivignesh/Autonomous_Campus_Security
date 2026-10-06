import csv
import io
import os
import random
import sys
from contextlib import redirect_stdout


# Allow imports from the src directory
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


from environment import CampusEnvironment
from multi_agent import MultiAgentPatrolSystem


# --------------------------------------------------
# EXPERIMENT SETTINGS
# --------------------------------------------------

NUM_TRIALS = 10
PATROL_STEPS = 10

RESULTS_DIR = os.path.join(
    PROJECT_ROOT,
    "results",
)

RESULTS_FILE = os.path.join(
    RESULTS_DIR,
    "multi_agent_results.csv",
)


# --------------------------------------------------
# RUN ONE TRIAL
# --------------------------------------------------

def run_trial(seed):
    """
    Run one multi-agent patrol trial
    and collect performance metrics.
    """

    random.seed(seed)

    campus = CampusEnvironment()

    system = MultiAgentPatrolSystem(campus)

    # Suppress console output during experiment
    with redirect_stdout(io.StringIO()):

        for _ in range(PATROL_STEPS):
            system.patrol_step()

    # ----------------------------------------------
    # Coverage metrics
    # ----------------------------------------------

    total_coverage = (
        system.calculate_total_coverage()
    )

    agent_1_coverage = (
        system.calculate_coverage_percentage(
            "Agent 1"
        )
    )

    agent_2_coverage = (
        system.calculate_coverage_percentage(
            "Agent 2"
        )
    )

    # ----------------------------------------------
    # Movement metrics
    # ----------------------------------------------

    total_distance = (
        system.agent_1.total_distance
        + system.agent_2.total_distance
    )

    # ----------------------------------------------
    # Battery metrics
    # ----------------------------------------------

    final_battery = (
        system.agent_1.battery
        + system.agent_2.battery
    )

    average_battery = final_battery / 2

    # ----------------------------------------------
    # Overlap metric
    # ----------------------------------------------

    agent_1_locations = system.coverage["Agent 1"]
    agent_2_locations = system.coverage["Agent 2"]

    overlapping_locations = (
        agent_1_locations
        & agent_2_locations
    )

    overlap_count = len(
        overlapping_locations
    )

    return {
        "total_coverage": total_coverage,
        "agent_1_coverage": agent_1_coverage,
        "agent_2_coverage": agent_2_coverage,
        "total_distance": total_distance,
        "average_battery": average_battery,
        "overlap_count": overlap_count,
    }


# --------------------------------------------------
# RUN EXPERIMENT
# --------------------------------------------------

def main():

    print("======================================")
    print("   MULTI-AGENT PERFORMANCE EVALUATION")
    print("======================================")

    print(f"\nTrials: {NUM_TRIALS}")
    print(f"Patrol steps per trial: {PATROL_STEPS}")

    results = []

    for trial in range(NUM_TRIALS):

        metrics = run_trial(
            seed=trial + 1
        )

        results.append(metrics)

        print(
            f"\nTrial {trial + 1}: "
            f"Coverage = "
            f"{metrics['total_coverage']:.2f}% | "
            f"Distance = "
            f"{metrics['total_distance']:.2f} | "
            f"Battery = "
            f"{metrics['average_battery']:.2f}"
        )

    # --------------------------------------------------
    # CALCULATE AVERAGES
    # --------------------------------------------------

    average_total_coverage = (
        sum(
            result["total_coverage"]
            for result in results
        )
        / len(results)
    )

    average_agent_1_coverage = (
        sum(
            result["agent_1_coverage"]
            for result in results
        )
        / len(results)
    )

    average_agent_2_coverage = (
        sum(
            result["agent_2_coverage"]
            for result in results
        )
        / len(results)
    )

    average_distance = (
        sum(
            result["total_distance"]
            for result in results
        )
        / len(results)
    )

    average_battery = (
        sum(
            result["average_battery"]
            for result in results
        )
        / len(results)
    )

    average_overlap = (
        sum(
            result["overlap_count"]
            for result in results
        )
        / len(results)
    )

    # --------------------------------------------------
    # DISPLAY SUMMARY
    # --------------------------------------------------

    print("\n======================================")
    print("          AVERAGE RESULTS")
    print("======================================")

    print(
        f"\nTotal Campus Coverage: "
        f"{average_total_coverage:.2f}%"
    )

    print(
        f"Agent 1 Territory Coverage: "
        f"{average_agent_1_coverage:.2f}%"
    )

    print(
        f"Agent 2 Territory Coverage: "
        f"{average_agent_2_coverage:.2f}%"
    )

    print(
        f"Average Total Distance: "
        f"{average_distance:.2f}"
    )

    print(
        f"Average Battery Remaining: "
        f"{average_battery:.2f}"
    )

    print(
        f"Average Overlap Count: "
        f"{average_overlap:.2f}"
    )

    # --------------------------------------------------
    # SAVE CSV
    # --------------------------------------------------

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

        writer.writerow(
            [
                "Metric",
                "Average",
            ]
        )

        writer.writerow(
            [
                "Total Campus Coverage (%)",
                round(
                    average_total_coverage,
                    2,
                ),
            ]
        )

        writer.writerow(
            [
                "Agent 1 Territory Coverage (%)",
                round(
                    average_agent_1_coverage,
                    2,
                ),
            ]
        )

        writer.writerow(
            [
                "Agent 2 Territory Coverage (%)",
                round(
                    average_agent_2_coverage,
                    2,
                ),
            ]
        )

        writer.writerow(
            [
                "Average Total Distance",
                round(
                    average_distance,
                    2,
                ),
            ]
        )

        writer.writerow(
            [
                "Average Battery Remaining",
                round(
                    average_battery,
                    2,
                ),
            ]
        )

        writer.writerow(
            [
                "Average Overlap Count",
                round(
                    average_overlap,
                    2,
                ),
            ]
        )

    print(
        f"\n✅ Results saved to:"
        f"\n{RESULTS_FILE}"
    )


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()