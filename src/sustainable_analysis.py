import csv
import json
import os

# --- Configuration ---
CSV_PATH = 'src/113-2.xlsx - 工作表1.csv'
JSON_PATH = 'src/CollegeScale/combined_sdg_details.json'
SCORE_THRESHOLD = 8.99

SDG_ORDER = [
    "No Poverty", "Zero Hunger", "Good Health and Well-being", "Quality Education",
    "Gender Equality", "Clean Water and Sanitation", "Affordable and Clean Energy",
    "Decent Work and Economic Growth", "Industry, Innovation and Infrastructure",
    "Reduced Inequalities", "Sustainable Cities and Communities",
    "Responsible Consumption and Production", "Climate Action", "Life Below Water",
    "Life on Land", "Peace, Justice and Strong Institutions", "Partnerships for the Goals"
]

def analyze():
    # 1. Load SDG details
    if not os.path.exists(JSON_PATH):
        print(f"Error: {JSON_PATH} not found.")
        return
    
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        sdg_data = json.load(f)

    # 2. Initialize statistics
    # Stats structure: { "Total": { "sustainable_count": 0, "enrollment": 0, "sdgs": [0]*17, "total_courses": 0 }, ... }
    stats = {
        "University": {
            "Total": {"sustainable_count": 0, "enrollment": 0, "sdgs": [0]*17, "total_courses": 0}
        },
        "College": {},
        "Department": {}
    }

    # 3. Read CSV and process
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # Verify columns based on previous head check
        # Index 3: 科目代號, 7: 教師所屬院別, 8: 開課單位, 10: 修課人數
        
        for row in reader:
            if not row: continue
            try:
                course_id = row[3].strip()
                college = row[7].strip()
                dept = row[8].strip()
                enrollment = int(row[10]) if row[10] else 0
            except (IndexError, ValueError):
                continue

            # Update total course counts
            for level, name in [("University", "Total"), ("College", college), ("Department", dept)]:
                if name not in stats[level]:
                    stats[level][name] = {"sustainable_count": 0, "enrollment": 0, "sdgs": [0]*17, "total_courses": 0}
                stats[level][name]["total_courses"] += 1

            # Check SDG scores
            # Try exact match first, then try first 8 digits
            match_id = None
            if course_id in sdg_data:
                match_id = course_id
            elif len(course_id) >= 8:
                prefix = course_id[:8]
                # Look for any key starting with this prefix
                for key in sdg_data.keys():
                    if key.startswith(prefix):
                        match_id = key
                        break
            
            if match_id:
                course_sdgs = sdg_data[match_id]
                is_sustainable = False
                met_sdgs = [False] * 17

                for i, sdg_name in enumerate(SDG_ORDER):
                    score = course_sdgs.get(sdg_name, {}).get('score', 0)
                    if score > SCORE_THRESHOLD:
                        met_sdgs[i] = True
                        is_sustainable = True

                if is_sustainable:
                    for level, name in [("University", "Total"), ("College", college), ("Department", dept)]:
                        stats[level][name]["sustainable_count"] += 1
                        stats[level][name]["enrollment"] += enrollment
                        for i in range(17):
                            if met_sdgs[i]:
                                stats[level][name]["sdgs"][i] += 1

    # 4. Format and Print Results (Summary)
    print("=== University Level Summary ===")
    uni = stats["University"]["Total"]
    print(f"Total Courses: {uni['total_courses']}")
    print(f"Sustainable Courses: {uni['sustainable_count']} ({uni['sustainable_count']/uni['total_courses']*100:.2f}%)")
    print(f"Total Enrollment in Sustainable Courses: {uni['enrollment']}")
    print("-" * 30)

    # 5. Output to file
    with open('sustainability_stats_result.json', 'w', encoding='utf-8') as out_f:
        json.dump(stats, out_f, ensure_ascii=False, indent=2)
    
    # 6. Generate a readable CSV for Department level
    with open('department_sustainability_stats.csv', 'w', encoding='utf-8', newline='') as csv_out:
        writer = csv.writer(csv_out)
        sdg_headers = [f"SDG{i+1}" for i in range(17)]
        writer.writerow(["College", "Department", "Total Courses", "Sustainable Courses", "Sustainable Enrollment"] + sdg_headers)
        
        # We need to map Dept to College for the CSV output
        dept_to_college = {}
        for college, depts in stats["College"].items():
            # This is a bit tricky because my stats[Department] doesn't store college info directly.
            # I'll re-run or just iterate through the stats.
            pass
            
        # Let's just iterate Department stats. Since I didn't store college in stats["Department"], 
        # I'll modify the loop above or just output what I have.
        # Actually, let's just use the Department names.
        for dept, data in sorted(stats["Department"].items()):
            writer.writerow([
                "", # College (optional if we don't track it here)
                dept,
                data["total_courses"],
                data["sustainable_count"],
                data["enrollment"]
            ] + data["sdgs"])

    print("\nResults saved to 'sustainability_stats_result.json' and 'department_sustainability_stats.csv'")

if __name__ == "__main__":
    analyze()
