import os
import json
from tqdm import tqdm

def simplify_json_files(source_folder, target_folder):
    """
    Simplifies JSON files from a source folder and saves them to a target folder.

    The simplified JSON contains only the 'final_score' (renamed to 'score') and 
    'reasoning' (renamed to 'reason') from the 'gemini_judge_final' field, 
    and the 'evidence' from the 'gemini_answer' field.
    """
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Created target folder: {target_folder}")

    file_list = [f for f in os.listdir(source_folder) if f.endswith('.json')]
    
    for filename in tqdm(file_list, desc="Simplifying JSON files"):
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, filename)

        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Skipping file {filename} due to error: {e}")
            continue

        simplified_data = {}

        # Check if the necessary keys exist and are not empty
        if not data.get('gemini_judge_final') or not data.get('gemini_answer'):
            continue

        gemini_judge = data['gemini_judge_final']
        gemini_answer_list = data['gemini_answer']
        
        # Ensure the data structures are as expected
        if not isinstance(gemini_judge, dict) or not isinstance(gemini_answer_list, list) or not gemini_answer_list:
            continue

        gemini_answer_sdgs = gemini_answer_list[0]
        
        # Iterate through the SDGs from the judge's final decision
        for sdg_name, judge_details in gemini_judge.items():
            if not isinstance(judge_details, dict):
                continue
                
            simplified_data[sdg_name] = {
                'score': judge_details.get('final_score'),
                'reason': judge_details.get('reasoning'),
                'evidence': gemini_answer_sdgs.get(sdg_name, {}).get('evidence', [])
            }

        if simplified_data:
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(simplified_data, f, ensure_ascii=False, indent=2)

def combine_simplified_jsons(simplified_folder, output_file):
    """
    Combines all simplified JSON files from a folder into a single JSON file.

    The resulting JSON is a dictionary where keys are the original filenames
    (without .json extension) and values are the contents of each JSON file.
    """
    combined_data = {}
    file_list = [f for f in os.listdir(simplified_folder) if f.endswith('.json')]

    for filename in tqdm(file_list, desc="Combining JSON files"):
        file_path = os.path.join(simplified_folder, filename)
        file_key = os.path.splitext(filename)[0]  # Get filename without extension

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            combined_data[file_key] = data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Skipping file {filename} during combination due to error: {e}")
            continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nAll simplified JSON files have been combined into: {output_file}")


if __name__ == '__main__':
    # --- 請在此處設定資料夾路徑 ---
    # User: Please fill in the source and target folder paths here.
    # source_folder: The directory containing the original JSON files.
    # target_folder: The directory where the simplified JSON files will be saved.
    # combined_output_file: The name for the final combined JSON file.

    source_folder = "all_courses_sdg_detail"  # 範例: "src/CollegeScale/all_courses_sdg_detail"
    target_folder = "simplified_sdg_detail"  # 範例: "src/CollegeScale/simplified_sdg_detail"
    combined_output_file = "combined_sdg_details.json" # 範例: "combined_sdg_details.json"
    
    # ------------------------------------

    # Make sure the source folder exists before running
    if not os.path.isdir(source_folder):
        print(f"錯誤：來源資料夾 '{source_folder}' 不存在或不是一個資料夾。")
        print(f"Error: Source folder '{source_folder}' does not exist or is not a directory.")
        print("請確保您已將 'source_folder' 設置為包含 JSON 檔案的正確路徑。")
        print("Please make sure you have set 'source_folder' to the correct path containing your JSON files.")
    else:
        # Step 1: Simplify individual JSON files
        simplify_json_files(source_folder, target_folder)
        print("\nSimplification process completed.")
        print(f"Simplified files are saved in: {target_folder}")

        # Step 2: Combine simplified files into one large JSON
        combine_simplified_jsons(target_folder, combined_output_file)
