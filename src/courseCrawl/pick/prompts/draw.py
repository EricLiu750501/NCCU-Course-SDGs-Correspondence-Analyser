import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# Add the project root directory to the Python path to enable absolute imports
# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the src directory
src_dir = os.path.dirname(current_dir)
# Go up another level to the project root
project_root = os.path.dirname(src_dir)
# Add project root to Python path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

SDG_ORDER = [
    "No Poverty",
    "Zero Hunger",
    "Good Health and Well-being",
    "Quality Education",
    "Gender Equality",
    "Clean Water and Sanitation",
    "Affordable and Clean Energy",
    "Decent Work and Economic Growth",
    "Industry, Innovation and Infrastructure",
    "Reduced Inequalities",
    "Sustainable Cities and Communities",
    "Responsible Consumption and Production",
    "Climate Action",
    "Life Below Water",
    "Life on Land",
    "Peace, Justice and Strong Institutions",
    "Partnerships for the Goals"
]



def load_json_data(file_path):
    """Load data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def extract_llm_scores(data_dict):
    """Extract scores from the CSO Concepts data for a specific LLM."""
    scores = {}
    for concept, details in data_dict.items():
        scores[concept] = details.get("score", 0)
    return scores


def categorize_scores_by_range(llm_scores):
    """
    Categorize concepts based on score ranges for each LLM.
    
    Categories:
    - 10: Exact score of 10
    - 7-9.999: High relevance
    - 4-6.999: Medium relevance
    - 1-3.999: Low relevance
    - 0.001-0.999: Minimal relevance
    """
    categories = {
        "10.000": "Core concept (10.000)",
        "7-9.999": "Highly relevant (7.000-9.999)",
        "4-6.999": "Moderately relevant (4.000-6.999)",
        "1-3.999": "Low relevance (1.000-3.999)",
        "0.001-0.999": "Minimal relevance (0.001-0.999)"
    }
    
    # Dictionary to store categorized concepts for each LLM
    llm_categories = {}
    
    for llm_name, scores in llm_scores.items():
        categorized = {
            "10.000": [],
            "7-9.999": [],
            "4-6.999": [],
            "1-3.999": [],
            "0.001-0.999": []
        }
        
        for concept, score in scores.items():
            if score == 10:
                categorized["10.000"].append(concept)
            elif 7 <= score < 10:
                categorized["7-9.999"].append(concept)
            elif 4 <= score < 7:
                categorized["4-6.999"].append(concept)
            elif 1 <= score < 4:
                categorized["1-3.999"].append(concept)
            elif 0.001 <= score < 1:
                categorized["0.001-0.999"].append(concept)
        
        llm_categories[llm_name] = categorized
    
    return llm_categories, categories



def plot_score_distributions(llm_scores, title="Score Distributions by LLM", course_code="0"):
    """Create a bar chart showing score distributions for each LLM across SDGs."""
    plt.figure(figsize=(16, 10))
    
    # Colors for different LLMs
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    
    # Get all unique concepts across all LLMs
    all_concepts = set()
    for llm_data in llm_scores.values():
        all_concepts.update(llm_data.keys())
    # all_concepts = list(all_concepts)
    all_concepts = SDG_ORDER
    
    # Number of LLMs and concepts for positioning bars
    n_llms = len(llm_scores)
    n_concepts = len(all_concepts)
    
    # Width of each bar group and individual bars
    group_width = 0.8  # width of the entire group of bars for one concept
    bar_width = group_width / n_llms  # width of individual bars
    
    # Plot bars for each LLM
    for i, (llm_name, scores) in enumerate(llm_scores.items()):
        y_values = [scores.get(concept, 0) for concept in all_concepts]
        x_positions = [j + (i - n_llms/2 + 0.5) * bar_width for j in range(n_concepts)]
        plt.bar(x_positions, y_values, width=bar_width, label=llm_name, color=colors[i % len(colors)], alpha=0.8)
    
    plt.title(title, fontsize=16)
    plt.xlabel('SDGs', fontsize=14)
    plt.ylabel('Score', fontsize=14)
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(fontsize=12)
    
    # Set x-axis ticks and labels at the center of each group
    plt.xticks(range(len(all_concepts)), all_concepts, rotation=45, ha='right', fontsize=8)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(f"{current_folder}/{course_code}.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_concept_categories_table(grim_llm_score , title="Concepts by Score Category"):

    """
    Create a table showing concepts by score category for each LLM.
    
    Args:
        grim_llm_score: A tuple containing (llm_categories, category_labels)
            - llm_categories: Dictionary with LLM names as keys and dictionaries of 
                            categorized concepts as values
            - category_labels: Dictionary mapping category keys to display labels
        title: Title for the plot
    """
    # Unpack the tuple input
    llm_categories, category_labels = grim_llm_score
    
    # Create a pandas DataFrame for better visualization
    llm_names = list(llm_categories.keys())
    category_names = list(category_labels.keys())
    
    # Initialize the DataFrame with empty cells
    data = []
    for llm_name in llm_names:
        row_data = []
        for category in category_names:
            concepts = llm_categories[llm_name][category]
            cell_text = "\n".join(sorted(concepts)) if concepts else "-"
            row_data.append(cell_text)
        data.append(row_data)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(20, 12))
    ax.axis('tight')
    ax.axis('off')
    
    # Create the table with column headers and row labels
    column_labels = [category_labels[cat] for cat in category_names]
    table = ax.table(cellText=data,
                    rowLabels=llm_names,
                    colLabels=column_labels,
                    cellLoc='left',
                    loc='center',
                    bbox=[0, 0, 1, 0.9])
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(16)
    
    # Make cells wrap text and adjust height
    for (i, j), cell in table.get_celld().items():
        cell.set_height(0.12)  # Increase cell height for better text display
        cell._text.set_wrap(True)
    
    plt.title(title, fontsize=16, y=0.98)
    plt.tight_layout()
    
    # Save the table
    plt.savefig(f"{current_folder}/concept_categories_table.png", dpi=300, bbox_inches='tight')
    plt.close()

def analyze_scores():
    """Analyze all JSON score data in the current folder."""
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # 找出所有 .json 檔案
    json_files = [f for f in os.listdir(current_folder) if f.endswith(".json")]

    if not json_files:
        print("⚠️ No JSON files found in the current folder.")
        return

    llm_scores = {}
    for json_file in json_files:
        llm_name = os.path.splitext(json_file)[0]  # 去掉 .json 當作名稱
        file_path = os.path.join(current_folder, json_file)
        data = load_json_data(file_path)
        if data:
            llm_scores[llm_name] = extract_llm_scores(data)
        else:
            print(f"⚠️ Could not load data for {llm_name}")

    if llm_scores:
        plot_score_distributions(llm_scores, current_folder, "Score Distributions by LLM")
        grim_llm_score = categorize_scores_by_range(llm_scores)
        plot_concept_categories_table(grim_llm_score, current_folder, "by Relevance Category")



if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # 找出所有 .json 檔案
    json_files = [f for f in os.listdir(current_folder) if f.endswith(".json")]
    llm_scores = {}     
    for js in json_files:
        filename = os.path.splitext(js)[0]
        file_path = os.path.join(current_folder, filename + ".json")
        data = load_json_data(file_path)
        scores = extract_llm_scores(data)
        llm_scores["gpt5"] = scores
        plot_score_distributions(llm_scores,f"Score Distributions for {filename} by LLM", filename)






