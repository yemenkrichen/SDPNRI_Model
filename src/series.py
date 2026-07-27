import json
import csv

transition = "boston_user_transitions.json"
output = "compartment_timeseries.csv"
restrained = 12 * 60 *60      # 12 hours =43200 seconds

with open(transition, "r") as f:
    data = json.load(f)
events = []
counts = {
    "S": 0,
    "D": 0,
    "P": 0,
    "N": 0,
    "R": 0,
    "I": 0
}
for user, history in data.items():
    if history == []: #check if the users are relevant
        continue
    history = sorted(history,key=lambda x: x["seconds_since_global_t0"])
    first_transition = history[0]["transition"].replace(" ", "")
    initial_state = first_transition.split("->")[0]
    counts[initial_state] += 1
    for event in history:
        events.append({
            "time": event["seconds_since_global_t0"],
            "transition": event["transition"].replace(" ", "")
        })

    last_event = history[-1]
    last_time = last_event["seconds_since_global_t0"]
    last_transition = last_event["transition"].replace(" ", "")
    final_state = last_transition.split("->")[1]
    if final_state not in ("I", "R"):
        events.append({
            "time": last_time + restrained,
            "transition": f"{final_state}->R"
        })
events.sort(key=lambda x: x["time"])
rows = []

rows.append([
    0,
    counts["S"],
    counts["D"],
    counts["P"],
    counts["N"],
    counts["R"],
    counts["I"]
])

for event in events:
    source, target = event["transition"].split("->")
    counts[source] -= 1
    counts[target] += 1
    rows.append([
        event["time"],
        counts["S"],
        counts["D"],
        counts["P"],
        counts["N"],
        counts["R"],
        counts["I"]
    ])

with open(output, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "time",
        "S",
        "D",
        "P",
        "N",
        "R",
        "I"
    ])
    writer.writerows(rows)
print(f"Saved {output}")
