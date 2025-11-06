# 將 details/ 裡面的所有 md 寫成 prompt 放到 prompts/ 裡面


title = ""
abstract = ""
keywords = ""
number_of_authors = 0
authorship_status_description = ""

sdgs_goals_targets = ""
with open("./goal_formatted_less.md", "r", encoding="utf-8") as f:
    sdgs_goals_targets = f.read()


def gen_prompt(course_info):
    sdgs_targets = \
    '''
    1. No Poverty
    2. Zero Hunger
    3. Good Health and Well-being
    4. Quality Education
    5. Gender Equality
    6. Clean Water and Sanitation
    7. Affordable and Clean Energy
    8. Decent Work and Economic Growth
    9. Industry, Innovation and Infrastructure
    10. Reduced Inequalities
    11. Sustainable Cities and Communities
    12. Responsible Consumption and Production
    13. Climate Action
    14. Life Below Water
    15. Life on Land
    16. Peace, Justice and Strong Institutions
    17. Partnerships for the Goals
    '''

    prompts = f"""
You are an expert in Sustainable Development Goals (SDGs) classification. 
Your task is to analyze the following university course and assign relevance scores to each of the 17 SDGs.

Follow ALL rules and output formatting instructions from the system prompt.

---

**Course Information**
{course_info}

---

** SDG Goals Targets Reference: **
{sdgs_goals_targets}

---


**Target SDGs (MAINTAIN THE EXACT ORDER PROVIDED):**
{sdgs_targets}

---

**Respond ONLY in the JSON format specified in the system prompt.**
"""
    return prompts


import json
import os

if __name__ == "__main__":
    pick_folder = "../courseCrawl/details"
    output_folder = "./prompts"

    os.makedirs(output_folder, exist_ok=True)

    for i, filename in enumerate(os.listdir(pick_folder)):
        if filename.endswith(".md"):
            filepath = os.path.join(pick_folder, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                course_info = f.read()

            prompt_text = gen_prompt(course_info)
            name, _ = os.path.splitext(filename)
            save_path = os.path.join(output_folder, f"{name}.txt")
            with open(save_path, "w", encoding="utf-8") as out:
                out.write(prompt_text)

            print(f"✅ Saved prompt: {save_path}")
