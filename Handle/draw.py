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



def plot_score_distributions(llm_scores, title="Score Distributions by LLM"):
    """Create a plot showing score distributions for each LLM across CSO concepts."""
    plt.figure(figsize=(16, 10))
    
    # Colors for different LLMs
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']
    
    # Get all unique concepts across all LLMs
    all_concepts = set()
    for llm_data in llm_scores.values():
        all_concepts.update(llm_data.keys())
    all_concepts = sorted(list(all_concepts))
    
    # Plot each LLM's score distribution
    for i, (llm_name, scores) in enumerate(llm_scores.items()):
        y_values = [scores.get(concept, 0) for concept in all_concepts]
        color = colors[i % len(colors)]
        plt.plot(range(len(all_concepts)), y_values, 
                 marker='o', linestyle='-', label=llm_name, color=color)
    
    plt.title(title, fontsize=16)
    plt.xlabel('Concepts', fontsize=14)
    plt.ylabel('Score', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # Set x-axis ticks and labels
    plt.xticks(range(len(all_concepts)), all_concepts, rotation=45, ha='right', fontsize=8)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(f"{current_folder}/score_distributions.png", dpi=300, bbox_inches='tight')
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
    """Main function to analyze score data from JSON files."""
    # Paths to the JSON files
    # current_folder = f"./{input_folder}"
    categories =  {}   
    llm_names = [
        "claude-sonnet-4",
        "gemini2-5flash",
        "gemini2-5pro",
        "gpt4o",
        "grok3",
        "perplexity-pro"
    ]

    # Load data for each LLM
    llm_scores = {}
    for llm_name in llm_names:
        file_path = f"{current_folder}/{llm_name}.json"
        data = load_json_data(file_path)
        if data:
            llm_scores[llm_name] = extract_llm_scores(data)
        else:
            print(f"Could not load data for {llm_name}")
    
    if llm_scores:
        # Plot score distributions
        plot_score_distributions(llm_scores, "Score Distributions by LLM")
        grim_llm_score = categorize_scores_by_range(llm_scores)
        
        plot_concept_categories_table(grim_llm_score, "by Relevance Category")




input_folder = int(input("Enter the input folder number (e.g., 10): "))
current_folder = f"./{input_folder}_acm"
analyze_scores()
    # for input_folder in range(1, 13):
    #     print(f"Analyzing folder {input_folder}...")
    #     analyze_scores()

