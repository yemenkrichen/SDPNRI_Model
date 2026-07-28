import json

with open("boston_users_database.json", "r", encoding="utf-8") as f:
    data = json.load(f)

seen = set()

for user, activities in data.items():
    for act in activities:
        tweet_text = act.get("text")

        if tweet_text and tweet_text not in seen:
            print(tweet_text)
            seen.add(tweet_text)
