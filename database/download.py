import json
import os
import requests
from constants import *
from database.constants import BASAL_JSON, BASAL_PATH, BASAL_REQUEST

def get_isic_json(request, json_file):
    json_data = requests.get(request).json()
    json_to_save = json_data
    print("First json file downloaded...")

    count = 1
    while json_data["next"]: 
        request = json_data["next"]
        json_data = requests.get(request).json()
        for item in json_data['results']:
            json_to_save["results"].append(item)
        print(count, "Json downloaded...Total of ",len(json_to_save['results']), " images" )
        count += 1
    

    json_file = open(json_file,'w', encoding='utf-8')   
    json.dump(json_to_save, json_file, ensure_ascii=False, indent=4)
    json_file.close()
    
def get_isic_files(json_file,path):
    # Opening JSON file
    f = open(json_file)
    data = json.load(f)
    results = data['results']

    try:
        os.mkdir(path)
    except:
        pass

    for i in range(len(results)):
        image = results[i]
        image_path = path + "/" + image["isic_id"] + ".png"

        if not os.path.exists(image_path):
            try:
                files = image['files']['full']
                url = files['url']
                plot = requests.get(url,timeout=5)
                content = plot.content
                print(i + 1, image_path)
                with open(image_path, 'wb') as file:
                    file.write(content)
            except TimeoutError:
                print(url)

    f.close()



