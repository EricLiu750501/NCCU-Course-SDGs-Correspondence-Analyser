
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


SDG_ORDER = [
    "No Poverty",
    "Zero Hunger",
    "Good Health and Well-being",
    "Quality Education",
    "Gender Equality",
    "Clean Water and Sanitation",
    "Affordable and Clean Energy",
    "Decent Work and Economic Growth",
    "Industry, Innovation and Infrastructure",
    "Reduced Inequalities",
    "Sustainable Cities and Communities",
    "Responsible Consumption and Production",
    "Climate Action",
    "Life Below Water",
    "Life on Land",
    "Peace, Justice and Strong Institutions",
    "Partnerships for the Goals"
]

def extract_reasons(results_dir="./"):
    """
    從所有JSON檔案中提取每個SDG的原因，並統整到一個檔案中
    """
    all_reasons = {sdg: [] for sdg in SDG_ORDER}
    course_count = 0
    
    # 遍歷資料夾中的所有JSON檔案
    for json_file in Path(results_dir).glob('*.json'):
        try:
            course_name = json_file.stem
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 收集每個SDG的reason和evidence
                for sdg_name, sdg_info in data.items():
                    if sdg_name in all_reasons and sdg_info['score'] > 0.1:  # 只收集有意義的分數
                        reason_entry = {
                            "course": course_name,
                            "score": sdg_info['score'],
                            "reason": sdg_info['reason'],
                            "evidence": sdg_info['evidence']
                        }
                        all_reasons[sdg_name].append(reason_entry)
                course_count += 1

                    
        except Exception as e:
            print(f"處理 {json_file} 時出錯: {e}")
    
    # 將所有原因寫入一個檔案
    with open("sdg_reasons_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"SDG 原因統整 (基於 {course_count} 個課程)\n\n")
        
        for sdg in SDG_ORDER:
            f.write(f"## {sdg}\n")
            if not all_reasons[sdg]:
                f.write("沒有相關課程\n\n")
                continue
                
            # 依分數排序，從高到低
            sorted_entries = sorted(all_reasons[sdg], key=lambda x: x['score'], reverse=True)
            
            for entry in sorted_entries:
                f.write(f"- 課程: {entry['course']} (分數: {entry['score']})\n")
                f.write(f"  原因: {entry['reason']}\n")
                if entry['evidence']:
                    f.write("  證據:\n")
                    for evidence in entry['evidence']:
                        f.write(f"    * {evidence}\n")
                f.write("\n")
    
    print(f"已將 {course_count} 個課程的SDG原因統整至 sdg_reasons_summary.txt")



def analyze_json_results(results_dir="./results"):
    """
    分析資料夾中所有JSON檔案，計算每個SDG指標的平均分數，並製作長條圖
    """
    # 儲存所有SDG分數
    sdg_scores = {}
    file_count = 0
    
    # 遍歷資料夾及子資料夾中的所有JSON檔案
    for json_file in Path(results_dir).glob('./*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 累加每個SDG的分數
                for sdg_name, sdg_info in data.items():
                    if sdg_name not in sdg_scores:
                        sdg_scores[sdg_name] = []
                    
                    # 加入分數到列表中
                    sdg_scores[sdg_name].append(sdg_info['score'])
                file_count += 1
                    
        except Exception as e:
            print(f"處理 {json_file} 時出錯: {e}")
    
    # 計算平均分數
    sdg_averages = {sdg: sum(scores)/len(scores) for sdg, scores in sdg_scores.items()}
    
    # 設定支援中文的字體
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft JhengHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False  # 正確顯示負號
    
    # 製作長條圖
    plt.figure(figsize=(15, 10))
    
    # 根據 SDG_ORDER 排序結果
    ordered_sdgs = []
    ordered_scores = []
    numbered_labels = []
    for i, sdg in enumerate(SDG_ORDER, 1):  # 從1開始編號
        if sdg in sdg_averages:
            ordered_sdgs.append(sdg)
            ordered_scores.append(sdg_averages[sdg])
            numbered_labels.append(f"{i}. {sdg}")  # 加入編號到標籤
    
    # 繪製長條圖
    bars = plt.bar(numbered_labels, ordered_scores)
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Average SDG Scores for Land Economic Dept.({file_count} Couses) (GPT-5-nano)')
    plt.xlabel('Sustainable Development Goals (SDGs)')
    plt.ylabel('Average Score')
    plt.ylim(0, 10)  # 固定 y 軸最大值為 10
    plt.tight_layout()
    
    # 為每個長條添加數值標籤
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height:.2f}', ha='center', va='bottom')
    
    # 儲存圖片
    plt.savefig("sdg_average_scores.png", dpi=300)
    plt.show()
    
    # 儲存平均分數到JSON檔案
    with open("avg_score.json", "w", encoding="utf-8") as f:
        json.dump(sdg_averages, f, ensure_ascii=False, indent=4)

    print(f"已分析 {file_count} 個JSON檔案")
    return sdg_averages

if __name__ == "__main__":
    results = analyze_json_results(results_dir="./")
    extract_reasons(results_dir="./")
    # print("平均分數:", results)
