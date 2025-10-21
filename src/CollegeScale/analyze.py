import matplotlib.pyplot as plt
import numpy as np

import json
import os
import glob

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




def plot_avg_score_final(data, model_name="", college_name="", num_courses=0):
    
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
    ax.set_title(f'Average SDG Scores for {college_name} ({num_courses} courses) ({model_name})')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f"plots/{model_name}_{college_name.replace(' ', '_')}_avg_scores.png")
    plt.close()



if __name__ == "__main__":
    result_dir = "./all_courses/"
    college_json_dir = "./" # Assuming college JSONs are in the current directory

    # Ensure plots directory exists
    plots_dir = "./plots/"
    os.makedirs(plots_dir, exist_ok=True)

    # List of college names to process (from CourseAnalyze.py)
    college_names = [
        "College_of_Commerce", "College_of_Law", "College_of_Liberal_Arts",
        "College_of_Science", "College_of_Social_Science", "College_of_Foreign_Languages",
        "College_of_Communication", "College_of_International_Affairs",
        "College_of_Education", "International_College_of_Innovation",
        "College_of_Informatics", "College_of_Xperimental",
        "Bachelor_Program_of_in_Sport", "PE_Coures",
        "Center_for_Creativity", "else_course"
    ]

    for college_name in college_names:
        college_file_path = os.path.join(college_json_dir, f"{college_name}.json")
        if not os.path.exists(college_file_path):
            print(f"Warning: College JSON file not found: {college_file_path}. Skipping.")
            continue

        with open(college_file_path, 'r', encoding='utf-8') as f:
            course_ids = json.load(f)

        print(f"Processing {college_name} with {len(course_ids)} courses...")

        filtered_data = load_all_json_data(result_dir, course_ids_filter=course_ids)
        num_filtered_courses = len(filtered_data)

        if num_filtered_courses == 0:
            print(f"No data found for {college_name}. Skipping plot generation.")
            continue

        gemini_avg, gpt_avg = calculate_average_scores_final(filtered_data)

        # Save average scores to JSON files
        json.dump(gemini_avg, open(f"gemini_avg_{college_name}.json", "w"), indent=4)
        json.dump(gpt_avg, open(f"gpt_avg_{college_name}.json", "w"), indent=4)

        # Plotting
        plot_avg_score_final(gemini_avg, "Gemini-2.5-flash", college_name, num_filtered_courses)
        plot_avg_score_final(gpt_avg, "GPT-4o-mini", college_name, num_filtered_courses)

    print("Analysis complete. Plots saved to the 'plots/' directory.")
    

