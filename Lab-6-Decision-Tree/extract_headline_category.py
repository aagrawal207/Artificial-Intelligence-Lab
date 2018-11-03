import json


def extract_headline_category():
    headline_category = []
    try:
        input_file = open('./News_Category_Dataset.json')
        input_data = input_file.readlines()
        input_file.close()
        for json_object in input_data:
            data = json.loads(json_object)
            headline_category.append((data['headline'], data['category']))
        return headline_category
    except IOError:
        print("ERROR : IO ERROR occurred while opening file")
        exit(0)
