import matplotlib.pyplot as plt
import numpy as np
import math
from wordcloud import WordCloud # Added for C. Keyword Analysis

import json
import os
import glob
import pandas as pd # Added for department info

SDG_NAMES = [
    "1. No Poverty", "2. Zero Hunger", "3. Good Health and Well-being",
    "4. Quality Education", "5. Gender Equality", "6. Clean Water and Sanitation",
    "7. Affordable and Clean Energy", "8. Decent Work and Economic Growth",
    "9. Industry, Innovation and Infrastructure", "10. Reduced Inequalities",
    "11. Sustainable Cities and Communities", "12. Responsible Consumption and Production",
    "13. Climate Action", "14. Life Below Water", "15. Life on Land",
    "16. Peace, Justice and Strong Institutions", "17. Partnerships for the Goals"
]

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
                data["file_path"] = file_path # Add file_path to the data
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
    
    plt.savefig(f"plots/{model_name}_{college_name.replace(' ', '_')}_avg_scores.png")
    plt.close()

def plot_radar_chart(data, model_name="", title=""):
    labels = list(data.keys())
    stats = list(data.values())

    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    angles += angles[:1]
    stats += stats[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='red', alpha=0.25)
    ax.plot(angles, stats, color='red', linewidth=2)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='grey', size=10)
    ax.set_ylim(0, 10)

    ax.set_title(title, va='bottom')
    plt.tight_layout()
    plt.savefig(f"plots/{title.replace(' ', '_').replace('(', '').replace(')', '')}_{model_name}_radar.png")
    plt.close()

def analyze_university_sdg_coverage(all_courses_data, model_name="Gemini-2.5-flash", threshold=5.0):
    # Filter for the chosen model
    model_judge_key = "gemini_judge_final" if model_name == "Gemini-2.5-flash" else "gpt_judge_final"

    # Output 1: Courses related to at least one SDG
    courses_with_any_sdg = 0
    for course_data in all_courses_data:
        if any(sdg_info["final_score"] > threshold for sdg_info in course_data[model_judge_key].values()):
            courses_with_any_sdg += 1

    total_courses = len(all_courses_data)
    percentage_with_any_sdg = (courses_with_any_sdg / total_courses) * 100 if total_courses > 0 else 0

    print(f"\n--- University SDG Coverage ({model_name}) ---")
    print(f"Total courses analyzed: {total_courses}")
    print(f"Courses related to at least one SDG (score > {threshold}): {courses_with_any_sdg} ({percentage_with_any_sdg:.2f}%)")

    # Plot 1: Bar chart for courses related to at least one SDG
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.bar(["Courses with >=1 SDG"], [percentage_with_any_sdg], color='lightgreen')
    ax1.set_ylim(0, 100)
    ax1.set_ylabel('Percentage (%)')
    ax1.set_title(f'University SDG Coverage ({model_name})')
    plt.tight_layout()
    plt.savefig(f"plots/University_SDG_Coverage_{model_name.replace(' ', '_')}.png")
    plt.close()

    # Output 2: Courses related to each SDG
    sdg_course_counts = {sdg: 0 for sdg in SDG_NAMES}
    for course_data in all_courses_data:
        for sdg_name_full in SDG_NAMES:
            # Extract the base SDG name from the full name (e.g., "1. No Poverty" -> "No Poverty")
            sdg_name_base = sdg_name_full.split('. ', 1)[1]
            # Find the corresponding key in the judge_final dictionary (case-insensitive match)
            found_sdg_key = None
            for key in course_data[model_judge_key].keys():
                if key.lower() == sdg_name_base.lower():
                    found_sdg_key = key
                    break

            if found_sdg_key and course_data[model_judge_key][found_sdg_key]["final_score"] > threshold:
                sdg_course_counts[sdg_name_full] += 1

    print("\nCourses related to each SDG (absolute count):")
    for sdg, count in sdg_course_counts.items():
        print(f"{sdg}: {count} courses")

    # Plot 2: Bar chart for courses related to each SDG
    fig2, ax2 = plt.subplots(figsize=(15, 8))
    ax2.bar(sdg_course_counts.keys(), sdg_course_counts.values(), color='skyblue')
    ax2.set_ylabel('Number of Courses')
    ax2.set_title(f'Number of Courses Related to Each SDG (University-wide, {model_name})')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"plots/University_Courses_per_SDG_{model_name.replace(' ', '_')}.png")
    plt.close()

def analyze_university_sdg_profile(all_courses_data, model_name="Gemini-2.5-flash"):
    print(f"\n--- University SDG Profile ({model_name}) ---")
    gemini_avg, gpt_avg = calculate_average_scores_final(all_courses_data)

    if model_name == "Gemini-2.5-flash":
        avg_scores = gemini_avg
    else:
        avg_scores = gpt_avg

    # Ensure the order of SDGs for plotting
    ordered_avg_scores = {sdg.split('. ', 1)[1]: avg_scores.get(sdg.split('. ', 1)[1], 0) for sdg in SDG_NAMES}

    print("Average scores for each SDG (University-wide):")
    for sdg, score in ordered_avg_scores.items():
        print(f"{sdg}: {score:.2f}")

    plot_radar_chart(ordered_avg_scores, model_name, f"University SDG Profile ({model_name})")

def analyze_course_sdg_density(all_courses_data, model_name="Gemini-2.5-flash", threshold=5.0):
    print(f"\n--- Course SDG Density Analysis ({model_name}) ---")
    model_judge_key = "gemini_judge_final" if model_name == "Gemini-2.5-flash" else "gpt_judge_final"

    sdg_counts_per_course = []
    for course_data in all_courses_data:
        sdg_count = 0
        for sdg_info in course_data[model_judge_key].values():
            if sdg_info["final_score"] > threshold:
                sdg_count += 1
        sdg_counts_per_course.append(sdg_count)

    # Plot histogram
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(sdg_counts_per_course, bins=range(max(sdg_counts_per_course) + 2), align='left', rwidth=0.8, color='purple')
    ax.set_xlabel(f'Number of Related SDGs (score > {threshold})')
    ax.set_ylabel('Number of Courses')
    ax.set_title(f'Course SDG Density Distribution (University-wide, {model_name})')
    ax.set_xticks(range(max(sdg_counts_per_course) + 2))
    plt.tight_layout()
    plt.savefig(f"plots/Course_SDG_Density_{model_name.replace(' ', '_')}.png")
    plt.close()

def add_department_info(all_courses_data, courses_df):
    course_id_to_dept = {}
    for index, row in courses_df.iterrows():
        course_id = str(row["科目代號\nCourse #"])
        department = str(row["開課系級\nDepartment and Level / Course School/Department"])
        course_id_to_dept[course_id] = department

    for course_data in all_courses_data:
        course_id = os.path.splitext(os.path.basename(course_data["file_path"]))[0] # Assuming file_path is added to course_data
        if course_id in course_id_to_dept:
            course_data["department"] = course_id_to_dept[course_id]
        else:
            course_data["department"] = "Unknown"
    return all_courses_data

def plot_department_sdg_heatmap(all_courses_data, model_name="Gemini-2.5-flash"):
    print(f"\n--- Department-SDG Heatmap Analysis ({model_name}) ---")
    model_judge_key = "gemini_judge_final" if model_name == "Gemini-2.5-flash" else "gpt_judge_final"

    department_sdg_scores = {}
    for course_data in all_courses_data:
        department = course_data.get("department", "Unknown")
        if department not in department_sdg_scores:
            department_sdg_scores[department] = {sdg: [] for sdg in SDG_NAMES}

        for sdg_name_full in SDG_NAMES:
            sdg_name_base = sdg_name_full.split('. ', 1)[1]
            found_sdg_key = None
            for key in course_data[model_judge_key].keys():
                if key.lower() == sdg_name_base.lower():
                    found_sdg_key = key
                    break
            if found_sdg_key:
                department_sdg_scores[department][sdg_name_full].append(course_data[model_judge_key][found_sdg_key]["final_score"])

    # Calculate average scores for each department-SDG pair
    department_sdg_avg_scores = {}
    for department, sdg_data in department_sdg_scores.items():
        department_sdg_avg_scores[department] = {
            sdg: np.mean(scores) if scores else 0 for sdg, scores in sdg_data.items()
        }

    # Convert to DataFrame for heatmap
    heatmap_df = pd.DataFrame.from_dict(department_sdg_avg_scores, orient='index')
    heatmap_df = heatmap_df[SDG_NAMES] # Ensure SDG order

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(18, max(8, len(heatmap_df) * 0.4)))
    cax = ax.matshow(heatmap_df, cmap='viridis')
    fig.colorbar(cax)

    ax.set_xticks(np.arange(len(SDG_NAMES)))
    ax.set_yticks(np.arange(len(heatmap_df.index)))
    ax.set_xticklabels(SDG_NAMES, rotation=90)
    ax.set_yticklabels(heatmap_df.index)

    ax.set_title(f'Department-SDG Average Score Heatmap ({model_name})')
    plt.tight_layout()
    plt.savefig(f"plots/Department_SDG_Heatmap_{model_name.replace(' ', '_')}.png")
    plt.close()

def find_top_courses_per_sdg(all_courses_data, model_name="Gemini-2.5-flash", target_sdg="Quality Education", top_n=10):
    print(f"\n--- Top {top_n} Courses for SDG: {target_sdg} ({model_name}) ---")
    model_judge_key = "gemini_judge_final" if model_name == "Gemini-2.5-flash" else "gpt_judge_final"

    course_sdg_scores = []
    for course_data in all_courses_data:
        course_id = os.path.splitext(os.path.basename(course_data["file_path"]))[0]
        department = course_data.get("department", "Unknown")
        
        # Find the correct SDG key (case-insensitive)
        found_sdg_key = None
        for key in course_data[model_judge_key].keys():
            if key.lower() == target_sdg.lower():
                found_sdg_key = key
                break

        if found_sdg_key:
            score = course_data[model_judge_key][found_sdg_key]["final_score"]
            course_sdg_scores.append({"course_id": course_id, "department": department, "score": score})

    # Sort by score in descending order
    course_sdg_scores.sort(key=lambda x: x["score"], reverse=True)

    # Print top N courses
    for i, course in enumerate(course_sdg_scores[:top_n]):
        print(f"{i+1}. Course ID: {course["course_id"]:<10} | Department: {course["department"]:<20} | Score: {course["score"]:.2f}")

def analyze_evidence_type(all_courses_data, model_name="Gemini-2.5-flash", threshold=5.0):
    print(f"\n--- Evidence Type Analysis ({model_name}) ---")
    model_answer_key = "gemini_answer" if model_name == "Gemini-2.5-flash" else "gpt_answer"
    model_judge_key = "gemini_judge_final" if model_name == "Gemini-2.5-flash" else "gpt_judge_final"

    evidence_type_counts = {"explicit": 0, "inferred": 0, "none": 0}

    for course_data in all_courses_data:
        for sdg_name_full in SDG_NAMES:
            sdg_name_base = sdg_name_full.split('. ', 1)[1]
            found_sdg_key = None
            for key in course_data[model_judge_key].keys():
                if key.lower() == sdg_name_base.lower():
                    found_sdg_key = key
                    break

            if found_sdg_key and course_data[model_judge_key][found_sdg_key]["final_score"] > threshold:
                evidence_type = course_data[model_answer_key][found_sdg_key]["evidence_type"]
                if evidence_type in evidence_type_counts:
                    evidence_type_counts[evidence_type] += 1
                else:
                    evidence_type_counts["none"] += 1 # Fallback for unexpected types

    total_relevant_evidence = sum(evidence_type_counts.values())
    print(f"Total relevant evidence entries: {total_relevant_evidence}")
    for etype, count in evidence_type_counts.items():
        percentage = (count / total_relevant_evidence) * 100 if total_relevant_evidence > 0 else 0
        print(f"{etype.capitalize()}: {count} ({percentage:.2f}%)")

    # Plot stacked bar chart
    labels = list(evidence_type_counts.keys())
    sizes = list(evidence_type_counts.values())

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightskyblue', 'lightgrey'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(f'Distribution of Evidence Types ({model_name})')
    plt.tight_layout()
    plt.close()

def analyze_keyword_wordcloud(all_courses_data, model_name="Gemini-2.5-flash", target_sdg="Responsible Consumption and Production", threshold=7.0):
    print(f"\n--- Keyword Analysis (Word Cloud) for SDG: {target_sdg} ({model_name}) ---")
    model_answer_key = "gemini_answer" if model_name == "Gemini-2.5-flash" else "gpt_answer"
    model_judge_key = "gemini_judge_final" if model_name == "Gemini-2.5-flash" else "gpt_judge_final"

    all_evidence_text = []
    for course_data in all_courses_data:
        # Find the correct SDG key (case-insensitive)
        found_sdg_key = None
        for key in course_data[model_judge_key].keys():
            if key.lower() == target_sdg.lower():
                found_sdg_key = key
                break

        if found_sdg_key and course_data[model_judge_key][found_sdg_key]["final_score"] > threshold:
            evidence_list = course_data[model_answer_key][found_sdg_key].get("evidence", [])
            all_evidence_text.extend(evidence_list)

    if not all_evidence_text:
        print(f"No high-scoring courses found for SDG {target_sdg} with score > {threshold}.")
        return

    text = " ".join(all_evidence_text)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Keyword Cloud for SDG {target_sdg} ({model_name}, Score > {threshold})')
    plt.tight_layout()
    # plt.close()
    plt.show()

def analyze_model_consistency(all_courses_data):
    print(f"\n--- Model Consistency Analysis (Inter-Rater Reliability) ---")
    gemini_scores_flat = []
    gpt_scores_flat = []

    for course_data in all_courses_data:
        for sdg_name_full in SDG_NAMES:
            sdg_name_base = sdg_name_full.split('. ', 1)[1]
            
            gemini_found_sdg_key = None
            for key in course_data["gemini_judge_final"].keys():
                if key.lower() == sdg_name_base.lower():
                    gemini_found_sdg_key = key
                    break
            
            gpt_found_sdg_key = None
            for key in course_data["gpt_judge_final"].keys():
                if key.lower() == sdg_name_base.lower():
                    gpt_found_sdg_key = key
                    break

            if gemini_found_sdg_key and gpt_found_sdg_key:
                gemini_scores_flat.append(course_data["gemini_judge_final"][gemini_found_sdg_key]["final_score"])
                gpt_scores_flat.append(course_data["gpt_judge_final"][gpt_found_sdg_key]["final_score"])

    if len(gemini_scores_flat) < 2:
        print("Not enough data points to calculate correlation.")
        return

    # # Calculate Pearson correlation
    # pearson_corr, _ = pearsonr(gemini_scores_flat, gpt_scores_flat)
    # print(f"Pearson Correlation Coefficient: {pearson_corr:.4f}")
    #
    # # Calculate Spearman correlation
    # spearman_corr, _ = spearmanr(gemini_scores_flat, gpt_scores_flat)
    # print(f"Spearman Correlation Coefficient: {spearman_corr:.4f}")

    # Plot scatter plot
    plt.figure(figsize=(8, 8))
    plt.scatter(gpt_scores_flat, gemini_scores_flat, alpha=0.5)
    plt.plot([0, 10], [0, 10], '--r') # y=x line
    plt.xlabel('GPT Final Score')
    plt.ylabel('Gemini Final Score')
    plt.title('Model Consistency: GPT vs. Gemini Final Scores')
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"plots/Model_Consistency_Scatter.png")
    plt.close()

def analyze_model_bias(all_courses_data):
    print(f"\n--- Model Bias Analysis ---")
    gemini_avg, gpt_avg = calculate_average_scores_final(all_courses_data)

    print("Average scores comparison:")
    for sdg_name_full in SDG_NAMES:
        sdg_name_base = sdg_name_full.split('. ', 1)[1]
        gemini_score = gemini_avg.get(sdg_name_base, 0)
        gpt_score = gpt_avg.get(sdg_name_base, 0)
        diff = gpt_score - gemini_score
        print(f"{sdg_name_full}: Gemini={gemini_score:.2f}, GPT={gpt_score:.2f}, Diff (GPT-Gemini)={diff:.2f}")

    # Identify SDGs with largest divergence
    divergences = []
    for sdg_name_full in SDG_NAMES:
        sdg_name_base = sdg_name_full.split('. ', 1)[1]
        gemini_score = gemini_avg.get(sdg_name_base, 0)
        gpt_score = gpt_avg.get(sdg_name_base, 0)
        divergences.append((sdg_name_full, abs(gpt_score - gemini_score)))

    divergences.sort(key=lambda x: x[1], reverse=True)
    print("\nSDGs with largest divergences:")
    for sdg, diff in divergences[:5]: # Top 5 divergences
        print(f"{sdg}: Absolute Difference={diff:.2f}")

    # Plotting the differences
    sdg_labels = [sdg.split('. ', 1)[1] for sdg in SDG_NAMES]
    gemini_scores = [gemini_avg.get(sdg, 0) for sdg in sdg_labels]
    gpt_scores = [gpt_avg.get(sdg, 0) for sdg in sdg_labels]

    x = np.arange(len(sdg_labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(15, 8))
    rects1 = ax.bar(x - width/2, gemini_scores, width, label='Gemini', color='red')
    rects2 = ax.bar(x + width/2, gpt_scores, width, label='GPT', color='blue')

    ax.set_ylabel('Average Score')
    ax.set_title('Average SDG Scores by Model')
    ax.set_xticks(x)
    ax.set_xticklabels(sdg_labels, rotation=45, ha='right')
    ax.legend()
    ax.set_ylim(0, 10)

    plt.tight_layout()
    plt.close()

def analyze_critique_impact(all_courses_data):
    print(f"\n--- Impact of Critique Step Analysis ---")

    gemini_revisions_count = 0
    gpt_revisions_count = 0
    total_sdg_evaluations = 0

    gemini_revision_magnitudes = []
    gpt_revision_magnitudes = []

    for course_data in all_courses_data:
        for sdg_name_full in SDG_NAMES:
            sdg_name_base = sdg_name_full.split('. ', 1)[1]
            total_sdg_evaluations += 1

            # Gemini Critique
            if "gemini_critique" in course_data and "revisions" in course_data["gemini_critique"]:
                for sdg_key, revision_info in course_data["gemini_critique"]["revisions"].items():
                    if sdg_key.lower() == sdg_name_base.lower():
                        gemini_revisions_count += 1
                        if "your_revised" in revision_info and "your_original" in revision_info:
                            magnitude = abs(revision_info["your_revised"] - revision_info["your_original"])
                            gemini_revision_magnitudes.append(magnitude)

            # GPT Critique
            if "gpt_critique" in course_data and "revisions" in course_data["gpt_critique"]:
                for sdg_key, revision_info in course_data["gpt_critique"]["revisions"].items():
                    if sdg_key.lower() == sdg_name_base.lower():
                        gpt_revisions_count += 1
                        if "your_revised" in revision_info and "your_original" in revision_info:
                            magnitude = abs(revision_info["your_revised"] - revision_info["your_original"])
                            gpt_revision_magnitudes.append(magnitude)

    gemini_revision_rate = (gemini_revisions_count / total_sdg_evaluations) * 100 if total_sdg_evaluations > 0 else 0
    gpt_revision_rate = (gpt_revisions_count / total_sdg_evaluations) * 100 if total_sdg_evaluations > 0 else 0

    print(f"Total SDG evaluations: {total_sdg_evaluations}")
    print(f"Gemini revisions: {gemini_revisions_count} ({gemini_revision_rate:.2f}%)")
    print(f"GPT revisions: {gpt_revisions_count} ({gpt_revision_rate:.2f}%)")

    if gemini_revision_magnitudes:
        print(f"Average Gemini revision magnitude: {np.mean(gemini_revision_magnitudes):.2f}")
    if gpt_revision_magnitudes:
        print(f"Average GPT revision magnitude: {np.mean(gpt_revision_magnitudes):.2f}")

    # Plotting revision rates
    labels = ['Gemini', 'GPT']
    revision_rates = [gemini_revision_rate, gpt_revision_rate]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(labels, revision_rates, color=['red', 'blue'])
    ax.set_ylim(0, 100)
    ax.set_ylabel('Revision Rate (%)')
    ax.set_title('Impact of Critique Step: Revision Rates by Model')
    plt.tight_layout()
    plt.savefig(f"plots/Critique_Impact_Revision_Rates.png")
    plt.close()





if __name__ == "__main__":
    result_dir = "./all_courses/"
    college_json_dir = "./" # Assuming college JSONs are in the current directory

    # Ensure plots directory exists
    plots_dir = "./plots/"
    os.makedirs(plots_dir, exist_ok=True)

    # Load all courses data for university-wide analysis
    all_courses_data = load_all_json_data(result_dir)

    # Load CoursesList.csv for department information
    courses_list_df = pd.read_csv("CoursesList.csv")
    all_courses_data = add_department_info(all_courses_data, courses_list_df)

    # A. Macro Descriptive Analysis (University Overview)
    # A-1. University SDG Coverage
    analyze_university_sdg_coverage(all_courses_data, model_name="Gemini-2.5-pro", threshold=7.0)
    # analyze_university_sdg_coverage(all_courses_data, model_name="GPT-4o-mini")

    # # A-2. University SDG Profile (Radar Chart)
    # analyze_university_sdg_profile(all_courses_data, model_name="Gemini-2.5-pro")
    # analyze_university_sdg_profile(all_courses_data, model_name="GPT-4o-mini")

    # A-3. Course SDG Density Analysis
    analyze_course_sdg_density(all_courses_data, model_name="Gemini-2.5-pro")
    # analyze_course_sdg_density(all_courses_data, model_name="GPT-4o-mini")

    # B. Comparative Analysis (College vs. Department)
    # B-2. Department-SDG Heatmap
    # plot_department_sdg_heatmap(all_courses_data, model_name="Gemini-2.5-pro")
    # plot_department_sdg_heatmap(all_courses_data, model_name="GPT-4o-mini")

    # B-3. Top Courses per SDG
    find_top_courses_per_sdg(all_courses_data, model_name="Gemini-2.5-pro", target_sdg="Quality Education")
    # find_top_courses_per_sdg(all_courses_data, model_name="GPT-4o-mini", target_sdg="Quality Education")
    find_top_courses_per_sdg(all_courses_data, model_name="Gemini-2.5-pro", target_sdg="Climate Action")
    # find_top_courses_per_sdg(all_courses_data, model_name="GPT-4o-mini", target_sdg="Climate Action")

    # C. Qualitative and Text Analysis
    # C-1. Keyword Analysis (Word Cloud)
    analyze_keyword_wordcloud(all_courses_data, model_name="Gemini-2.5-pro", target_sdg="Responsible Consumption and Production")
    # analyze_keyword_wordcloud(all_courses_data, model_name="GPT-4o-mini", target_sdg="Responsible Consumption and Production")

    # C-2. Evidence Type Analysis
    analyze_evidence_type(all_courses_data, model_name="Gemini-2.5-pro")
    # analyze_evidence_type(all_courses_data, model_name="GPT-4o-mini")

    # D. Methodology and Model Comparison Analysis
    # D-1. Model Consistency Analysis
    analyze_model_consistency(all_courses_data)

    # D-2. Model Bias Analysis
    analyze_model_bias(all_courses_data)

    # D-3. Impact of Critique Step Analysis
    analyze_critique_impact(all_courses_data)

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
    # college_names = ["All_Courses"]

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

        # # Plotting (using radar chart for college profiles)
        # plot_radar_chart(gemini_avg, "Gemini-2.5-flash", f"{college_name} SDG Profile (Gemini-2.5-flash)")
        # plot_radar_chart(gpt_avg, "GPT-4o-mini", f"{college_name} SDG Profile (GPT-4o-mini)")

    print("Analysis complete. Plots saved to the 'plots/' directory.")
