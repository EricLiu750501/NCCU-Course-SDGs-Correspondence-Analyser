import json
import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from sdg_summary import SDG_MAPPING

# 🔹 Kullback–Leibler Divergence
def kl_divergence(p, q):
    """計算 KL Divergence: KL(P || Q)"""
    p = np.array(p, dtype=np.float64)
    q = np.array(q, dtype=np.float64)
    
    # 正規化成機率分布
    p /= p.sum()
    q /= q.sum()
    
    # 避免 log(0) → 做平滑
    eps = 1e-12
    p = np.clip(p, eps, 1)
    q = np.clip(q, eps, 1)
    
    return np.sum(p * np.log(p / q))

# 🔹 Jensen–Shannon Divergence
def js_divergence(p, q):
    """計算 Jensen–Shannon Divergence"""
    p = np.array(p, dtype=np.float64)
    q = np.array(q, dtype=np.float64)
    
    # 正規化成機率分布
    p /= p.sum()
    q /= q.sum()
    
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)

def calculate_divergences(statistics):
    """Calculate KL and JS divergences between different score distributions"""
    # Get all SDGs that have scores for all four categories
    all_sdgs = set()
    for score_type in statistics.values():
        all_sdgs.update(score_type.keys())
    
    # We need common SDGs across all score types
    common_sdgs = []
    for sdg in all_sdgs:
        if all(sdg in statistics[score_type] for score_type in statistics):
            common_sdgs.append(sdg)
    
    common_sdgs = sorted(common_sdgs,
                    key=lambda x: int(SDG_MAPPING.get(x, "SDG_99").replace("SDG_", "")) if SDG_MAPPING.get(x) else 99)
    
    # Create distribution vectors for each score type
    distributions = {}
    for score_type in statistics:
        distributions[score_type] = [statistics[score_type][sdg]["mean"] for sdg in common_sdgs]
    
    # Calculate divergences
    divergences = {
        "KL": {},
        "JS": {}
    }
    
    comparisons = [
        ("gpt_original", "gemini_original"),
        ("gpt_judge_final", "gemini_judge_final"),
        ("gpt_original", "gpt_judge_final"),
        ("gemini_original", "gemini_judge_final")
    ]
    
    for dist1, dist2 in comparisons:
        kl_p_q = kl_divergence(distributions[dist1], distributions[dist2])
        kl_q_p = kl_divergence(distributions[dist2], distributions[dist1])
        js = js_divergence(distributions[dist1], distributions[dist2])
        
        divergences["KL"][(dist1, dist2)] = kl_p_q
        divergences["KL"][(dist2, dist1)] = kl_q_p
        divergences["JS"][(dist1, dist2)] = js
        divergences["JS"][(dist2, dist1)] = js  # JS is symmetric
    
    return divergences


def plot_divergences(divergences, output_path="sdg_divergences.png"):
    """Create a bar chart showing KL and JS divergences between distributions"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Define the comparisons to show
    comparisons = [
        ("gpt_original", "gemini_original"),
        ("gpt_judge_final", "gemini_judge_final"),
        ("gpt_original", "gpt_judge_final"),
        ("gemini_original", "gemini_judge_final")
    ]
    
    labels = [
        "GPT vs Gemini (Original)",
        "GPT vs Gemini (Judge Final)",
        "GPT: Original vs Judge",
        "Gemini: Original vs Judge"
    ]
    
    # Plot KL divergences
    kl_values = [divergences["KL"][(comp[0], comp[1])] for comp in comparisons]
    kl_values_reverse = [divergences["KL"][(comp[1], comp[0])] for comp in comparisons]
    
    x = np.arange(len(labels))
    width = 0.35
    
    ax1.bar(x - width/2, kl_values, width, label='KL(P||Q)')
    ax1.bar(x + width/2, kl_values_reverse, width, label='KL(Q||P)')
    
    ax1.set_title('KL Divergence Between Score Distributions')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, axis='y', alpha=0.3)
    
    # Plot JS divergences
    js_values = [divergences["JS"][(comp[0], comp[1])] for comp in comparisons]
    
    ax2.bar(x, js_values, width=0.6)
    ax2.set_title('JS Divergence Between Score Distributions')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=45, ha='right')
    ax2.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Divergences plot saved to: {output_path}")

def load_all_json_data(directory_path):
    """Load all JSON files in the given directory"""
    json_files = glob.glob(os.path.join(directory_path, "*.json"))
    data_list = []
    
    for file_path in json_files:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                data_list.append(data)
                print(f"Loaded: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return data_list

def extract_scores_from_data(data_list):
    """Extract all scores from the data list"""
    all_scores = {
        "gpt_original": defaultdict(list),
        "gemini_original": defaultdict(list),
        "gpt_judge_final": defaultdict(list),
        "gemini_judge_final": defaultdict(list)
    }
    
    # Collect scores from all files
    for data in data_list:
        # Get all SDGs in this data file
        try:
            sdgs = list(data["gpt_answer"].keys())
            
            # Extract original scores
            for sdg in sdgs:
                all_scores["gpt_original"][sdg].append(data["gpt_answer"][sdg]["score"])
                all_scores["gemini_original"][sdg].append(data["gemini_answer"][sdg]["score"])
            
            # Calculate final scores for each judge
            for sdg in sdgs:
                # Extract critique suggestions
                gpt_critique_score = None
                gemini_critique_score = None
                
                if "suggested_changes" in data["gpt_critique"]:
                    for sdg_key, change in data["gpt_critique"]["suggested_changes"].items():
                        # Match SDG name or number
                        if (sdg_key == sdg or 
                            SDG_MAPPING.get(sdg) == sdg_key or 
                            sdg == SDG_MAPPING.get(sdg_key)):
                            gpt_critique_score = change["new_score"]
                            break
                
                if "suggested_changes" in data["gemini_critique"]:
                    for sdg_key, change in data["gemini_critique"]["suggested_changes"].items():
                        # Match SDG name or number
                        if (sdg_key == sdg or 
                            SDG_MAPPING.get(sdg) == sdg_key or 
                            sdg == SDG_MAPPING.get(sdg_key)):
                            gemini_critique_score = change["new_score"]
                            break
                
                # Get judge decisions
                gpt_winner = data["gpt_judge_final"][sdg]["winner"]
                gemini_winner = data["gemini_judge_final"][sdg]["winner"]
                
                # Calculate final scores based on judge decisions
                gpt_score = data["gpt_answer"][sdg]["score"]
                gemini_score = data["gemini_answer"][sdg]["score"]
                
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
                
                all_scores["gpt_judge_final"][sdg].append(gpt_final)
                all_scores["gemini_judge_final"][sdg].append(gemini_final)
                
        except Exception as e:
            print(f"Error processing data: {e}")
            continue
    
    return all_scores

def calculate_statistics(all_scores):
    """Calculate mean and standard deviation for each score type and SDG"""
    statistics = {
        "gpt_original": {},
        "gemini_original": {},
        "gpt_judge_final": {},
        "gemini_judge_final": {}
    }
    
    for score_type, sdg_scores in all_scores.items():
        for sdg, scores in sdg_scores.items():
            if scores:  # Only if we have scores for this SDG
                statistics[score_type][sdg] = {
                    "mean": np.mean(scores),
                    "std": np.std(scores),
                    "count": len(scores)
                }
    
    return statistics

def plot_average_scores(statistics, output_path="average_sdg_scores.png"):
    course_num = statistics['gpt_original']['No Poverty']['count']
    
    """Create a bar chart showing average scores with error bars"""
    # Get all unique SDGs across all statistics
    all_sdgs = set()
    for score_type in statistics.values():
        all_sdgs.update(score_type.keys())
    
    # Sort SDGs in standard order
    all_sdgs = sorted(list(all_sdgs), 
                     key=lambda x: int(SDG_MAPPING.get(x, "SDG_99").replace("SDG_", "")) if SDG_MAPPING.get(x) else 99)
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Define bar positions and width
    bar_width = 0.2
    index = np.arange(len(all_sdgs))
    
    # Define score types, colors and labels
    score_types = [
        ("gpt_original", "royalblue", "GPT Original"),
        ("gemini_original", "coral", "Gemini Original"),
        ("gpt_judge_final", "forestgreen", "GPT Judge Final"),
        ("gemini_judge_final", "purple", "Gemini Judge Final")
    ]
    
    # Plot bars for each score type
    for i, (score_type, color, label) in enumerate(score_types):
        means = []
        errors = []
        
        for sdg in all_sdgs:
            if sdg in statistics[score_type]:
                means.append(statistics[score_type][sdg]["mean"])
                errors.append(statistics[score_type][sdg]["std"])
            else:
                means.append(0)
                errors.append(0)
        
        # Position the bars side by side
        position = index + (i - 1.5) * bar_width
        
        # Plot bars
        ax.bar(position, means, width=bar_width, label=label, color=color, alpha=0.8)
        # Add error bars if needed
        # ax.errorbar(position, means, yerr=errors, fmt='none', ecolor='black', capsize=3)
    
    # Add labels and legend
    ax.set_title(f'Average SDG Scores Comparison for Land Economic  ({course_num} courses)', fontsize=16)
    ax.set_xlabel('Sustainable Development Goals (SDGs)')
    ax.set_ylabel('Average Score')
    ax.set_xticks(index)
    ax.set_xticklabels([f"{int(SDG_MAPPING.get(sdg, '99').replace('SDG_', ''))}. {sdg}" for sdg in all_sdgs], rotation=45, ha='right', fontsize=10)
    ax.set_ylim(0, 10.5)
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot saved to: {output_path}")

def main():
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = "."
    
    # Load all JSON data
    data_list = load_all_json_data(directory_path)
    
    if not data_list:
        print("No valid JSON files found.")
        return
    
    # Extract and process scores
    all_scores = extract_scores_from_data(data_list)
    statistics = calculate_statistics(all_scores)
    
    # Print summary statistics
    print("\nAverage Scores Summary:")
    print("=" * 80)
    print(f"{'SDG':<40} {'GPT Orig':<12} {'Gemini Orig':<12} {'GPT Final':<12} {'Gemini Final':<12}")
    print("-" * 80)
    
    # Get all SDGs and sort them
    all_sdgs = set()
    for score_type in statistics.values():
        all_sdgs.update(score_type.keys())
    
    sorted_sdgs = sorted(all_sdgs, 
                        key=lambda x: int(SDG_MAPPING.get(x, "SDG_99").replace("SDG_", "")) if SDG_MAPPING.get(x) else 99)
    
    for sdg in sorted_sdgs:
        gpt_orig = f"{statistics['gpt_original'].get(sdg, {}).get('mean', 'N/A'):.3f}" if sdg in statistics['gpt_original'] else "N/A"
        gemini_orig = f"{statistics['gemini_original'].get(sdg, {}).get('mean', 'N/A'):.3f}" if sdg in statistics['gemini_original'] else "N/A"
        gpt_final = f"{statistics['gpt_judge_final'].get(sdg, {}).get('mean', 'N/A'):.3f}" if sdg in statistics['gpt_judge_final'] else "N/A"
        gemini_final = f"{statistics['gemini_judge_final'].get(sdg, {}).get('mean', 'N/A'):.3f}" if sdg in statistics['gemini_judge_final'] else "N/A"
        
        print(f"{sdg:<40} {gpt_orig:<12} {gemini_orig:<12} {gpt_final:<12} {gemini_final:<12}")
    
    # Plot the results
    output_path = os.path.join(os.path.abspath(directory_path), "average_sdg_scores.png")
    plot_average_scores(statistics, output_path)
    
    # Calculate and print divergences
    print("\nDistribution Divergences:")
    print("=" * 80)
    divergences = calculate_divergences(statistics)
    
    for div_type in ["KL", "JS"]:
        print(f"\n{div_type} Divergence:")
        for (dist1, dist2), value in divergences[div_type].items():
            print(f"{dist1} vs {dist2}: {value:.4f}")
    
    # Plot divergences
    div_output_path = os.path.join(os.path.abspath(directory_path), "sdg_divergences.png")
    plot_divergences(divergences, div_output_path)

if __name__ == "__main__":
    main()

