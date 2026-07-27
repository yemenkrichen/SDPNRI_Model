import os
import json
from datetime import datetime

p="data/aug-rnr-data_full/bostonbombings"
subs = ["rumours","non-rumours"]
res ={}

def parse_time(s):
    try:
        return datetime.strptime(s,"%a %b %d %H:%M:%S +0000 %Y")
    except:
        return None

for sub in subs:
    sub_path = os.path.join(p,sub)
    for thread in os.listdir(sub_path):
        t_dir = os.path.join(sub_path,thread)
        if not os.path.isdir(t_dir) or thread.startswith("."):
            continue
        t0 = None
        orig_user = None
        src_f = None
        res[thread] = []
        src_dir= os.path.join(t_dir,"source-tweets")
        files= [f for f in os.listdir(src_dir) if f.endswith(".json") and not f.startswith(".")]
        if files:
            src_f = os.path.join(src_dir,files[0])
            
        if src_f and os.path.exists(src_f):
            try:
                with open(src_f,'r',encoding='utf-8',errors='ignore') as f:
                    js = json.load(f)

                    is_rt = "retweeted_status" in js
                    tgt = js.get("retweeted_status",js)
                    orig_user = tgt.get("user",{}).get("id_str")
                    t0= parse_time(tgt.get("created_at"))
                    txt = tgt.get("full_text") or tgt.get("text","")
                    rc= tgt.get("retweet_count",0)
                    fc= tgt.get("favorite_count",0)
                if orig_user and t0:
                    res[thread].append(
                           {
                                "tweet_id": tgt.get("id_str"),
                                "user_id": orig_user,
                                "parent_user_id": None,
                                "type": "source",
                                "created_at": t0,
                                "text": txt,
                                "seconds_since_t0": 0.0,
                                "retweet_count": rc,
                                "favorite_count": fc
                            }
                        )
                    if is_rt:
                        rt_t = parse_time(js.get("created_at"))
                        rt_u = js.get("user",{}).get("id_str")
                        if rt_t and rt_u:
                            
                            res[thread].append(
                                {
                                    "tweet_id": js.get("id_str"),
                                    "user_id": rt_u,
                                    "parent_user_id": orig_user,
                                    "type": "retweet",
                                    "created_at": rt_t,
                                    "text": js.get("full_text") or js.get("text",""),
                                    "seconds_since_t0": (rt_t - t0).total_seconds(),
                                    "retweet_count": js.get("retweet_count",0),
                                    "favorite_count": js.get("favorite_count",0)
                                }
                            )
            except Exception as e:
                print(f"error on {thread}: {e}")
                continue
                
        rx_dir = os.path.join(t_dir,"reactions")
        if os.path.exists(rx_dir):
            for file in os.listdir(rx_dir):
                if not file.endswith(".json") or file.startswith("._"):
                    continue
                    
                r_p = os.path.join(rx_dir,file)
                with open(r_p,'r',encoding='utf-8',errors='ignore') as f:
                    r_js = json.load(f)
                    ru = r_js.get("user",{}).get("id_str")
                    rt = parse_time(r_js.get("created_at"))
                    r_txt = r_js.get("full_text") or r_js.get("text","")
                    
                    if ru and rt and t0:
                        diff = (rt - t0).total_seconds()
                        r_type = "retweet" if "retweeted_status" in r_js else "reply"
                        
                        action_data = {
                            "tweet_id": r_js.get("id_str"),
                            "user_id": ru,
                            "parent_user_id": r_js.get("in_reply_to_user_id_str") or orig_user,
                            "type": r_type,
                            "created_at": rt,
                            "text": r_txt,
                            "seconds_since_t0": diff,
                            "favorite_count": r_js.get("favorite_count",0)
                        }
                        res[thread].append(action_data)
                        
        res[thread] = sorted(res[thread],key=lambda x: x["seconds_since_t0"])
with open("bostonbombings_clean.json","w",encoding="utf-8") as out:
    json.dump(res,out,indent=4,default=str)

print("done")
