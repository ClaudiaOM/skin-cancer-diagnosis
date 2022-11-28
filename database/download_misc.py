import json
import os
import requests


seborrheic_keratosis_requests = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22seborrheic%20keratosis%22"
pigmented_benign_keratosis_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22pigmented%20benign%20keratosis%22"
actinic_keratosis_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22actinic%20keratosis%22"
solar_lentigo_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22solar%20lentigo%22"
vascular_lesion_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22vascular%20lesion%22"
dermatofibroma_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22dermatofibroma%22"
lentigo_nos_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22lentigo%20NOS%22"
lentigo_simplex_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22lentigo%20simplex%22"
lichenoid_keratinosis_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22lichenoid%20keratinosis%22"
neurofibroma_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3Aneurofibroma"
acrochordon_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3Aacrochordon"
scar_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3Ascar"
nevus_request = "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3Anevus"

REQUESTS = ["https://api.isic-archive.com/api/v2/images/search/?limit=2500&query=diagnosis%3A%22squamous%20cell%20carcinoma%22%20AND%20image_type%3Adermoscopic",
            "https://api.isic-archive.com/api/v2/images/search/?cursor=cD0yMDE2LTExLTE1KzIyJTNBMzklM0EwMC43NDEwMDAlMkIwMCUzQTAw&query=image_type%3Adermoscopic+AND+diagnosis%3A%22seborrheic+keratosis%22",
            "https://api.isic-archive.com/api/v2/images/search/?query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22pigmented%20benign%20keratosis%22",
            "https://api.isic-archive.com/api/v2/images/search/?cursor=cD0yMDE4LTAzLTE5KzAxJTNBNDMlM0E1Mi43NDAwMDAlMkIwMCUzQTAw&query=image_type%3Adermoscopic+AND+diagnosis%3A%22pigmented+benign+keratosis%22",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22actinic%20keratosis%22",
            "https://api.isic-archive.com/api/v2/images/search/?cursor=cD0yMDE4LTAzLTE5KzAxJTNBMzYlM0EyNS42ODQwMDAlMkIwMCUzQTAw&query=image_type%3Adermoscopic+AND+diagnosis%3A%22actinic+keratosis%22",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22solar%20lentigo%22",
            "https://api.isic-archive.com/api/v2/images/search/?cursor=cD0yMDIyLTA2LTA5KzE4JTNBNTIlM0EzMS44ODUyNjUlMkIwMCUzQTAw&query=image_type%3Adermoscopic+AND+diagnosis%3A%22solar+lentigo%22",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22vascular%20lesion%22",
            "https://api.isic-archive.com/api/v2/images/search/?cursor=cD0yMDE4LTAzLTE5KzAxJTNBMzQlM0ExNC4xMzIwMDAlMkIwMCUzQTAw&query=image_type%3Adermoscopic+AND+diagnosis%3A%22vascular+lesion%22",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22dermatofibroma%22",
            "https://api.isic-archive.com/api/v2/images/search/?cursor=cD0yMDE4LTAzLTE5KzAxJTNBMzElM0E1NC42OTQwMDAlMkIwMCUzQTAw&query=image_type%3Adermoscopic+AND+diagnosis%3Adermatofibroma",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22lentigo%20NOS%22",
            "https://api.isic-archive.com/api/v2/images/search/?cursor=cD0yMDE1LTA2LTI2KzE0JTNBMzUlM0E0MC40MTEwMDAlMkIwMCUzQTAw&query=image_type%3Adermoscopic+AND+diagnosis%3A%22lentigo+NOS%22",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22lentigo%20simplex%22",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22lichenoid%20keratinosis%22",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3Aneurofibroma",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3Aacrochordon",
            "https://api.isic-archive.com/api/v2/images/search/?limit=300&query=image_type%3Adermoscopic%20AND%20diagnosis%3Ascar",
            "https://api.isic-archive.com/api/v2/images/search/?query=image_type%3Adermoscopic%20AND%20diagnosis%3A%22nevus%22",
            "https://api.isic-archive.com/api/v2/images/search/?cursor=cD0yMDIyLTA2LTA5KzE4JTNBNTIlM0EzOC4wNzk2ODIlMkIwMCUzQTAw&query=image_type%3Adermoscopic+AND+diagnosis%3A%22nevus%22"]

MISC_JSON = "misc.json"
MISC_PATH = "misc_images"

def get_isic_json():
    count = 1
    json_to_save = {"results":[]}
    for request in REQUESTS:
        print("Downloading json ", count, "...")
        json_data = requests.get(request).json()
        print(len(json_data['results']))
        for item in json_data['results']:
            json_to_save["results"].append(item)
        print("Json downloaded...Total of ",len(json_to_save['results']), " images" )
        count += 1
    
    json_file = open(MISC_JSON,'w', encoding='utf-8')   
    json.dump(json_to_save, json_file, ensure_ascii=False, indent=4)
    json_file.close()
    
def get_isic_files():
    # Opening JSON file
    f = open(MISC_JSON)
    data = json.load(f)
    results = data['results']

    try:
        os.mkdir(MISC_PATH)
    except:
        pass

    for i in range(len(results)):
        image = results[i]
        image_path = MISC_PATH + "/" + image["isic_id"] + ".png"

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

get_isic_json()
get_isic_files()

