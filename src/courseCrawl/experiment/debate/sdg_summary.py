import json

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


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def format_summary_table(data):
    """Create a formatted summary table of all scores and final decisions"""
    
    # Get all SDGs
    sdgs = list(data["gpt_answer"].keys())
    
    # Extract GPT and Gemini original scores
    gpt_scores = {sdg: data["gpt_answer"][sdg]["score"] for sdg in sdgs}
    gemini_scores = {sdg: data["gemini_answer"][sdg]["score"] for sdg in sdgs}
    
    # Extract critique suggestions
    gpt_critique = {}
    if "suggested_changes" in data["gpt_critique"]:
        for sdg_key, change in data["gpt_critique"]["suggested_changes"].items():
            # Try to find this SDG in our list of SDGs
            matching_sdg = None
            for sdg in sdgs:
                # Check if the key matches the SDG name or number
                if (sdg_key == sdg or 
                    SDG_MAPPING.get(sdg) == sdg_key or 
                    sdg == SDG_MAPPING.get(sdg_key)):
                    matching_sdg = sdg
                    break
            if matching_sdg:
                gpt_critique[matching_sdg] = change["new_score"]
    
    gemini_critique = {}
    if "suggested_changes" in data["gemini_critique"]:
        for sdg_key, change in data["gemini_critique"]["suggested_changes"].items():
            # Try to find this SDG in our list of SDGs
            matching_sdg = None
            for sdg in sdgs:
                # Check if the key matches the SDG name or number
                if (sdg_key == sdg or 
                    SDG_MAPPING.get(sdg) == sdg_key or 
                    sdg == SDG_MAPPING.get(sdg_key)):
                    matching_sdg = sdg
                    break
            if matching_sdg:
                gemini_critique[matching_sdg] = change["new_score"]

    # print(gpt_critique)
    # print(gemini_critique)
    
    # Get judge decisions
    gpt_judge_decisions = {sdg: data["gpt_judge_final"][sdg]["winner"] for sdg in sdgs}
    gemini_judge_decisions = {sdg: data["gemini_judge_final"][sdg]["winner"] for sdg in sdgs}

    def final_scores(judge_decisions): 
        # Calculate final scores
        final_scores = {}
        for sdg in sdgs:
            gpt_score = gpt_scores[sdg]
            gemini_score = gemini_scores[sdg]
            
            gpt_critique_score = gpt_critique.get(sdg, None)
            gemini_critique_score = gemini_critique.get(sdg, None)
            
            winner = judge_decisions[sdg]
            
            if winner == "A":
                if gemini_critique_score is not None:
                    final_scores[sdg] = (gpt_score + gemini_critique_score) / 2
                else:
                    final_scores[sdg] = gpt_score
            elif winner == "B":
                if gpt_critique_score is not None:
                    final_scores[sdg] = (gemini_score + gpt_critique_score) / 2
                else:
                    final_scores[sdg] = gemini_score
            else:  # Tie
                scores = [s for s in [gpt_score, gemini_score, gpt_critique_score, gemini_critique_score] if s is not None]
                final_scores[sdg] = sum(scores) / len(scores)
        return final_scores

    gpt_final_scores = final_scores(gpt_judge_decisions)
    gemini_final_scores = final_scores(gemini_judge_decisions)
    
    # Create and format the table
    header = ["SDG", "GPT Score", "Gemini Score", "GPT Critique", "Gemini Critique", "GPT/Gemini Winner", "GPT FS", "Gemini Final Score"]
    rows = []
    
    for sdg in sdgs:
        row = [
            sdg,
            f"{gpt_scores[sdg]:.3f}",
            f"{gemini_scores[sdg]:.3f}",
            f"{gpt_critique.get(sdg, 'N/A')}" if sdg in gpt_critique else "N/A",
            f"{gemini_critique.get(sdg, 'N/A')}" if sdg in gemini_critique else "N/A",
            gpt_judge_decisions[sdg],
            gemini_judge_decisions[sdg],
            f"{gpt_final_scores[sdg]:.3f}",
            f"{gemini_final_scores[sdg]:.3f}"
        ]
        rows.append(row)
    
    return header, rows, gpt_final_scores, gemini_final_scores


def plot_sdg_scores(gpt_scores, gemini_scores, gpt_final_scores, gemini_final_scores, output_path=None):
    """
    Create a bar chart showing original scores and final scores for each SDG.
    
    Args:
        gpt_scores: Dictionary of original GPT scores
        gemini_scores: Dictionary of original Gemini scores
        gpt_final_scores: Dictionary of GPT judge's final scores
        gemini_final_scores: Dictionary of Gemini judge's final scores
        output_path: Path to save the plot (default is current directory)
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    
    # Get all SDGs and sort them in standard order
    all_sdgs = sorted(list(set(list(gpt_scores.keys()) + list(gemini_scores.keys()))), 
                     key=lambda x: int(SDG_MAPPING.get(x, "SDG_99").replace("SDG_", "")) if SDG_MAPPING.get(x) else 99)
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Width of each bar group and individual bars
    group_width = 0.8  # width of the entire group of bars for one SDG
    bar_width = group_width / 4  # width for 4 types of scores
    
    # Colors for different score types
    colors = ['royalblue', 'darkorange', 'forestgreen', 'firebrick']
    
    # Plot bars for each score type
    for i, (scores, label, color) in enumerate([
        (gpt_scores, 'GPT Original', colors[0]),
        (gemini_scores, 'Gemini Original', colors[1]),
        (gpt_final_scores, 'GPT Judge Final', colors[2]),
        (gemini_final_scores, 'Gemini Judge Final', colors[3])
    ]):
        x_positions = [j + (i - 1.5) * bar_width for j in range(len(all_sdgs))]
        y_values = [scores.get(sdg, 0) for sdg in all_sdgs]
        ax.bar(x_positions, y_values, width=bar_width, label=label, color=color, alpha=0.8)
    
    # Add labels and legend
    ax.set_title('SDG Scores Comparison', fontsize=16)
    ax.set_xlabel('SDGs', fontsize=14)
    ax.set_ylabel('Score', fontsize=14)
    ax.set_xticks(range(len(all_sdgs)))
    ax.set_xticklabels([f"{sdg}\n({SDG_MAPPING.get(sdg, '')})" for sdg in all_sdgs], rotation=45, ha='right', fontsize=10)
    ax.set_ylim(0, 10.5)
    ax.grid(True, axis='y', alpha=0.3)
    ax.legend(fontsize=12)
    
    plt.tight_layout()
    
    # Save or show the plot
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        plt.savefig(os.path.join(current_dir, "sdg_scores_comparison.png"), dpi=300, bbox_inches='tight')
    
    plt.close()




def main():
    import os
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "./923882001_2.json"
    
    data = load_json_data(file_path)
    header, rows, gpt_final_scores, gemini_final_scores = format_summary_table(data)
    
    # Extract original scores for plotting
    sdgs = list(data["gpt_answer"].keys())
    gpt_scores = {sdg: data["gpt_answer"][sdg]["score"] for sdg in sdgs}
    gemini_scores = {sdg: data["gemini_answer"][sdg]["score"] for sdg in sdgs}
    
    # Print the formatted table
    print(f"{header[0]:<40} {header[1]:<12} {header[2]:<12} {header[3]:<15} {header[4]:<15} {header[5]:<6} {header[6]:<6} {header[7]:<15} ")
    print("-" * 130)
    
    for row in rows:
        print(f"{row[0]:<40} {row[1]:<12} {row[2]:<12} {row[3]:<15} {row[4]:<15} {row[5]:<6} {row[6]:<6} {row[7]:<15} {row[8]:<15}")
    
    print("\nFinal SDG Scores Summary:")
    for sdg in sorted(gpt_final_scores.keys()):
        print(f"{sdg:<40}: GPT: {gpt_final_scores[sdg]:.3f}  Gemini: {gemini_final_scores[sdg]:.3f}")
    
    # Generate and save the plot
    output_filename = os.path.splitext(os.path.basename(file_path))[0] + "_plot.png"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
    plot_sdg_scores(gpt_scores, gemini_scores, gpt_final_scores, gemini_final_scores, output_path)
    print(f"\nPlot saved to: {output_path}")
    

if __name__ == "__main__":
    main()

