import matplotlib.pyplot as plt
import numpy as np

import json
import os
import glob

def load_all_json_data(directory_path):
    """Load all JSON files in the given directory"""
    json_files = glob.glob(os.path.join(directory_path, "*.json"))
    data_list = []
    
    for file_path in json_files:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                data_list.append(data)
                # print(f"Loaded: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return data_list

def calculate_average_scores_final(data):
    # Initialize dictionaries to store sum of scores for each SDG
    gemini_scores = {
        "No Poverty": [], "Zero Hunger": [], "Good Health and Well-being": [],
        "Quality Education": [], "Gender Equality": [], "Clean Water and Sanitation": [],
        "Affordable and Clean Energy": [], "Decent Work and Economic Growth": [],
        "Industry, Innovation and Infrastructure": [], "Reduced Inequalities": [],
        "Sustainable Cities and Communities": [], "Responsible Consumption and Production": [],
        "Climate Action": [], "Life Below Water": [], "Life on Land": [],
        "Peace, Justice and Strong Institutions": [], "Partnerships for the Goals": []
    }
    
    gpt_scores = {key: [] for key in gemini_scores.keys()}
    
    # Create normalized lookup dictionaries (lowercase keys mapped to original keys)
    gemini_norm_keys = {k.lower(): k for k in gemini_scores.keys()}
    gpt_norm_keys = {k.lower(): k for k in gpt_scores.keys()}
    
    # Iterate through each JSON file's data and collect scores
    for json_data in data:
        try:
            for sdg in json_data["gpt_judge_final"]:
                # Normalize the key by converting to lowercase for lookup
                norm_sdg = sdg.lower()
                if norm_sdg in gpt_norm_keys:
                    standard_key = gpt_norm_keys[norm_sdg]
                    gpt_scores[standard_key].append(json_data["gpt_judge_final"][sdg]["final_score"])
            
            for sdg in json_data["gemini_judge_final"]:
                # Normalize the key by converting to lowercase for lookup
                norm_sdg = sdg.lower()
                if norm_sdg in gemini_norm_keys:
                    standard_key = gemini_norm_keys[norm_sdg]
                    gemini_scores[standard_key].append(json_data["gemini_judge_final"][sdg]["final_score"])
        except Exception as e:
            print(f"Error processing a JSON file: {e} {json_data}")
    
    # Calculate averages for each SDG
    gpt_avg = {sdg: sum(scores)/len(scores) if scores else 0 for sdg, scores in gpt_scores.items()}
    gemini_avg = {sdg: sum(scores)/len(scores) if scores else 0 for sdg, scores in gemini_scores.items()}
    
    return gemini_avg, gpt_avg




def plot_avg_score_final(data, model_name=""):
    
    # Define SDG names with their numbers
    sdg_names = [
        "1. No Poverty", "2. Zero Hunger", "3. Good Health and Well-being",
        "4. Quality Education", "5. Gender Equality", "6. Clean Water and Sanitation",
        "7. Affordable and Clean Energy", "8. Decent Work and Economic Growth",
        "9. Industry, Innovation and Infrastructure", "10. Reduced Inequalities",
        "11. Sustainable Cities and Communities", "12. Responsible Consumption and Production",
        "13. Climate Action", "14. Life Below Water", "15. Life on Land",
        "16. Peace, Justice and Strong Institutions", "17. Partnerships for the Goals"
    ]
    
    # Extract scores in the same order as sdg_names
    original_sdg_names = list(data.keys())
    scores = [data[sdg] for sdg in original_sdg_names]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))
    bars = ax.bar(sdg_names, scores, color='skyblue')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.2f}', ha='center', va='bottom')
    
    # Set y-axis limits from 0 to 10
    ax.set_ylim(0, 10)
    
    # Add labels and title
    ax.set_xlabel('Sustainable Development Goals (SDGs)')
    ax.set_ylabel('Average Score')
    ax.set_title(f'Average SDG Scores for Commerce College (475 courses) ({model_name})')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f"{model_name}_avg_scores.png")
    plt.close()



if __name__ == "__main__":
    result_dir = "./result/"
    data = load_all_json_data(result_dir)
    print(data[0]['gemini_judge_final'].keys())
    gemini_avg, gpt_avg = calculate_average_scores_final(data)
    
    json.dump(gemini_avg, open("gemini_avg.json", "w"), indent=4)
    json.dump(gpt_avg, open("gpt_avg.json", "w"), indent=4)

    plot_avg_score_final(gemini_avg, "Gemini-2.5-flash")
    plot_avg_score_final(gpt_avg, "GPT-5-nano")
    

