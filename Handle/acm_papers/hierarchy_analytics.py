import json


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




input_folder = int(input("Enter the input folder number (e.g., 10): "))
current_folder = f"./{input_folder}/next_level"
print(json.dumps(analyze_scores(), indent=4))


