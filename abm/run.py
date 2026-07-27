import csv
import json
import random
import matplotlib.pyplot as plt
import pandas as pd
from model import SDPNRIModel

random.seed(42)

with open("boston_users_database.json") as f:
    user_timelines = json.load(f)

model = SDPNRIModel(user_timelines)
results = []

initial_counts = model.get_state_counts()
results.append(
    {
        "time_step": 0,
        "time_hours": 0,
        "time_seconds": 1,
        "S": initial_counts["S"],
        "D": initial_counts["D"],
        "P": initial_counts["P"],
        "N": initial_counts["N"],
        "R": initial_counts["R"],
        "I": initial_counts["I"],
    }
)

for step_idx in range(1, 361):
    model.step()
    counts = model.get_state_counts()

    row = {
        "time_step": model.step_count,
        "time_hours": model.step_count,
        "time_seconds": model.step_count * 3600,
        "S": counts["S"],
        "D": counts["D"],
        "P": counts["P"],
        "N": counts["N"],
        "R": counts["R"],
        "I": counts["I"],
    }
    results.append(row)

csv_filename = "abm_results.csv"
with open(csv_filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

df = pd.DataFrame(results)

plt.figure(figsize=(12, 6))

plt.plot(
    df["time_seconds"],
    df["S"],
    label="S (Susceptible)",
    color="#7f7f7f",
    linestyle="--",
)
plt.plot(
    df["time_seconds"], df["D"], label="D (Doubtful)", color="#e69f00", linewidth=1.5
)
plt.plot(
    df["time_seconds"],
    df["P"],
    label="P (Positively Infected)",
    color="#d55e00",
    linewidth=1.5,
)
plt.plot(
    df["time_seconds"],
    df["N"],
    label="N (Negatively Infected)",
    color="#cc79a7",
    linewidth=1.5,
)
plt.plot(
    df["time_seconds"],
    df["I"],
    label="I (Immune - Debunkers)",
    color="#009e73",
    linewidth=1.5,
)
plt.plot(
    df["time_seconds"],
    df["R"],
    label="R (Restrained - quiet >43200s)",
    color="#0072b2",
    linewidth=1.5,
)

plt.xscale("log")
plt.xlim(100, 600000)
plt.ylim(-25, 510)

plt.title(
    "SDPNRI Compartment Dynamics Over Time (ABM Simulation)",
    fontsize=13,
    fontweight="bold",
)
plt.xlabel("Seconds Since Global $t_0$", fontsize=11)
plt.ylabel("Number of Users", fontsize=11)
plt.grid(True, which="both", linestyle=":", alpha=0.5)

plt.legend(loc="upper right", frameon=True, shadow=True)

plt.tight_layout()
plt.savefig("sdpnri_cascade_plot.png", dpi=300)
plt.close()
