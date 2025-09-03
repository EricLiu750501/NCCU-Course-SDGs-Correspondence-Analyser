
title = ""
abstract = ""
keywords = ""
number_of_authors = 0
authorship_status_description = ""
acm_css_top_levels = '''
**Top-Level ACM CCS Categories (evaluate these only):**
General and reference
Hardware
Computer systems organization
Networks
Software and its engineering
Theory of computation
Mathematics of computing
Information systems
Security and privacy
Human-centered computing
Computing methodologies
Applied computing
Social and professional topics
    '''



def gen_prompt(title, abstract, keywords, number_of_authors, authorship_status_description, acm_ccs):


    
    prompts = f"""
You are an academic reviewer specializing in the ACM Computing Classification System (ACM CCS). Your role is to assign relevance scores to a research paper based on its title, abstract, keywords, and author information. Your assessment should be precise, as if contributing to an official ACM CCS metadata classification.


The scores should reflect the direct importance and relevance of the paper to each CSO concept:
-   **10.000**: Core concept, the paper fundamentally contributes to this area.
-   **7.000 - 9.999**: Highly relevant, a major focus or significant application area.
-   **4.000 - 6.999**: Moderately relevant, a supporting area or minor application.
-   **1.000 - 3.999**: Low relevance, only tangentially mentioned or very minor connection.
-   **0.001 - 0.999**: Minimal to no relevance, barely or not at all related, but must be above 0.

Your output must:
Each reason must explicitly reference **phrases or concepts** from the title, abstract, or keywords that support the score. Avoid vague reasoning such as "somewhat related"; instead, cite specific terms or methods that justify the rating.
If a concept is barely relevant or not relevant, assign a low score (e.g., 0.001) but still provide a justification, even if only to state that none of the core concepts match that category. Do not leave the score or reason blank.
Ensure that the JSON response preserves the **exact order and full coverage** of the ACM CCS categories as provided above. Do not omit or reorder any entries.

---

**Paper Information:**
Title: {title}
Abstract: {abstract}
Keywords: {keywords}
Number of Authors: {number_of_authors}
Author Affiliation: {authorship_status_description}

---

{acm_ccs}

---

**Respond in JSON format, structured as follows:**

```json
{{
    "General and reference": {{
        "reason": "Concise reason for the score, highlighting relevant phrases or concepts from the paper information.",
        "score": number_with_three_decimal_places
    }},
    "Hardware": {{
        "reason": "Concise reason for the score, highlighting relevant phrases or concepts from the paper information.",
        "score": number_with_three_decimal_places
    }},
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
        paper_abstract = info.get("Abstract", "") # Note: "Abstract" in JSON has a capital A
        paper_keywords = info.get("keywords", "")
        num_authors = info.get("Number of Authors", 0)

        # author_expertise = str(info.get("expertise", ""))
        # author_depart = info.get("department", "")
        # author_college = info.get("college", "")
        author_aff = info.get("Author Affiliation", "")

        authorship_status = info.get("Contribution", "") # Note: "Contribution" is used for authorship status

        author_affiliation_status = "\n"
        for j in range(num_authors):
            author_affiliation_status += f"{authorship_status[j]} : {author_aff[j]}\n"

        # Generate the prompt
        generated_prompt = gen_prompt(
            title=paper_title,
            abstract=paper_abstract,
            keywords=paper_keywords,
            number_of_authors=num_authors,
            authorship_status_description=author_affiliation_status,
            acm_ccs = acm_css_top_levels
        )
        # Save the prompt to a file
        with open(f"./{i}/prompt.txt", "w") as f:
            f.write(generated_prompt)


        print(f"Saved prompt {i} to prompts/{i}/prompt")
        print(generated_prompt)
