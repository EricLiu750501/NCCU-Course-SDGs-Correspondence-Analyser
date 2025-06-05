
import json
import os

def merge_data(scholars: dict, append_data: dict) -> dict:
    for college, programs in append_data.items():
        if college not in scholars:
            scholars[college] = programs
        else:
            for program, people in programs.items():
                if program not in scholars[college]:
                    scholars[college][program] = people
                else:
                    # 合併 list，避免重複（依據 url 區分）
                    existing_urls = {person["url"] for person in scholars[college][program]}
                    for person in people:
                        if person["url"] not in existing_urls:
                            scholars[college][program].append(person)
    return scholars
    

# Get the directory of scholars_info files from the file path
file_path = "/Users/liuzihong/Desktop/Senior_Project/code/src/AH/scholars_info_0.json"
directory = os.path.dirname(file_path)
output_path = os.path.join(directory, "scholars_info_all.json")

# Initialize the merged data dictionary
merged_data = {}

# Merge scholars_info_0.json through scholars_info_4.json
for i in range(5):
    input_path = os.path.join(directory, f"scholars_info_{i}.json")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Merge departments and scholars
            merge_data(merged_data, data)
             
        print(f"Processed file: {input_path}")
    except Exception as e:
        print(f"Error processing file {input_path}: {e}")

# Write the merged data to the output file
with open(output_path, 'w', encoding='utf-8') as outfile:
    json.dump(merged_data, outfile, ensure_ascii=False, indent=2)
print(f"Merged data written to {output_path}")

