import json 
 # Import random module
import random


# computerScience.json 隨機選資料
def main():
    file_path = "./computerScience.json"
    samples = {}
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        
        sample_size = 30
        # Randomly select 30 items from json_data
        selected = random.sample(json_data, sample_size)
        
        # Create samples dictionary with selected items
    samples = json.dumps(selected, indent=4, ensure_ascii=False)
    print(samples)
         



if __name__ == "__main__":
    main()
