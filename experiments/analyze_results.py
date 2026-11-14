
import pandas as pd

# -----------------------------------------
# PATROL STRATEGY RESULTS
# -----------------------------------------

patrol = pd.read_csv("results/patrol_results.csv")

patrol_summary = (
    patrol.groupby("Strategy")
    .agg(
        Average_Distance=("Distance", "mean"),
        Average_Unique_Areas=("Unique Areas", "mean"),
        Average_Total_Visits=("Total Visits", "mean"),
        Average_Final_Battery=("Final Battery", "mean"),
    )
    .round(2)
)

# Calculate coverage using 9 campus locations.
patrol_summary["Campus_Coverage_Percent"] = (
    patrol_summary["Average_Unique_Areas"] / 9 * 100
).round(2)

print("\nPATROL STRATEGY COMPARISON")
print(patrol_summary.to_markdown())

# -----------------------------------------
# MULTI-AGENT RESULTS
# -----------------------------------------

multi = pd.read_csv("results/multi_agent_results.csv")

multi_summary = multi.set_index("Metric")["Average"]

print("\nMULTI-AGENT RESULTS")
print(multi_summary.to_markdown())

# -----------------------------------------
# EXPORT TABLES
# -----------------------------------------

patrol_summary.to_csv(
    "results/patrol_summary.csv"
)

multi_summary.to_csv(
    "results/multi_agent_summary.csv"
)

print("\nSummary CSV files created.")
