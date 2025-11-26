import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from collections import OrderedDict

# --- Configuration ---
# User should fill in the output path
INPUT_JSON_PATH = 'combined_sdg_details.json'
OUTPUT_IMAGE_PATH = 'whole_university_sdg_analysis.png' # 圖片輸出位置 (User can change this)
SCORE_THRESHOLD = 8.99

# --- SDG Mappings and Plotting details ---
SDG_MAPPING = OrderedDict([
    ("No Poverty", "SDG1 消除貧窮"),
    ("Zero Hunger", "SDG2 消除飢餓"),
    ("Good Health and Well-being", "SDG3 健康與福祉"),
    ("Quality Education", "SDG4 優質教育"),
    ("Gender Equality", "SDG5 性別平等"),
    ("Clean Water and Sanitation", "SDG6 淨水與衛生"),
    ("Affordable and Clean Energy", "SDG7 可負擔能源"),
    ("Decent Work and Economic Growth", "SDG8 就業與經濟成長"),
    ("Industry, Innovation and Infrastructure", "SDG9 工業、創新基礎建設"),
    ("Reduced Inequalities", "SDG10 減少不平等"),
    ("Sustainable Cities and Communities", "SDG11 永續城市"),
    ("Responsible Consumption and Production", "SDG12 責任消費與生產"),
    ("Climate Action", "SDG13 氣候行動"),
    ("Life Below Water", "SDG14 海洋生態"),
    ("Life on Land", "SDG15 陸地生態"),
    ("Peace, Justice and Strong Institutions", "SDG16 和平與正義制度"),
    ("Partnerships for the Goals", "SDG17 全球夥伴")
])

# Colors sampled from the provided image
SDG_COLORS = [
    '#55d1c8', '#42b6ae', '#3d9ec2', '#345e9d', '#8d479c', '#ce6ca3', '#d94761',
    '#f26f55', '#f89a43', '#fabe39', '#f2d53c', '#b3d145', '#76c15a', '#34a77b',
    '#008b80', '#006a6a', '#004958'
]

# Set font that supports Chinese characters
# Setting a list of fonts for better compatibility
try:
    mpl.rcParams['font.sans-serif'] = ['PingFang TC', 'Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']
    mpl.rcParams['axes.unicode_minus'] = False # To handle minus sign properly
except Exception as e:
    print(f"Could not set Chinese font: {e}. The plot may not display characters correctly.")

def analyze_and_plot(data_path, output_path):
    """
    Loads combined course data, analyzes SDG scores, and generates a bar chart.
    """
    # 1. Load data
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{data_path}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{data_path}'")
        return

    total_courses = len(data)
    if total_courses == 0:
        print("No course data to analyze.")
        return
        
    # 2. Process data: Count courses for each SDG meeting the threshold
    sdg_counts = {sdg_en: 0 for sdg_en in SDG_MAPPING.keys()}

    for course_data in data.values():
        for sdg_en, sdg_details in course_data.items():
            # Check if the SDG from the file is one we are tracking
            if sdg_en in sdg_counts and sdg_details.get('score') is not None:
                if sdg_details['score'] > SCORE_THRESHOLD:
                    sdg_counts[sdg_en] += 1
    
    # 3. Prepare for plotting
    sdg_labels_ch = list(SDG_MAPPING.values())
    counts = list(sdg_counts.values())
    
    # 4. Generate plot
    fig, ax = plt.subplots(figsize=(12, 8))

    y_pos = np.arange(len(sdg_labels_ch))
    ax.barh(y_pos, counts, align='center', color=SDG_COLORS)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sdg_labels_ch)
    ax.invert_yaxis()  # Invert axis to have SDG1 at the top
    
    ax.set_xlabel('課程數', fontsize=12)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', length=0, labelsize=10) # Hide y-axis ticks

    # Remove chart borders for a cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Add data labels (count and percentage) to the right of the bars
    for i, (count, label) in enumerate(zip(counts, sdg_labels_ch)):
        percentage = (count / total_courses) * 100 if total_courses > 0 else 0
        ax.text(count + 5, i, f' {count}  ({percentage:.2f}%)', va='center', ha='left', fontsize=10)

    plt.tight_layout()
    
    # 5. Save plot
    try:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Analysis plot saved to '{output_path}'")
    except Exception as e:
        print(f"Error saving plot: {e}")

if __name__ == '__main__':
    # The user mentioned they will write the output path themselves.
    # The input path is based on the previous script's output.
    analyze_and_plot(data_path=INPUT_JSON_PATH, output_path=OUTPUT_IMAGE_PATH)
