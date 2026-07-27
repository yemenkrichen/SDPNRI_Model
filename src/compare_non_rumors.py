import os
import json
nonrumors ="data/aug-rnr-data_full/bostonbombings/non-rumours"
folders = os.listdir(nonrumors)
for folder in folders:
    folder_path =os.path.join(nonrumors,folder)
    if not os.path.isdir(folder_path):
        continue
    source_path = os.path.join(folder_path,"source-tweets")
    files = os.listdir(source_path)
    for file in files:
        if file.endswith('.json') and not file.startswith('._'):
            json_path = os.path.join(source_path, file)
            with open(json_path,'r') as f:
                data= json.load(f)
            if "retweeted_status" in data:
                text = data["retweeted_status"]["full_text"]
            else:
                text=data["full_text"]
                
            print(folder+ ' : ' + text)
            

