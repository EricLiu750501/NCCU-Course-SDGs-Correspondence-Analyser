import json 
import glob
import os

def load_all_json_data(directory_path, course_ids_filter=None):
    """Load all JSON files in the given directory, optionally filtered by course IDs."""
    json_files = glob.glob(os.path.join(directory_path, "*.json"))
    data_list = []
    
    for file_path in json_files:
        file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
        if course_ids_filter and file_name_without_ext not in course_ids_filter:
            continue # Skip if not in filter list

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                data["file_path"] = file_path # Add file_path to the data
                data_list.append(data)
                # print(f"Loaded: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return data_list


data_lst = load_all_json_data("./")
# print(data_lst[0])

c = 0
for d in data_lst:
    try:
        if d["gpt_answer"] == {}:
            c += 1
    
    except KeyError:
        pass

    # print(d.items())
    # if d["gpt_answer"] == {}:
    #     c+=1

print(c)



