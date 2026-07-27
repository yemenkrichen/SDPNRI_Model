import os
import json

base = "data/aug-rnr-data_full/bostonbombings"
categories = ["rumours", "non-rumours"]

out_lines = []

for category in categories:
    cat_path = os.path.join(base, category)
    folders = os.listdir(cat_path)
    for folder in folders:
        folder_path = os.path.join(cat_path, folder)
        if not os.path.isdir(folder_path):
            continue
        source_path = os.path.join(folder_path, "source-tweets")
        if not os.path.isdir(source_path):
            continue
        files = os.listdir(source_path)
        for file in files:
            if file.endswith('.json') and not file.startswith('._'):
                json_path = os.path.join(source_path, file)
                with open(json_path, 'r') as f:
                    data = json.load(f)

                if "retweeted_status" in data:
                    text = data["retweeted_status"].get("full_text", data["retweeted_status"].get("text", ""))
                else:
                    text = data.get("full_text", data.get("text", ""))

                text = text.replace("\n", " ").strip()
                line = folder + ' : ' + text
                print(line)
                out_lines.append(line)

with open("all_tweets.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines) + "\n")

print(f"\nDone. Extracted {len(out_lines)} tweets -> all_tweets.txt")
