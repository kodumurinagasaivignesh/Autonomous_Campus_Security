
import os
import pandas as pd
import matplotlib.pyplot as plt

# Read experiment data
df = pd.read_csv("results/patrol_results.csv")

# Output folder
output_dir = "docs/images"
os.makedirs(output_dir, exist_ok=True)

# Calculate averages
summary = (
    df.groupby("Strategy")
    .agg(
        Distance=("Distance", "mean"),
        Unique_Areas=("Unique Areas", "mean"),
        Final_Battery=("Final Battery", "mean"),
    )
    .round(2)
)

# 1. Average patrol distance
plt.figure()
summary["Distance"].plot(kind="bar")
plt.title("Average Patrol Distance by Strategy")
plt.xlabel("Patrol Strategy")
plt.ylabel("Average Distance")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(
    os.path.join(output_dir, "patrol_distance.png"),
    dpi=300
)
plt.close()

# 2. Unique areas covered
plt.figure()
summary["Unique_Areas"].plot(kind="bar")
plt.title("Average Unique Areas Covered")
plt.xlabel("Patrol Strategy")
plt.ylabel("Unique Areas")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(
    os.path.join(output_dir, "unique_areas.png"),
    dpi=300
)
plt.close()

# 3. Remaining battery
plt.figure()
summary["Final_Battery"].plot(kind="bar")
plt.title("Average Final Battery")
plt.xlabel("Patrol Strategy")
plt.ylabel("Battery Remaining")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(
    os.path.join(output_dir, "final_battery.png"),
    dpi=300
)
plt.close()

print("Charts saved in docs/images/")
