import os
import shutil
data_path = "data/aug-rnr-data_full/bostonbombings/non-rumours"

girl_rumor = {
    "323978115728699393", "323958486369202177", "323988065494368259", "324081982361436160"
}
correct_news ={
    "324040568705519616", "324044455336349696"
}

keep = girl_rumor.union(correct_news)
for folder in os.listdir(data_path):
    folder_path = os.path.join(data_path, folder)
    if os.path.isdir(folder_path):
        if folder not in keep:
            shutil.rmtree(folder_path)
    elif os.path.isfile(folder_path):
        os.remove(folder_path)
        
