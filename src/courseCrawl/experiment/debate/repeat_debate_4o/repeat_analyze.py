
import json
import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict

# SDG name to number mapping
SDG_MAPPING = {
    "No Poverty": "SDG_1",
    "Zero Hunger": "SDG_2",
    "Good Health and Well-being": "SDG_3",
    "Quality Education": "SDG_4",
    "Gender Equality": "SDG_5",
    "Clean Water and Sanitation": "SDG_6",
    "Affordable and Clean Energy": "SDG_7",
    "Decent Work and Economic Growth": "SDG_8",
    "Industry, Innovation and Infrastructure": "SDG_9",
    "Reduced Inequalities": "SDG_10",
    "Sustainable Cities and Communities": "SDG_11",
    "Responsible Consumption and Production": "SDG_12",
    "Climate Action": "SDG_13",
    "Life Below Water": "SDG_14",
    "Life on Land": "SDG_15",
    "Peace, Justice and Strong Institutions": "SDG_16",
    "Partnerships for the Goals": "SDG_17"
}

SDG_GOALS = list(SDG_MAPPING.keys())

def load_all_json_data(directory_path):
    """Load all JSON files in the given directory"""
    json_files = glob.glob(os.path.join(directory_path, "*.json"))
    data_list = []
    
    for file_path in json_files:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Extract course ID from filename
                base_name = os.path.basename(file_path)
                course_id = base_name.split('_')[0]
                run_index = base_name.split('_')[1].split('.')[0]
                data['course_id'] = course_id
                data['run_index'] = run_index
                data_list.append(data)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return data_list

def extract_scores_from_data(data_list):
    """Extract all scores from the data list and organize by course_id"""
    # Organize data by course_id
    course_data = defaultdict(list)
    for data in data_list:
        course_id = data.get('course_id', 'unknown')
        course_data[course_id].append(data)
    
    # Create a nested dictionary structure for course scores
    course_scores = {}
    
    for course_id, course_runs in course_data.items():
        # Initialize scores for this course
        course_scores[course_id] = {
            "gpt_original": {},
            "gemini_original": {},
            "gpt_judge_final": {},
            "gemini_judge_final": {}
        }
        
        # For each run of this course
        for run_data in course_runs:
            run_index = run_data.get('run_index', '0')
            
            # Extract scores from this run
            try:
                sdgs = list(run_data["gpt_answer"].keys())
                
                # Extract original scores
                for sdg in sdgs:
                    # Initialize if first time seeing this SDG
                    if sdg not in course_scores[course_id]["gpt_original"]:
                        course_scores[course_id]["gpt_original"][sdg] = {}
                        course_scores[course_id]["gemini_original"][sdg] = {}
                        course_scores[course_id]["gpt_judge_final"][sdg] = {}
                        course_scores[course_id]["gemini_judge_final"][sdg] = {}
                    
                    # Store original scores
                    course_scores[course_id]["gpt_original"][sdg][run_index] = run_data["gpt_answer"][sdg]["score"]
                    course_scores[course_id]["gemini_original"][sdg][run_index] = run_data["gemini_answer"][sdg]["score"]
                
                # Calculate final scores for each judge
                for sdg in sdgs:
                    # Extract critique suggestions
                    gpt_critique_score = None
                    gemini_critique_score = None
                    
                    if "suggested_changes" in run_data["gpt_critique"]:
                        for sdg_key, change in run_data["gpt_critique"]["suggested_changes"].items():
                            # Match SDG name or number
                            if (sdg_key == sdg or 
                                SDG_MAPPING.get(sdg) == sdg_key or 
                                sdg == SDG_MAPPING.get(sdg_key)):
                                gpt_critique_score = change["new_score"]
                                break
                    
                    if "suggested_changes" in run_data["gemini_critique"]:
                        for sdg_key, change in run_data["gemini_critique"]["suggested_changes"].items():
                            # Match SDG name or number
                            if (sdg_key == sdg or 
                                SDG_MAPPING.get(sdg) == sdg_key or 
                                sdg == SDG_MAPPING.get(sdg_key)):
                                gemini_critique_score = change["new_score"]
                                break
                    
                    # Get judge decisions
                    gpt_winner = run_data["gpt_judge_final"][sdg]["winner"]
                    gemini_winner = run_data["gemini_judge_final"][sdg]["winner"]
                    
                    # Calculate final scores based on judge decisions
                    gpt_score = run_data["gpt_answer"][sdg]["score"]
                    gemini_score = run_data["gemini_answer"][sdg]["score"]
                    
                    # GPT judge final score
                    if gpt_winner == "A":
                        gpt_final = gpt_score if gemini_critique_score is None else (gpt_score + gemini_critique_score) / 2
                    elif gpt_winner == "B":
                        gpt_final = gemini_score if gpt_critique_score is None else (gemini_score + gpt_critique_score) / 2
                    else:  # Tie
                        scores = [s for s in [gpt_score, gemini_score, gpt_critique_score, gemini_critique_score] if s is not None]
                        gpt_final = sum(scores) / len(scores)
                    
                    # Gemini judge final score
                    if gemini_winner == "A":
                        gemini_final = gpt_score if gemini_critique_score is None else (gpt_score + gemini_critique_score) / 2
                    elif gemini_winner == "B":
                        gemini_final = gemini_score if gpt_critique_score is None else (gemini_score + gpt_critique_score) / 2
                    else:  # Tie
                        scores = [s for s in [gpt_score, gemini_score, gpt_critique_score, gemini_critique_score] if s is not None]
                        gemini_final = sum(scores) / len(scores)
                    
                    course_scores[course_id]["gpt_judge_final"][sdg][run_index] = gpt_final
                    course_scores[course_id]["gemini_judge_final"][sdg][run_index] = gemini_final
                    
            except Exception as e:
                print(f"Error processing data for course {course_id}, run {run_index}: {e}")
                continue
    
    # Filter out SDGs where no score is over 7 in any analysis
    filtered_course_scores = {}
    for course_id, score_data in course_scores.items():
        filtered_course_scores[course_id] = {
            "gpt_original": {},
            "gemini_original": {},
            "gpt_judge_final": {},
            "gemini_judge_final": {}
        }
        
        for sdg in SDG_GOALS:
            # Check if this SDG exists in any of the analyses
            has_high_score = False
            
            # Check each analysis type
            for analysis_type in ["gpt_original", "gemini_original", "gpt_judge_final", "gemini_judge_final"]:
                if sdg in score_data[analysis_type]:
                    # Check if any score is over 7
                    for run_index, score in score_data[analysis_type][sdg].items():
                        if score > 0:
                            has_high_score = True
                            break
                    
                    if has_high_score:
                        break
            
            # If we found a high score, include this SDG in the filtered data
            if has_high_score:
                for analysis_type in ["gpt_original", "gemini_original", "gpt_judge_final", "gemini_judge_final"]:
                    if sdg in score_data[analysis_type]:
                        filtered_course_scores[course_id][analysis_type][sdg] = score_data[analysis_type][sdg]
    
    return filtered_course_scores

def create_heatmaps(course_scores):
    """Create heatmaps showing stability (std) of scores across runs for all courses"""
    # Create output directory if it doesn't exist
    output_dir = "heatmaps"
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare data structures for standard deviation calculation
    score_types = ["gpt_original", "gemini_original", "gpt_judge_final", "gemini_judge_final"]
    std_data = {score_type: defaultdict(dict) for score_type in score_types}
    
    # Calculate standard deviations for each course, SDG, and score type
    for course_id, scores in course_scores.items():
        for score_type in score_types:
            for sdg, runs in scores[score_type].items():
                if runs:  # Only calculate if there are runs
                    values = list(runs.values())
                    if len(values) > 1:  # Need at least 2 values to calculate std
                        std_data[score_type][course_id][sdg] = np.std(values)
                    else:
                        std_data[score_type][course_id][sdg] = 0  # No variation with only 1 run
    
    # Create a figure with 2x2 subplots
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle(f"Standard Deviation of SDG Scores Across Runs", fontsize=16)
    
    # Titles for each subplot
    title_map = {
        "gpt_original": "GPT Original Scores - Std Dev",
        "gemini_original": "Gemini Original Scores - Std Dev",
        "gpt_judge_final": "GPT Judge Final Scores - Std Dev",
        "gemini_judge_final": "Gemini Judge Final Scores - Std Dev"
    }
    
    # Convert data to DataFrames and create heatmaps
    for score_type, ax in zip(score_types, axes.flatten()):
        # Convert to DataFrame
        df = pd.DataFrame.from_dict(std_data[score_type], orient='index')
        
        # Make sure all SDGs are included with consistent order
        for sdg in SDG_GOALS:
            if sdg not in df.columns:
                df[sdg] = 0
        
        # Sort columns by SDG order
        df = df[SDG_GOALS]
        
        # Create heatmap
        sns.heatmap(df, ax=ax, cmap="YlOrRd", annot=True, fmt=".2f", 
                   vmin=0, vmax=df.values.max() if df.values.size > 0 and df.values.max() > 0 else 1,
                   cbar_kws={'label': 'Std Dev'})
        
        ax.set_title(title_map[score_type], fontsize=14)
        ax.set_xlabel("SDG Goals", fontsize=12)
        ax.set_ylabel("Course IDs", fontsize=12)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    plt.tight_layout(rect=(0, 0, 1, 0.97))  # Adjust for suptitle
    output_path = os.path.join(output_dir, "sdg_stability_stddev.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"Created standard deviation heatmaps at {output_path}")

    # Create scatter plots to compare standard deviations before vs after debate
    create_std_comparison_scatterplots(std_data, course_scores, output_dir)

def create_std_comparison_scatterplots(std_data, course_scores, output_dir):
    """Create scatter plots comparing std before and after debate"""
    # Prepare data for scatter plots
    gpt_comparison = []
    gemini_comparison = []
    
    # Extract data points for comparison
    for course_id in std_data["gpt_original"].keys():
        for sdg in std_data["gpt_original"][course_id].keys():
            if sdg in std_data["gpt_judge_final"][course_id]:
                gpt_comparison.append((
                    std_data["gpt_original"][course_id][sdg],
                    std_data["gpt_judge_final"][course_id][sdg],
                    f"{course_id}:{sdg}"  # Label for point
                ))
            
            if sdg in std_data["gemini_judge_final"][course_id]:
                gemini_comparison.append((
                    std_data["gemini_original"][course_id][sdg],
                    std_data["gemini_judge_final"][course_id][sdg],
                    f"{course_id}:{sdg}"  # Label for point
                ))
    
    # Create scatter plot figure with 1x2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    fig.suptitle(f"Comparison of Standard Deviations Before vs After Debate", fontsize=16)
    
    # Process both models
    for ax_idx, (comparison_data, title) in enumerate([
        (gpt_comparison, "GPT: Original vs Judge Final"),
        (gemini_comparison, "Gemini: Original vs Judge Final")
    ]):
        ax = axes[ax_idx]
        
        # Extract x and y values
        x_vals = [x for x, _, _ in comparison_data]
        y_vals = [y for _, y, _ in comparison_data]
        labels = [label for _, _, label in comparison_data]
        
        # Draw scatter plot
        scatter = ax.scatter(x_vals, y_vals, alpha=0.7)
        
        # Draw diagonal line for reference
        max_val = max(max(x_vals) if x_vals else 0, max(y_vals) if y_vals else 0)
        ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.5)
        
        # Add titles and labels
        ax.set_title(title, fontsize=14)
        ax.set_xlabel("Standard Deviation Before Debate", fontsize=12)
        ax.set_ylabel("Standard Deviation After Debate", fontsize=12)
        
        # Make both axes start at 0 and have the same scale
        ax.set_xlim(0, max_val * 1.1)
        ax.set_ylim(0, max_val * 1.1)
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Add counts of points above/below diagonal
        below_diag = sum(1 for x, y in zip(x_vals, y_vals) if y < x)
        above_diag = sum(1 for x, y in zip(x_vals, y_vals) if y > x)
        equal_diag = sum(1 for x, y in zip(x_vals, y_vals) if y == x)
         
        # Print details about equal std points
        print(f"\n--- {title}: Points with Equal Standard Deviation Before and After ---")
        if equal_diag > 0:
            for i, (x, y, label) in enumerate(zip(x_vals, y_vals, labels)):
                if y == x:
                    course_id, sdg = label.split(':')
                    
                    # Collect the actual scores for this course and SDG
                    model_type = "gpt" if "GPT" in title else "gemini"
                    
                    # Get the original scores
                    original_scores = list(course_scores[course_id][f"{model_type}_original"][sdg].values())
                    
                    # Get the final scores
                    final_scores = list(course_scores[course_id][f"{model_type}_judge_final"][sdg].values())
                    
                    # print(f"Point {i+1}: {label}")
                    # print(f"  Standard Deviation: {x:.4f}")
                    # print(f"  Original scores: {', '.join([f'{s:.2f}' for s in original_scores])}")
                    # print(f"  Final scores: {', '.join([f'{s:.2f}' for s in final_scores])}")
                    print(f"  Mean original: {np.mean(original_scores):.2f}, Mean final: {np.mean(final_scores):.2f}")
        else:
            print("No points with equal standard deviation found.")
        print("---" * 20)

        info_text = f"Points: {len(x_vals)}\nMore stable after: {below_diag}\nLess stable after: {above_diag}\nNo change: {equal_diag}"
        ax.text(0.05, 0.95, info_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout(rect=(0, 0, 1, 0.95))  # Adjust for suptitle
    output_path = os.path.join(output_dir, "stability_comparison_scatter.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print(f"Created standard deviation comparison scatter plots at {output_path}")



def main():
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = "."
    
    # Load all JSON data
    print("Loading JSON data...")
    data_list = load_all_json_data(directory_path)
    
    if not data_list:
        print("No valid JSON files found.")
        return
    
    print(f"Loaded {len(data_list)} JSON files.")
    
    # Extract and process scores
    print("Extracting scores...")
    course_scores = extract_scores_from_data(data_list)
    
    print(f"Found {len(course_scores)} unique courses.")
    
    # Create heatmaps for each course
    print("Creating heatmaps...")
    create_heatmaps(course_scores)
    
    print("Analysis complete!")

if __name__ == "__main__":
    main()

