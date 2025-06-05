from LLMs import prompts, ask
from AH.reader_scholar import reader
import os
from ASJC_code.getASJC import ASJC
import random
import json
import re
import sys
import glob
import shutil

def code_college_mapping(college:str):
    dict = {
        'College of Social Science': "Social Sciences",
        'College of Liberal Arts':"Arts and Humanities",
        'Affiliated Centers': "Multidisciplinary",
        'College of Commerce':"Business, Management, and Accounting",
        'College of Education':"Social Sciences",
        'College of Informatics':"Computer Science",

    }
    if dict.get(college) is None:
        # print("Error: " + college + " not in dict")
        return None
    return dict[college]

def extract_json(text:str) -> dict:
    code_blocks = re.findall(r'```json(.*?)```', text, re.DOTALL | re.IGNORECASE) 
    if code_blocks:
        try:
            return json.loads(code_blocks[0])
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
    return {}

def extract_score(dic:dict) -> list:
    l = []
    for key, value in dic.items():
        l.append(value['score'])
    return [float(item) for item in l]


def read_multiline():
    print("Paste abstract, then press Ctrl+D (Linux/macOS) or Ctrl+Z + Enter (Windows):")
    return sys.stdin.read()

def start_asking(mode:str, ele:dict):
    print("-" * 20, {mode}, "-" * 20)
    title = ele['title']
    author = {
        "college": ele['college'],
        'department': ele['department'],
        "expertise": ele['expertise']
    }
    
    input_abstract = ""
    if "Abstract" in mode:
        print(ele['url'])
        print("title:", title)
        input_abstract = input("Get abstract (Y/N)")
        if input_abstract == "Y":
            with open("abstract_input.txt", "r", encoding="utf-8") as f:
                input_abstract = f.read()
        else:
            return "結束"
        print("\n Get abstract\n")

    input_keywords = ""
    if "Keywords" in mode:
        print(ele['url'])
        print("title:", title)
        input_keywords = input("Get keywords (Y/N)")
        if input_keywords == "Y":
            with open("keywords_input.txt", "r", encoding="utf-8") as f:
                input_keywords = f.read()
        else:
            return "結束"
        print("\n Get keywords\n")


    domain = code_college_mapping(author['college'])
    if domain:
        subdomain = asjc.subDomains(domain)
        p = prompts.prompts(subdomain)
        
        generate_prompt = ""
        if mode == "Abstract":
            generate_prompt = p.abstract(input_abstract)
        elif mode == "Title":
            generate_prompt = p.title(title)
        elif mode == "Title_Author":
            generate_prompt = p.title_author(title, author)
        elif mode == "Title_Abstract":
            generate_prompt = p.title_abstract(title, input_abstract)
        elif mode == "Title_Keywords":
            generate_prompt = p.title_keywords(title, input_abstract)
        elif mode == "Abstract_Author":
            generate_prompt = p.abstract_author(input_abstract, author)
        elif mode == "Abstract_Keywords":
            generate_prompt = p.abstract_keywords(input_abstract, input_keywords)
        elif mode == "Author_Keywords":
            generate_prompt = p.author_keywords(author, input_keywords)
        elif mode == "Keywords":
            generate_prompt = p.keywords(input_keywords)
        else:
            return "Nothing"
        result = extract_json(gemini.ask(generate_prompt))
        score = extract_score(result)

        
        # print(result)
        # print(score)

        with open(f"result_{mode}.json", "w", encoding="utf-8") as f:
            json.dump({
                "Mode" :mode,
                "Info":ele,
                "Abstract":input_abstract,
                "Keywords":input_keywords,
                "Result":result

            }, f, ensure_ascii=False, indent=2)

        read_data = []
        try:
            with open(f"result_score_diff.json", "r", encoding="utf-8") as f:
                try:
                    read_data = json.load(f)
                    # Ensure read_data is a list if it exists
                    if not isinstance(read_data, list):
                        read_data = []
                except json.JSONDecodeError:
                    read_data = []  # Initialize as an empty list instead of dict
        except FileNotFoundError:
            with open(f"result_score_diff.json", "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        read_data.append({
            "Mode": mode,
            "Score": score,
        })

                
        with open(f"result_score_diff.json", "w", encoding="utf-8") as f:
            json.dump(read_data, f, ensure_ascii=False, indent=2)

        print("-" * 20, "End", "-" * 20)


        
    else:
        print("Error: " + author['college'] + " not in dict")


def warp():
    """
    Moves result_*.json files to the next available numbered folder under Results/.
    Creates the folder if it doesn't exist.
    """

    # Ensure Results directory exists
    results_dir = "Results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Find all result_*.json files in current directory
    result_files = glob.glob("result_*.json")
    if not result_files:
        print("No result_*.json files found.")
        return
    
    # Find the next available number
    existing_folders = [int(f) for f in os.listdir(results_dir) if f.isdigit() and os.path.isdir(os.path.join(results_dir, f))]
    next_number = 1 if not existing_folders else max(existing_folders) + 1
    
    # Create the new folder
    new_folder = os.path.join(results_dir, str(next_number))
    os.makedirs(new_folder)
    
    # Move all result files to the new folder
    for file in result_files:
        shutil.move(file, os.path.join(new_folder, file))
    
    print(f"Moved {len(result_files)} result files to {new_folder}/")



if __name__ == "__main__":
    random.seed(11451456)
    # print(os.getcwd())
    r = reader("./AH/scholars_info_all.json")


    asjc = ASJC('./ASJC_code/detailed.json')
    gpt = ask.GPT()
    gemini = ask.Gemini()
    data = random.choices(r.scholars_with_college("College of Informatics"), k=10)
    
    for ele in data:
        print("*" * 40)
        start_asking("Title", ele)
        start_asking("Title_Abstract", ele)
        start_asking("Title_Author", ele)
        start_asking("Title_Keywords", ele)
        start_asking("Abstract", ele)
        start_asking("Abstract_Author", ele)
        start_asking("Abstract_Keywords", ele)
        start_asking("Author_Keywords", ele)
        start_asking("Keywords", ele)
        warp()

