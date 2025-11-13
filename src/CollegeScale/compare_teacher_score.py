import pandas as pd
import json
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# Function to get a Chinese font path on macOS, adapted from analyze.py
def get_chinese_font_path():
    """
    Searches for a common Chinese font on macOS.
    """
    potential_font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for path in potential_font_paths:
        if os.path.exists(path):
            return path
    return None

def load_all_json_data(directory_path):
    """Load all JSON files in the given directory."""
    json_files = glob.glob(os.path.join(directory_path, "*.json"))
    data_list = []
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                data["file_path"] = file_path
                data_list.append(data)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return data_list

def is_llm_sustainable(course_data, model_name="Gemini-2.5-pro", threshold=5.0):
    """
    Determines if a course is sustainable based on LLM scores,
    mimicking the logic from analyze_university_sdg_coverage.
    """
    model_judge_key = "gemini_judge_final" if "gemini" in model_name.lower() else "gpt_judge_final"
    
    if model_judge_key in course_data and isinstance(course_data[model_judge_key], dict):
        for sdg_name, sdg_info in course_data[model_judge_key].items():
            score = sdg_info.get("final_score", 0)
            # Special case for Quality Education
            if "quality education" in sdg_name.lower():
                if score == 10:
                    return True
            # General case for other SDGs
            elif score > threshold:
                return True
    return False

def compare_scores(llm_data, teacher_scores_df, model_name, llm_threshold):
    """
    Compares LLM scores with teacher scores and categorizes them.
    """
    # Create a dictionary for quick lookup of teacher scores
    teacher_scores_map = pd.Series(teacher_scores_df['永續課程'].values, index=teacher_scores_df['科目代號']).to_dict()

    # Initialize counters
    results = {
        "LLM_and_Teacher_Agree": [],
        "LLM_Agrees_Teacher_Disagree": [],
        "Teacher_Agrees_LLM_Disagree": [],
        "Both_Disagree": []
    }

    for course_data in llm_data:
        course_id_str = os.path.splitext(os.path.basename(course_data["file_path"]))[0]
        
        # Teacher's assessment
        teacher_score = teacher_scores_map.get(course_id_str)
        # Also handle cases where the course_id might be an integer in the csv
        if teacher_score is None:
             try:
                teacher_score = teacher_scores_map.get(int(course_id_str))
             except (ValueError, TypeError):
                # print(f"Warning: Course ID {course_id_str} not found in teacher scores file. Skipping.")
                continue
        
        if teacher_score is None:
            # print(f"Warning: Course ID {course_id_str} not found in teacher scores file after type conversion. Skipping.")
            continue

        teacher_agrees = teacher_score >= 3

        # LLM's assessment
        llm_agrees = is_llm_sustainable(course_data, model_name=model_name, threshold=llm_threshold)

        # Categorize
        if llm_agrees and teacher_agrees:
            results["LLM_and_Teacher_Agree"].append(course_id_str)
        elif llm_agrees and not teacher_agrees:
            results["LLM_Agrees_Teacher_Disagree"].append(course_id_str)
        elif not llm_agrees and teacher_agrees:
            results["Teacher_Agrees_LLM_Disagree"].append(course_id_str)
        else: # not llm_agrees and not teacher_agrees
            results["Both_Disagree"].append(course_id_str)
            
    return results

def plot_comparison_results(results, model_name, llm_threshold):
    """
    Visualizes the comparison results as a bar chart.
    """
    # Use a Chinese font if available
    font_path = get_chinese_font_path()
    if font_path:
        font_name = FontProperties(fname=font_path).get_name()
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [font_name]
        plt.rcParams['axes.unicode_minus'] = False
    else:
        print("Warning: No suitable Chinese font found. Plot labels might not display correctly.")

    categories = {
        "LLM 和老師都認同": len(results["LLM_and_Teacher_Agree"]),
        "LLM 認同，老師不認同": len(results["LLM_Agrees_Teacher_Disagree"]),
        "老師認同，LLM 不認同": len(results["Teacher_Agrees_LLM_Disagree"]),
        "兩者皆不認同": len(results["Both_Disagree"])
    }
    
    labels = list(categories.keys())
    counts = list(categories.values())

    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(labels, counts, color=['green', 'blue', 'orange', 'red'])

    # Add counts on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom')

    ax.set_ylabel('課程數量')
    ax.set_title(f'LLM ({model_name}, threshold>{llm_threshold}) vs. 老師 (score>=3) 永續課程標記比較')
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()

    # Save the plot
    plot_filename = f"comparison_{model_name.replace(' ', '_')}_vs_teacher.png"
    plt.savefig(plot_filename)
    print(f"Plot saved as {plot_filename}")


if __name__ == "__main__":
    # --- Configuration ---
    MODEL_NAME = "Gemini-2.5-pro"  # Or "GPT-4o-mini"
    LLM_THRESHOLD = 9.0 # Threshold for LLM to agree
    TEACHER_CSV_PATH = "../1141.csv"
    LLM_DATA_DIR = "./all_courses_sdg_detail/"
    # --- End Configuration ---

    # Load teacher scores
    try:
        teacher_scores_df = pd.read_csv(TEACHER_CSV_PATH)
        # Ensure course ID is string for matching
        teacher_scores_df['科目代號'] = teacher_scores_df['科目代號'].astype(str)
    except FileNotFoundError:
        print(f"Error: Teacher scores file not found at {TEACHER_CSV_PATH}")
        exit()

    # Load LLM analysis data
    llm_data = load_all_json_data(LLM_DATA_DIR)
    if not llm_data:
        print(f"Error: No LLM data found in {LLM_DATA_DIR}")
        exit()

    # Perform comparison
    comparison_results = compare_scores(llm_data, teacher_scores_df, MODEL_NAME, LLM_THRESHOLD)

    # Print summary
    print("--- Comparison Summary ---")
    print(f"Model: {MODEL_NAME} (Threshold > {LLM_THRESHOLD})")
    print(f"Teacher Threshold >= 3")
    print("-" * 26)
    for category, courses in comparison_results.items():
        print(f"{category}: {len(courses)} courses")
    
    # Visualize results
    plot_comparison_results(comparison_results, MODEL_NAME, LLM_THRESHOLD)
