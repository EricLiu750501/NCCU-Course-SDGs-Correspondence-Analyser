
# 對 ./prompts/ 資料夾下所有的 資料喂入 LLM 裡面
import os
from openai import OpenAI
from pathlib import Path
from google import genai
from google.genai import types
import google.generativeai as genai

import json
from dotenv import load_dotenv
import time

system_prompt = [
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


class GPT:
    def __init__(self):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            api_key=openai_api_key,
        )
        self.messages = system_prompt.copy()

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



def getPrompt(prompt_folder = "./prompts", course_code_list = "地政課程.json"):
    # 從 ./prompts 裡面讀取檔案
    with open(course_code_list, 'r', encoding='utf-8') as f:
        code_lst = json.load(f)
    

    matched_files = []
    for file_path in Path(prompt_folder).glob('*.txt'):
        filename = file_path.stem  # 不含副檔名的檔名
        if filename in code_lst:
            matched_files.append(file_path)
    
    return matched_files
    
    

class Gemini:
    def __init__(self):
        load_dotenv()
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=gemini_api_key)

        # 建立模型物件
        self.model = genai.GenerativeModel(
            model_name = "gemini-2.5-flash",
            system_instruction = system_prompt[0]['content']
            )

    def query_json(self, prompt: str, temperature: float = 0.0):
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "response_mime_type": "application/json"
            }
        )
        return response.text


def main():
    # gg = GPT()
    # gg.query_json("你好啊")

    # gemini = Gemini()
    # print(gemini.query_json("你好啊, 隨便輸出一個數"))
    # exit()
    
    prompt_files = getPrompt(course_code_list= "社會課程.json")

    target_folder = "./prompts"
    result_folder = "./results/社會_Gemini/"

    # 確認資料夾存在
    if not os.path.exists(target_folder):
        print(f"資料夾 {target_folder} 不存在")
        return

    # 讀取所有檔案
    results = {}
    GPT_model = GPT()
    Gemini_model = Gemini()

    processed_count = 0
    # for file_path in Path(target_folder).glob('*'):
    #     if file_path.is_file():
    if True:
        for file_path in prompt_files:
            original_name = file_path.stem  # 取得不含副檔名的檔名
            result_file_path = os.path.join(result_folder, f"{original_name}.json")
            print(f"處理檔案: {file_path}")
            print(f"結果檔案: {result_file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 向LLM發送查詢
            start_time = time.time()
            # response = GPT_model.query_json(content, temperature=1)
            response = Gemini_model.query_json(content, temperature=0.0)
            end_time = time.time()
            print(f"API 調用耗時: {end_time - start_time:.2f} 秒")
            
            if response:
                original_name = file_path.stem  # 取得不含副檔名的檔名
                result_file_path = os.path.join(result_folder, f"{original_name}.json")
                data = json.loads(response)
                with open(result_file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"已儲存結果到 {result_file_path}")
                processed_count += 1

    # # 將結果保存到檔案
    # with open('llm_responses.json', 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)
    #
    # print(f"已處理 {len(results)} 個檔案，結果已保存到 llm_responses.json")

if __name__ == "__main__":
    main()

