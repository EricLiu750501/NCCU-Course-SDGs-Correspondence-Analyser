
# 對 ./prompts/ 資料夾下所有的 資料喂入 LLM 裡面
import os
from openai import OpenAI
from pathlib import Path
import json
from dotenv import load_dotenv


class GPT:
    def __init__(self):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            api_key=openai_api_key,
        )
        self.messages = [
            {"role": "system", "content": 
             """
You are an expert classifier for mapping university course descriptions to the 17 United Nations Sustainable Development Goals (SDGs). 
Rules:
1. ONLY use information present in the provided "Course Information". Do NOT assume or invent facts not in the input.
2. Return STRICTLY valid JSON and nothing else (no extra text). If you cannot produce valid JSON, return {"error":"could_not_produce_json"}.
3. Preserve the EXACT SDG order requested. Do not omit keys.
4. For each SDG provide:
   - "score": numeric, range 0.001–10.000, with three decimal places.
   - "reason": concise (<=30 words), explicitly reference verbatim phrases from the Course Information.
   - "evidence": an array of up to 3 exact phrases or short excerpts from the Course Information that support the score (leave empty array if none).
   - "evidence_type": either "explicit" (course text directly mentions the SDG topic) or "inferred" (reasonable inference from course content).
5. If there is NO supporting text, set score to 0.001, reason to "No evidence found", evidence to [], evidence_type to "none".
6. Prioritize explicit mentions over inference. If only indirect language exists, use a low score and mark evidence_type "inferred".
7. Keep "reason" factual and citation-like (e.g., "mentions 'water treatment' and 'sustainable engineering' → relevant to Clean Water and Sanitation").
8. Do NOT reveal chain-of-thought. Only give the short "reason" and the "evidence" items.
             """},
        ]

    def query_json(self, prompt:str, temperature:int=0) -> str:
        self.messages.append({"role": "user", "content": prompt})
        responses = self.client.chat.completions.create(
            model="gpt-5-nano",
            messages =  self.messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
        if responses.choices[0].message.content:
            self.messages.append({"role": "assistant", "content": responses.choices[0].message.content})
            return responses.choices[0].message.content
        else:
            return "None"


def main():
    target_folder = "./prompts"

    # 確認資料夾存在
    if not os.path.exists(target_folder):
        print(f"資料夾 {target_folder} 不存在")
        return

    # 讀取所有檔案
    results = {}
    GPT_model = GPT()
    for file_path in Path(target_folder).glob('*'):
        if file_path.is_file():
            print(f"處理檔案: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 向LLM發送查詢
            response = GPT_model.query_json(content, temperature=1)
            
            if response:
                # results[file_path.name] = response
                data = json.loads(response)
                with open('llm_responses_nano_5_system.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
        break

    # # 將結果保存到檔案
    # with open('llm_responses.json', 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)
    #
    # print(f"已處理 {len(results)} 個檔案，結果已保存到 llm_responses.json")

if __name__ == "__main__":
    main()

