import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys


acm_hierarchy = {
    "General and reference": [
        "Document types",
        "Cross-computing tools and techniques"
    ],
    "Hardware": [
        "Computer systems organization",
        "Networks",
        "Software and its engineering",
        "Theory of computation",
        "Mathematics of computing",
        "Information systems",
        "Security and privacy",
        "Human-centered computing",
        "Computing methodologies",
        "Applied computing",
        "Social and professional topics"
    ],
    "Computer systems organization": [
        "Architectures",
        "Embedded and cyber-physical systems",
        "Real-time systems",
        "Dependable and fault-tolerant systems and networks"
    ],
    "Networks": [
        "Network architectures",
        "Network protocols",
        "Network components",
        "Network algorithms",
        "Network performance evaluation",
        "Network properties",
        "Network services",
        "Network types"
    ],
    "Software and its engineering": [
        "Software organization and properties",
        "Software notations and tools",
        "Software creation and management"
    ],
    "Theory of computation": [
        "Models of computation",
        "Formal languages and automata theory",
        "Computational complexity and cryptography",
        "Logic",
        "Design and analysis of algorithms",
        "Randomness, geometry and discrete structures",
        "Theory and algorithms for application domains",
        "Semantics and reasoning"
    ],
    "Mathematics of computing": [
        "Discrete mathematics",
        "Probability and statistics",
        "Mathematical software",
        "Information theory",
        "Mathematical analysis",
        "Continuous mathematics"
    ],
    "Information systems": [
        "Data management systems",
        "Information storage systems",
        "Information systems applications",
        "World Wide Web",
        "Information retrieval"
    ],
    "Security and privacy": [
        "Cryptography",
        "Formal methods and theory of security",
        "Security services",
        "Intrusion/anomaly detection and malware mitigation",
        "Security in hardware",
        "Systems security",
        "Network security",
        "Database and storage security",
        "Software and application security",
        "Human and societal aspects of security and privacy"
    ],
    "Human-centered computing": [
        "Human computer interaction (HCI)",
        "Interaction design",
        "Collaborative and social computing",
        "Ubiquitous and mobile computing",
        "Visualization",
        "Accessibility"
    ],
    "Computing methodologies": [
        "Symbolic and algebraic manipulation",
        "Parallel computing methodologies",
        "Artificial intelligence",
        "Machine learning",
        "Modeling and simulation",
        "Computer graphics",
        "Distributed computing methodologies",
        "Concurrent computing methodologies"
    ],
    "Applied computing": [
        "Electronic commerce",
        "Enterprise computing",
        "Physical sciences and engineering",
        "Life and medical sciences",
        "Law, social and behavioral sciences",
        "Computer forensics",
        "Arts and humanities",
        "Computers in other domains",
        "Operations research",
        "Education",
        "Document management and text processing"
    ],
    "Social and professional topics": [
        "Professional topics",
        "Computing / technology policy",
        "User characteristics"
    ]
}


# Add the project root directory to the Python path to enable absolute imports
# Get the absolute path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the src directory
src_dir = os.path.dirname(current_dir)
# Go up another level to the project root
project_root = os.path.dirname(src_dir)
# Add project root to Python path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)



def load_json_data(file_path):
    """Load data from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None

def extract_llm_scores(data_dict):
    """Extract scores from the CSO Concepts data for a specific LLM."""
    scores = {}
    for concept, details in data_dict.items():
        scores[concept] = details.get("score", 0)
    return scores


def filter_scores(llm_scores, threshold=7, top_k=None):
    """
    Filter concepts based on a score threshold for each LLM and return top scoring concepts.
    
    Args:
        llm_scores: Dictionary with LLM names as keys and dictionaries of concept scores as values
        threshold: Minimum score to include a concept (default: 7)
        top_k: Optional limit on the number of concepts to return per LLM (default: None, return all that meet threshold)
    
    Returns:
        Dictionary with LLM names as keys and lists of top concepts that meet the threshold,
        sorted by score (highest first)
    """
    filtered_concepts = {}
    
    for llm_name, scores in llm_scores.items():
        # Filter concepts that meet or exceed the threshold
        qualifying_concepts = [(concept, score) for concept, score in scores.items() if score >= threshold]
        
        # Sort the qualifying concepts by score (highest first)
        qualifying_concepts.sort(key=lambda x: x[1], reverse=True)
        
        # Limit to top_k if specified
        if top_k is not None:
            qualifying_concepts = qualifying_concepts[:top_k]
        
        # Store only the concept names in the result, maintaining the sorted order
        filtered_concepts[llm_name] = [concept for concept, _ in qualifying_concepts]
        
    return filtered_concepts




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

**ACM CCS Categories (evaluate these only):**
{acm_ccs}

---

**Respond in JSON format, structured as follows:**

```json
{{
    "Categories 1": {{
        "reason": "Concise reason for the score, highlighting relevant phrases or concepts from the paper information.",
        "score": number_with_three_decimal_places
    }},
    "Categorise 2": {{
        "reason": "Concise reason for the score, highlighting relevant phrases or concepts from the paper information.",
        "score": number_with_three_decimal_places
    }},
}}
"""
    return prompts



def analyze_scores():
    """Main function to analyze score data from JSON files."""
    # Paths to the JSON files
    # current_folder = f"./{input_folder}"
    categories =  {}   
    llm_names = [
        "claude-sonnet-4",
        "gemini2-5flash",
        "gemini2-5pro",
        "gpt4o",
        "grok3",
        "perplexity-pro"
    ]

    # Load data for each LLM
    llm_scores = {}
    for llm_name in llm_names:
        file_path = f"{current_folder}/{llm_name}.json"
        data = load_json_data(file_path)
        if data:
            llm_scores[llm_name] = extract_llm_scores(data)
        else:
            print(f"Could not load data for {llm_name}")
    
    if llm_scores:
        filtered_scores = filter_scores(llm_scores, threshold=7, top_k=3)
        # print("Filtered Scores (threshold >= 7):")
        # print(json.dumps(filtered_scores, indent=4))
        return filtered_scores

def gen_level_concept(concepts):
    """Generate a mapping of concepts to their hierarchy levels."""
    level_concept = {}
    for llm_name, concepts_list in concepts.items():
        level_concept[llm_name] = []
        for c in concepts_list:
            # Find the level in the ACM hierarchy
            level_concept[llm_name] += acm_hierarchy[c]



    return level_concept



input_folder = int(input("Enter the input folder number (e.g., 10): "))
current_folder = f"./{input_folder}"
filtered_concepts = analyze_scores()
lower_level_concepts = gen_level_concept(filtered_concepts)



with open("./samples.json", "r") as f:
    infos = json.load(f)

print("--- Generated Prompts ---")

info = infos[input_folder]
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

for llm_name, concepts_list in lower_level_concepts.items():
    # Generate the prompt
    generated_prompt = gen_prompt(
        title=paper_title,
        abstract=paper_abstract,
        keywords=paper_keywords,
        number_of_authors=num_authors,
        authorship_status_description=author_affiliation_status,
        acm_ccs = "\n".join(lower_level_concepts[llm_name])
    )
    # Save the prompt to a file
    with open(f"./{input_folder}/next_level/prompt_{llm_name}.txt", "w") as f:
        f.write(generated_prompt)


    print(f"Saved prompt {input_folder} to prompts/{input_folder}/prompt")
    print(generated_prompt)







