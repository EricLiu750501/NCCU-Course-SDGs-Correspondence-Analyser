import numpy as np
import json
from pathlib import Path
from scipy.spatial.distance import cosine
from scipy.stats import pearsonr

# 🔹 Kullback–Leibler Divergence
def kl_divergence(p, q):
    """計算 KL Divergence: KL(P || Q)"""
    p = np.array(p, dtype=np.float64)
    q = np.array(q, dtype=np.float64)
    
    # 正規化成機率分布
    p /= p.sum()
    q /= q.sum()
    
    # 避免 log(0) → 做平滑
    eps = 1e-12
    p = np.clip(p, eps, 1)
    q = np.clip(q, eps, 1)
    
    return np.sum(p * np.log(p / q))

# 🔹 Jensen–Shannon Divergence
def js_divergence(p, q):
    """計算 Jensen–Shannon Divergence"""
    p = np.array(p, dtype=np.float64)
    q = np.array(q, dtype=np.float64)
    
    # 正規化成機率分布
    p /= p.sum()
    q /= q.sum()
    
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)

# 🔹 Cosine Similarity
def cosine_similarity(p, q):
    """計算 Cosine 相似度"""
    return 1 - cosine(p, q)  # scipy 的 cosine 是距離，所以要 1 - distance

# 🔹 Pearson Correlation
def pearson_corr(p, q):
    """計算 Pearson 相關係數"""
    corr, _ = pearsonr(p, q)
    return corr

# ============================
# ✅ 範例使用
# ============================


def compare_distributions():
    dept_name = ["地政", "社會", "資訊"]
    llm_name = ["GPT", "Gemini"]
    name = "avg_score.json"
    
    for dept in dept_name:
        gpt_file = Path('./').joinpath(dept + "_" + llm_name[0]).joinpath(name)
        gemini_file = Path('./').joinpath(dept + "_" + llm_name[1]).joinpath(name)


        # print(gpt_file)
        # print(gemini_file)

        with open(gpt_file, "r", encoding="utf-8") as f:
            gpt_data = json.load(f)
        with open(gemini_file, "r", encoding="utf-8") as f:
            gemini_data = json.load(f)

        gpt_scores = list(gpt_data.values())
        gemini_scores = list(gemini_data.values())

        print(f"\n=== {dept} 系 LLM 比較 ===")
        print("KL Divergence:", kl_divergence(gpt_scores, gemini_scores))
        print("JS Divergence:", js_divergence(gpt_scores, gemini_scores))
        print("Cosine Similarity:", cosine_similarity(gpt_scores, gemini_scores))
        print("Pearson Correlation:", pearson_corr(gpt_scores, gemini_scores))

def compare_distributions_class():
    dept_name = ["地政", "社會", "資訊"]
    llm_name = ["GPT", "Gemini"]
    for dept in dept_name: 
        gpt_folder = Path('./').joinpath(dept + "_" + llm_name[0])
        gemini_folder = Path('./').joinpath(dept + "_" + llm_name[1])

        # Get all json files in the folders (excluding avg_score.json)
        gpt_files = [f for f in gpt_folder.glob("*.json") if f.name != "avg_score.json"]

        for gpt_file in gpt_files:
            # Find the corresponding file in the Gemini folder
            gemini_file = gemini_folder.joinpath(gpt_file.name)
            
            if not gemini_file.exists():
                print(f"找不到對應的 Gemini 檔案: {gpt_file.name}")
                continue
                
            course_name = gpt_file.stem  # Get filename without extension
            
            try:
                with open(gpt_file, "r", encoding="utf-8") as f:
                    gpt_data = json.load(f)
                with open(gemini_file, "r", encoding="utf-8") as f:
                    gemini_data = json.load(f)
                
                # Extract scores from the nested dictionary structure
                gpt_scores = []
                gemini_scores = []
                
                # Process each SDG goal in both datasets
                for sdg in gpt_data:
                    if sdg in gemini_data and 'score' in gpt_data[sdg] and 'score' in gemini_data[sdg]:
                        gpt_scores.append(float(gpt_data[sdg]['score']))
                        gemini_scores.append(float(gemini_data[sdg]['score']))
                
                if len(gpt_scores) > 0 and len(gemini_scores) > 0:
                    print(f"\n課程: {course_name}")
                    print("KL Divergence:", kl_divergence(gpt_scores, gemini_scores))
                else:
                    print(f"\n課程: {course_name} - 沒有足夠的數值資料進行比較")
                
            except Exception as e:
                print(f"處理課程 {course_name} 時發生錯誤: {str(e)}")


if __name__ == "__main__":
    # 假設 GPT 與 Gemini 的 SDG 分數
    # gpt_scores = [0.0, 0.25, 0.06, 7.84, 0.0, 0.12, 0.0, 0.31, 5.72, 0.12, 7.08, 0.10, 1.47, 0.14, 0.69, 4.97, 0.77]
    # gemini_scores = [0.0, 0.19, 0.97, 4.77, 1.41, 0.24, 1.00, 1.58, 2.28, 1.13, 0.69, 1.94, 1.72, 0.19, 0.75, 3.03, 1.91]
    compare_distributions_class()
