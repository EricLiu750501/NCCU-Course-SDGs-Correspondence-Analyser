
title = ""
abstract = ""
keywords = ""
number_of_authors = 0
authorship_status_description = ""


def gen_prompt(title, abstract, keywords, number_of_authors, authorship_status_description):
    cso_concepts = \
    '''
    01. artificial intelligence
    02. bioinformatics
    03. computer aided design
    04. computer hardware
    05. computer imaging and vision
    06. computer networks
    07. computer programming
    08. computer security
    09. computer systems
    10. data mining
    11. human computer interaction
    12. information retrieval
    13. information technology
    14. internet
    15. operating systems
    16. pattern matching
    17. robotics
    18. software
    19. software engineering
    20. theoretical computer science
    '''

    asjc_domain = \
    '''
    1000	Multidisciplinary	
    1100	Agricultural and Biological Sciences	
    1200	Arts and Humanities 	
    1300	Biochemistry, Genetics and Molecular Biology 	
    1400	Business, Management, and Accounting 	
    1500	Chemical Engineering 	
    1600	Chemistry 	
    1700	Computer Science 	
    1800	Decision Sciences 	
    1900	Earth and Planetary Sciences 	
    2000	Economics, Econometrics and Finance 	
    2100	Energy 	
    2200	Engineering 	
    2300	Environmental Science 	
    2400	Immunology and Microbiology 	
    2500	Materials Science 	
    2600	Mathematics 	
    2700	Medicine 	
    2800	Neuroscience 	
    2900	Nursing 	
    3000	Pharmacology, Toxicology, and Pharmaceutics 	
    3100	Physics and Astronomy 	
    3200	Psychology 	
    3300	Social Sciences 	
    3400	Veterinary 	
    3500	Dentistry 	
    3600	Health Professions 	
    '''

    prompts = f"""
You are an expert in academic research classification. Your first task is to determine the primary broad academic domain(s) of the given research paper. Then, if the paper is identified as primarily belonging to "Computer Science", proceed to analyze it further using the Computer Science Ontology (CSO) concepts.

The scores should reflect the direct importance and relevance of the paper to each CSO concept:
-   **10.000**: Core concept, the paper fundamentally contributes to this area.
-   **7.000 - 9.999**: Highly relevant, a major focus or significant application area.
-   **4.000 - 6.999**: Moderately relevant, a supporting area or minor application.
-   **1.000 - 3.999**: Low relevance, only tangentially mentioned or very minor connection.
-   **0.001 - 0.999**: Minimal to no relevance, barely or not at all related, but must be above 0.

---

**Paper Information:**
Title: {title}
Abstract: {abstract}
Keywords: {keywords}
Number of Authors: {number_of_authors}
Author Affiliation: {authorship_status_description}

---

**Broad Academic Domains (Identify all relevant ASJC codes and their corresponding names):**
{asjc_domain}
---

**Target CSO Concepts (ONLY if primary domain is Computer Science, AND **MAINTAIN THE EXACT ORDER PROVIDED**):**
{cso_concepts}

---

**Respond in JSON format, structured as follows:**
```json
{{
    "Broad Domain": "Computer Science, Social Sciences", // List all relevant broad domains here, comma-separated, or just "Computer Science"
    "CSO Concepts": {{
        // The concepts in this object MUST appear in the exact order as provided in the "Target CSO Concepts" list above.
        "CSO Concept Name 1": {{
            "reason": "Concise reason for the score, highlighting relevant phrases or concepts from the paper information.",
            "score": number_with_three_decimal_places
        }},
        "CSO Concept Name 2": {{ // Example to show the next concept in order
            "reason": "Concise reason for the score, highlighting relevant phrases or concepts from the paper information.",
            "score": number_with_three_decimal_places
        }},
        // ... include all target CSO concepts with their scores and reasons, following the exact input order.
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
        paper_abstract = info.get("Abstract", "") # Note: "Abstract" in JSON has a capital A
        paper_keywords = info.get("keywords", "")
        num_authors = info.get("Number of Authors", 0)

        author_expertise = str(info.get("expertise", ""))
        author_depart = info.get("department", "")
        author_college = info.get("college", "")

        authorship_status = info.get("Contribution", "") # Note: "Contribution" is used for authorship status

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
