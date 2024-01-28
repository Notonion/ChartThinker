import json

def remove_duplicates(json_data):
    unique_ids = set()
    unique_data = []

    for item in json_data:
        item_id = item['id']
        if item_id not in unique_ids:
            unique_ids.add(item_id)
            unique_data.append(item)

    return unique_data

def compare_json(a_data, b_data):
    a_ids = set(item['id'] for item in a_data)
    b_ids = set(item['id'] for item in b_data)

    missing_elements = [item for item in a_data if item['id'] not in b_ids]

    return missing_elements

def generate_c_json(missing_elements):
    with open('c.json', 'w',encoding='utf-8') as outfile:
        json.dump(missing_elements, outfile, indent=2)

# read a.json and b.json
with open('a.json', 'r',encoding='utf-8') as a_file, open('b.json', 'r',encoding='utf-8') as b_file:
    a_json_data = json.load(a_file)
    b_json_data = json.load(b_file)


b_unique_data = remove_duplicates(b_json_data)


missing_elements = compare_json(a_json_data, b_unique_data)

# generate c.json file
generate_c_json(missing_elements)

