
import json
import numpy as np
import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_course_std_dev(base_path=None):
    """
    Calculate standard deviation for each course across multiple evaluations
    
    Args:
        base_path: Path to the root directory containing experiment data
    """
    if base_path is None:
        base_path = Path("./repeat")
    else:
        base_path = Path(base_path)
    
    files = sorted(base_path.glob("*.json"))
        # Group files by courseId
    course_files = {}
    for file_path in files:
        # Parse the filename to get courseId
        match = re.match(r'(.+)_\d+\.json', file_path.name)
        if match:
            course_id = match.group(1)
            if course_id not in course_files:
                course_files[course_id] = []
            course_files[course_id].append(file_path)
    
    results = []
    
    # Calculate standard deviation for each course
    for course_id, file_paths in course_files.items():
        if len(file_paths) <= 1:
            print(f"Course {course_id}: Not enough files for std calculation")
            continue
        
        # Collect scores for each SDG goal across files
        sdg_scores = {}
        
        for file_path in file_paths:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                for sdg, sdg_data in data.items():
                    if 'score' in sdg_data:
                        if sdg not in sdg_scores:
                            sdg_scores[sdg] = []
                        sdg_scores[sdg].append(float(sdg_data['score']))
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")

        # Calculate standard deviation and mean for each SDG goal
        std_devs = {}
        means = {}
        for sdg, scores in sdg_scores.items():
            if len(scores) > 1:  # Need at least 2 points for std dev
                std_devs[sdg] = np.std(scores, ddof=1)  # ddof=1 for sample std dev
                means[sdg] = np.mean(scores)
        
        # Average standard deviation and mean across all SDGs
        if std_devs:
            avg_std_dev = sum(std_devs.values()) / len(std_devs)
            avg_mean = sum(means.values()) / len(means)
            print(f"Course {course_id}:")
            print(f"  Average std dev = {avg_std_dev:.4f}")
            print(f"  Average mean = {avg_mean:.4f}")
            
            # Print standard deviation for each SDG
            print(f"  Per-SDG standard deviations:")
            for sdg, std_val in std_devs.items():
                print(f"    {sdg}: std={std_val:.4f}, mean={means[sdg]:.4f}")
            
            # Store results
            results.append({
                'course_id': course_id,
                'avg_std_dev': avg_std_dev,
                'avg_mean': avg_mean,
                'std_devs': std_devs,
                'means': means
            })
        else:
            print(f"Course {course_id}: Unable to calculate std dev")
    
    return results


def generate_std_tables(results):
    """
    Generate tables showing standard deviations for each SDG across courses
    
    Args:
        results: List of dictionaries containing course results
    """
    if not results:
        print("No results to display")
        return
    
    # Get the list of all SDGs across all courses
    all_sdgs = set()
    for result in results:
        all_sdgs.update(result['std_devs'].keys())
    
    all_sdgs = sorted(list(all_sdgs))
    
    # Create DataFrame for standard deviations
    std_data = {'Course': []}
    mean_data = {'Course': []}
    
    for sdg in all_sdgs:
        std_data[sdg] = []
        mean_data[sdg] = []
    
    for result in results:
        std_data['Course'].append(result['course_id'])
        mean_data['Course'].append(result['course_id'])
        
        for sdg in all_sdgs:
            if sdg in result['std_devs']:
                std_data[sdg].append(f"{result['std_devs'][sdg]:.4f}")
                mean_data[sdg].append(f"{result['means'][sdg]:.4f}")
            else:
                std_data[sdg].append("N/A")
                mean_data[sdg].append("N/A")
    
    # Create DataFrames
    std_df = pd.DataFrame(std_data)
    mean_df = pd.DataFrame(mean_data)
    
    # Print tables
    print("\n--- Standard Deviation Table ---")
    print(std_df.to_string(index=False))
    
    print("\n--- Mean Table ---")
    print(mean_df.to_string(index=False))
    
    # Save tables to CSV
    std_df.to_csv("sdg_std_table.csv", index=False)
    mean_df.to_csv("sdg_mean_table.csv", index=False)
    print("\nTables saved as 'sdg_std_table.csv' and 'sdg_mean_table.csv'")
    
    return std_df, mean_df

def generate_heatmaps(std_df, mean_df):
    """
    Generate heatmaps for standard deviation and mean values
    
    Args:
        std_df: DataFrame containing standard deviation values
        mean_df: DataFrame containing mean values
    """
    try:
        
        # Convert string values to float for both dataframes
        std_numeric = std_df.copy()
        mean_numeric = mean_df.copy()
        
        # Keep course column as is
        course_col = std_df['Course']
        
        # Convert other columns to numeric, errors will become NaN
        for col in std_df.columns:
            if col != 'Course':
                std_numeric[col] = pd.to_numeric(std_df[col], errors='coerce')
                mean_numeric[col] = pd.to_numeric(mean_df[col], errors='coerce')
        
        # Set up the matplotlib figure
        plt.figure(figsize=(14, 12))
        
        # Create heatmap for standard deviations
        plt.subplot(2, 1, 1)
        std_pivot = std_numeric.drop('Course', axis=1)
        std_pivot.index = course_col
        sns.heatmap(std_pivot, annot=True, cmap="YlOrRd", fmt=".2f", linewidths=.5, 
                    cbar_kws={'label': 'Standard Deviation'})
        plt.title('Standard Deviation Heatmap by Course and SDG Goal')
        plt.tight_layout()
        
        # Create heatmap for means
        plt.subplot(2, 1, 2)
        mean_pivot = mean_numeric.drop('Course', axis=1)
        mean_pivot.index = course_col
        sns.heatmap(mean_pivot, annot=True, cmap="viridis", fmt=".2f", linewidths=.5,
                    cbar_kws={'label': 'Mean Score'})
        plt.title('Mean Score Heatmap by Course and SDG Goal')
        
        plt.tight_layout()
        plt.savefig('sdg_heatmaps_GPT.png', dpi=300, bbox_inches='tight')
        print("Heatmaps saved as 'sdg_heatmaps.png'")
        
    except ImportError:
        print("Could not generate heatmaps. Please install matplotlib and seaborn: pip install matplotlib seaborn")





if __name__ == "__main__":
    results = calculate_course_std_dev(base_path="./地政_GPT_tmp_NaN/")
    # results = calculate_course_std_dev(base_path="./地政_GPT_tmp_NaN")
    std_df, mean_df = generate_std_tables(results)
    generate_heatmaps(std_df, mean_df)
    # calculate_course_std_dev(base_path="./地政_Gemini_tmp_1")
