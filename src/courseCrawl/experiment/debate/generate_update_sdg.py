import json

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def apply_critique_to_model(model_answer, critique):
    """Apply critique changes to the model answer"""
    updated_answer = model_answer.copy()
    
    for sdg, change in critique.items():
        # Handle the different formats in gpt_critique vs gemini_critique
        if sdg in updated_answer:
            sdg_key = sdg
        elif sdg.replace("_", " ") in updated_answer:
            sdg_key = sdg.replace("_", " ")
        else:
            continue
            
        updated_answer[sdg_key]["score"] = change["new_score"]
        updated_answer[sdg_key]["reason"] = change.get("reason", updated_answer[sdg_key]["reason"])
    
    return updated_answer

def generate_final_sdgs(data):
    gpt_original = data["gpt_answer"]
    gemini_original = data["gemini_answer"]
    
    # Apply critiques
    gpt_critique_changes = {}
    if "suggested_changes" in data["gpt_critique"]:
        gpt_critique_changes = data["gpt_critique"]["suggested_changes"]
    
    gemini_critique_changes = {}
    if "suggested_changes" in data["gemini_critique"]:
        gemini_critique_changes = data["gemini_critique"]["suggested_changes"]
    
    # Create updated versions based on critiques
    gpt_updated = apply_critique_to_model(gemini_original, gpt_critique_changes)
    gemini_updated = apply_critique_to_model(gpt_original, gemini_critique_changes)
    
    # Generate judge-based final scores
    final_scores = {}
    for sdg in gpt_original.keys():
        gpt_score = gpt_original[sdg]["score"]
        gemini_score = gemini_original[sdg]["score"]
        gpt_updated_score = gpt_updated[sdg]["score"]
        gemini_updated_score = gemini_updated[sdg]["score"]
        
        winner = data["gpt_judge_final"].get(sdg, {}).get("winner", "Tie")
        
        if winner == "A":
            # GPT answer + GPT's critique of itself
            final_scores[sdg] = (gpt_score + gemini_updated_score) / 2
        elif winner == "B":
            # Gemini answer + Gemini's critique of itself
            final_scores[sdg] = (gemini_score + gpt_updated_score) / 2
        else:  # Tie
            final_scores[sdg] = (gpt_score + gemini_score + gpt_updated_score + gemini_updated_score) / 4
    
    return {
        "gpt_original": gpt_original,
        "gemini_original": gemini_original,
        "gpt_updated": gpt_updated,
        "gemini_updated": gemini_updated,
        "final_scores": final_scores
    }

def main():
    data = load_json_data("./207742001.json")
    results = generate_final_sdgs(data)
    
    # Output the final scores
    print("Final SDG Scores:")
    for sdg, score in results["final_scores"].items():
        print(f"{sdg}: {score:.2f}")

if __name__ == "__main__":
    main()

