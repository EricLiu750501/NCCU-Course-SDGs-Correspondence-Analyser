
title = ""
abstract = ""
keywords = ""
number_of_authors = 0
authorship_status_description = ""


def gen_prompt(title, abstract, keywords, number_of_authors, authorship_status_description):
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
You are an academic reviewer specializing in the United Nations Sustainable Development Goals (SDGs).
Your role is to assign **relevance scores** to a research paper based on its **title, abstract, keywords, and author information**.
Your assessment should be precise, as if contributing to an official SDG metadata classification.

The scores should reflect the direct importance and relevance of the paper to each SDG target:
- **10.000**: Core contribution, the paper fundamentally addresses this SDG.
- **7.000 - 9.999**: Highly relevant, a major focus or significant application area.
- **4.000 - 6.999**: Moderately relevant, a supporting area or minor application.
- **1.000 - 3.999**: Low relevance, only tangentially mentioned or very minor connection.
- **0.001 - 0.999**: Minimal to no relevance, barely or not at all related, but must be above 0.

---

**Paper Information:**
Title: {title}
Abstract: {abstract}
Keywords: {keywords}
Number of Authors: {number_of_authors}
Author Affiliation: {authorship_status_description}

---

**Target SDGs (MAINTAIN THE EXACT ORDER PROVIDED):**
{sdgs_targets}

---

**Respond in JSON format, structured as follows:**
```json
{{
    "No Poverty": {{
        "reason": "Concise reason citing phrases or concepts from the paper (or explicit absence).",
        "score": number_with_three_decimal_places
    }},
    "Zero Hunger": {{
        "reason": "Concise reason citing phrases or concepts from the paper (or explicit absence).",
        "score": number_with_three_decimal_places
    }},
    ...
    "Partnerships for the Goals": {{
        "reason": "Concise reason citing phrases or concepts from the paper (or explicit absence).",
        "score": number_with_three_decimal_places
    }}
}}
"""
    return prompts


import json

if __name__ == "__main__":
    with open("./samples.json", "r") as f:
        infos = json.load(f)

    print("--- Generated Prompts ---")
    for i, info in enumerate(infos):
        # Extract data from the JSON entry
        paper_title = info.get("title", "")
        paper_abstract = info.get("Abstract", "")
        paper_keywords = info.get("keywords", "")
        num_authors = info.get("Number of Authors", 0)

        author_expertise = str(info.get("expertise", ""))
        author_depart = info.get("department", "")
        author_college = info.get("college", "")

        authorship_status = info.get("Contribution", "")

        author_affiliation_status = f"{authorship_status}: {author_depart}, {author_college}, expertise:{author_expertise}"

        # Generate the prompt
        generated_prompt = gen_prompt(
            title=paper_title,
            abstract=paper_abstract,
            keywords=paper_keywords,
            number_of_authors=num_authors,
            authorship_status_description=author_affiliation_status
        )
        # Save the prompt to a file
        with open(f"./{i}/prompt.txt", "w") as f:
            f.write(generated_prompt)

        print(f"Saved prompt {i} to prompts/{i}/prompt")
        print(generated_prompt)

