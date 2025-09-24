
import json

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_final_scores(data):
    sdgs = list(data["gpt_answer"].keys())
    results = {}
    
    for sdg in sdgs:
        gpt_score = data["gpt_answer"][sdg]["score"]
        gemini_score = data["gemini_answer"][sdg]["score"]
        
        # Get critique-modified scores if they exist
        gpt_critique_modified = None
        gemini_critique_modified = None
        
        if sdg.replace(" ", "_") in data.get("gpt_critique", {}).get("suggested_changes", {}):
            gpt_critique_modified = data["gpt_critique"]["suggested_changes"][sdg.replace(" ", "_")]["new_score"]
        
        if sdg in data.get("gemini_critique", {}).get("suggested_changes", {}):
            gemini_critique_modified = data["gemini_critique"]["suggested_changes"][sdg]["new_score"]
        
        # Get winner from judge finals
        winner = data["gpt_judge_final"].get(sdg, {}).get("winner", "Tie")
        
        # Calculate final score based on the rules
        if winner == "A":
            if gpt_critique_modified is not None:
                final_score = (gpt_score + gpt_critique_modified) / 2
            else:
                final_score = gpt_score
        elif winner == "B":
            if gemini_critique_modified is not None:
                final_score = (gemini_score + gemini_critique_modified) / 2
            else:
                final_score = gemini_score
        else:  # Tie
            scores = [gpt_score, gemini_score]
            if gpt_critique_modified is not None:
                scores.append(gpt_critique_modified)
            if gemini_critique_modified is not None:
                scores.append(gemini_critique_modified)
            final_score = sum(scores) / len(scores)
        
        results[sdg] = {
            "original_gpt_score": gpt_score,
            "original_gemini_score": gemini_score,
            "gpt_critique_score": gpt_critique_modified,
            "gemini_critique_score": gemini_critique_modified,
            "winner": winner,
            "final_score": final_score
        }
    
    return results

def main():
    data = load_json_data("./257778001.json")
    results = calculate_final_scores(data)
    
    # Output the final scores
    for sdg, result in results.items():
        print(f"{sdg}: {result['final_score']:.3f} (Winner: {result['winner']})")

if __name__ == "__main__":
    main()
