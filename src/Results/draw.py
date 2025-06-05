import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial
from scipy.stats import pearsonr, spearmanr
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

from src.ASJC_code.getASJC import ASJC


def load_json_data(file_path):
    """Load data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def extract_mode_scores(data):
    """Extract scores for each mode from the data."""
    mode_scores = {}
    for item in data:
        mode = item.get("Mode")
        scores = item.get("Score")
        if mode and scores:
            mode_scores[mode] = scores
    return mode_scores

def calculate_correlations(mode_scores):
    """Calculate Cosine, Pearson, and Spearman correlations between different modes."""
    correlation_results = {
        'Cosine': {},
        'Pearson': {},
        'Spearman': {}
    }
    
    modes = list(mode_scores.keys())
    
    for i, mode1 in enumerate(modes):
        for j, mode2 in enumerate(modes):
            if i >= j:  # Skip self-correlations and duplicates
                continue
                
            # Get scores for both modes
            scores1 = np.array(mode_scores[mode1])
            scores2 = np.array(mode_scores[mode2])
            
            # Calculate Cosine similarity
            cosine_sim = 1 - spatial.distance.cosine(scores1, scores2)
            correlation_results['Cosine'][f"{mode1} vs {mode2}"] = cosine_sim
            
            # Calculate Pearson correlation
            pearson_corr, _ = pearsonr(scores1, scores2)
            correlation_results['Pearson'][f"{mode1} vs {mode2}"] = pearson_corr
            
            # Calculate Spearman correlation
            spearman_corr, _ = spearmanr(scores1, scores2)
            correlation_results['Spearman'][f"{mode1} vs {mode2}"] = spearman_corr
            
    return correlation_results

def plot_score_distributions(mode_scores, title="Score Distributions by Mode"):
    """Create a plot showing score distributions for each mode."""
    plt.figure(figsize=(12, 8))
    
    # Colors for different modes
    colors = [ 'blue',       # 藍色
        'red',        # 紅色
        'green',      # 綠色
        'orange',     # 橘色
        'purple',     # 紫色
        'brown',      # 棕色
        'pink',       # 粉紅色
        'gray',       # 灰色
        'olive'       # 橄欖綠
    ]
    
    asjc = ASJC("../ASJC_code/detailed.json")
    index = asjc.subDomainQuery('Computer Science', [i for i in range(13)])
    
    # Plot each mode's score distribution
    for i, (mode, scores) in enumerate(mode_scores.items()):
        color = colors[i % len(colors)]
        plt.plot(range(len(scores)), scores, 
                 marker='o', linestyle='-', label=mode, color=color)
    
    plt.title(title, fontsize=16)
    plt.xlabel('Computer Science Subdomains', fontsize=14)
    plt.ylabel('Score', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # Set x-axis ticks and labels if we have ASJC subdomain information
    if index:
        # If we have more data points than labels, use a subset of the labels
        if len(scores) > len(index):
            plt.xticks(range(len(index)), index, rotation=45, ha='right', fontsize=8)
        else:
            plt.xticks(range(len(scores)), index[:len(scores)], rotation=45, ha='right', fontsize=8)
    
    # Save the plot
    plt.savefig(f"./{input_folder}/score_distributions.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_correlation_heatmap(correlation_results):
    """Create 2D heatmaps for correlation metrics."""
    # Extract all unique modes from correlation results
    modes = set()
    for _, correlations in correlation_results.items():
        for comparison in correlations.keys():
            mode1, mode2 = comparison.split(" vs ")
            modes.add(mode1)
            modes.add(mode2)
    
    modes = sorted(list(modes))
    
    # Create separate heatmap for each correlation metric
    for metric, correlations in correlation_results.items():
        # Initialize correlation matrix with NaNs (diagonal will be 1.0)
        corr_matrix = np.ones((len(modes), len(modes)))
        np.fill_diagonal(corr_matrix, 1.0)
        
        # Fill the correlation matrix
        for comparison, value in correlations.items():
            mode1, mode2 = comparison.split(" vs ")
            idx1, idx2 = modes.index(mode1), modes.index(mode2)
            corr_matrix[idx1, idx2] = value
            corr_matrix[idx2, idx1] = value  # Symmetric matrix
        
        # Create the heatmap
        plt.figure(figsize=(10, 8))
        im = plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
        
        # Add colorbar
        plt.colorbar(im, label=f'{metric} Correlation')
        
        # Add text annotations
        for i in range(len(modes)):
            for j in range(len(modes)):
                text_color = 'white' if abs(corr_matrix[i, j]) > 0.5 else 'black'
                plt.text(j, i, f'{corr_matrix[i, j]:.3f}', 
                         ha='center', va='center', color=text_color, fontsize=9)
        
        # Set ticks and labels
        plt.xticks(range(len(modes)), modes, rotation=45, ha='right')
        plt.yticks(range(len(modes)), modes)
        
        plt.title(f'{metric} Correlation Heatmap', fontsize=14)
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(f"./{input_folder}/{metric.lower()}_correlation_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()

def analyze_scores():
    """Main function to analyze score data from JSON files."""
    # Paths to the JSON files
    current_file = f"./{input_folder}/result_score_diff.json"
    # Load data
    current_data = load_json_data(current_file)
    
    if current_data:
        current_mode_scores = extract_mode_scores(current_data)
        
        # Plot score distributions
        plot_score_distributions(current_mode_scores, "Score Distributions by Mode")
        
        # Calculate correlations for current data
        current_correlations = calculate_correlations(current_mode_scores)

        # Create correlation heatmaps
        plot_correlation_heatmap(current_correlations)

        # Print correlation results
        print("Correlation Analysis Results:")
        for metric, correlations in current_correlations.items():
            print(f"\n{metric} Correlations:")
            for comparison, value in correlations.items():
                print(f"  {comparison}: {value:.4f}")

if __name__ == "__main__":
    input_folder = int(input("Enter the input folder number (e.g., 10): "))
    analyze_scores()
    # for input_folder in range(1, 13):
    #     print(f"Analyzing folder {input_folder}...")
        # analyze_scores()

