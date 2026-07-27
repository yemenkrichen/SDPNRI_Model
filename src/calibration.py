import json
import csv
from collections import defaultdict

transition_file = "boston_user_transitions.json"
timeseries_file = "compartment_timeseries.csv"
output_file = "calibrated_rates.csv"

allowed_transitions = {"S->D", "S->P", "S->N", "S->I","D->P", "D->N", "D->I","P->D", "P->N", "P->I","N->D", "N->P", "N->I"}

transition_counts = defaultdict(int)

with open(transition_file, "r", encoding="utf-8") as f:
    data = json.load(f)

for user, history in data.items():

    # All users without relevant activities will be ignored
    if history ==[]:
        continue
    for event in history:
        transition = event["transition"].replace(" ", "")

        if transition in allowed_transitions:
            transition_counts[transition] += 1
rows = []
with open(timeseries_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            "time": float(row["time"]),
            "S": int(row["S"]),
            "D": int(row["D"]),
            "P": int(row["P"]),
            "N": int(row["N"]),
            "R": int(row["R"]),
            "I": int(row["I"])
        })


person_time = {
    "S": 0,
    "D": 0,
    "P": 0,
    "N": 0,
    "I": 0
}


for i in range(len(rows)-1):

    dt = rows[i+1]["time"] - rows[i]["time"]

    # ignore zero-time jumps as they're contradictory with my data'
    if dt <= 0:
        continue

    for state in person_time:
        person_time[state] += rows[i][state] * dt

results = []

for transition in allowed_transitions:
    source, target = transition.split("->")
    count = transition_counts[transition]
    exposure = person_time[source]

    if exposure > 0:
        rate = count / exposure
    else:
        rate = 0

    results.append({
        "transition": transition,
        "events": count,
        "person_seconds": exposure,
        "rate_per_second": rate
    })

with open(output_file, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "transition",
            "events",
            "person_seconds",
            "rate_per_second"
        ]
    )
    writer.writeheader()
    writer.writerows(
        sorted(results, key=lambda x: x["transition"])
    )

print(f"Saved: {output_file}")

