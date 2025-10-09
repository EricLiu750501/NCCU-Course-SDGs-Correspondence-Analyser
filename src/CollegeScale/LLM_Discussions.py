import os
from openai import OpenAI
from pathlib import Path
from google import genai
from google.genai import types
import google.generativeai as genai

import json
from dotenv import load_dotenv
import time

from system_prompts import crituque_prompt, critique_system_prompt, judge_prompt, judge_system_prompt, system_prompt



class GPT:
    def __init__(self):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            api_key=openai_api_key,
        )
        self.messages = system_prompt.copy()

    def query_json(self, prompt:str, temperature:int=0, modelType:str="gpt-5-nano") -> str: #TODO:注意 modelType 被換成 gpt-5-nano
        self.messages.append({"role": "user", "content": prompt})
        responses = self.client.chat.completions.create(
            model=modelType,
            messages =  self.messages,
            # temperature=temperature,
            response_format={"type": "json_object"}
        )
        if responses.choices[0].message.content:
            self.messages.append({"role": "assistant", "content": responses.choices[0].message.content})
            return responses.choices[0].message.content
        else:
            return "None"

    def change_system_prompt(self, newSystemPrompt):
        self.messages = newSystemPrompt.copy()  # 重設
    def get_messages(self):
        return self.messages


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
        self.messages = []

    def query_json(self, prompt: str, temperature: float = 0.0):
        self.messages.append({"role": "user", "content": prompt})
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "response_mime_type": "application/json"
            }
        )

        if response.text:
            self.messages.append({"role": "model", "content": response.text})
            return response.text
        else:
            return "None"
        return response.text

    def change_system_prompt(self, newSystemPrompt):
        self.messages = []
        self.model = genai.GenerativeModel(
            model_name = "gemini-2.5-flash",
            system_instruction = newSystemPrompt[0]['content']
        )

    def get_messages(self):
        return self.messages


def getPrompt(prompt_folder = "../courseCrawl/prompts/", course_code_list = "College_of_Commerce.json"): 
    # 從 ./prompts 裡面讀取檔案
    with open(course_code_list, 'r', encoding='utf-8') as f:
        code_lst = json.load(f)
    
    matched_files = []
    for file_path in Path(prompt_folder).glob('*.txt'):
        filename = file_path.stem  # 不含副檔名的檔名
        if filename in code_lst:
            matched_files.append(file_path)
    
    return matched_files


def Disscussion():
    print("testing GPT Nano and Gemini flash 2.5 Debate")
    # 準備要跑的 prompts
    prompt_files = getPrompt()
    
    result_folder = "./result"
    os.makedirs(result_folder, exist_ok=True)

    for file_path in prompt_files:
        GPT_model = GPT()
        Gemini_model = Gemini()

        with open(file_path, "r", encoding="utf-8") as f:
            course_prompt = f.read()

        course_name = Path(file_path).stem
        course_markdown_file = os.path.join(f"../courseCrawl/details/{course_name}.md")
        save_path = os.path.join(result_folder, f"{course_name}.json")

        with open(course_markdown_file, "r", encoding="utf-8") as f:
            course_markdown = f.read()

        # Check if the result file already exists
        if os.path.exists(save_path):
            print(f"⏭️ 跳過已存在的課程結果: {course_name} : {save_path}")
            continue

        print(f"Running Disscussion for {course_name}")
        print(save_path)
        with open(save_path, "w", encoding="utf-8") as out:
            json.dump({},out , indent=2, ensure_ascii=False)
        
        course_start_time = time.time()

        # Step 1. 獨立回答
        gpt_answer = GPT_model.query_json(course_prompt)
        gemini_answer = Gemini_model.query_json(course_prompt, temperature=0)

        # Step 2. Cross-exam
        GPT_model.change_system_prompt(critique_system_prompt("GPT"))
        gpt_critique = GPT_model.query_json(
            crituque_prompt("GPT", course_markdown, gpt_answer, gemini_answer)
            , temperature=0)

        Gemini_model.change_system_prompt(critique_system_prompt("Gemini"))
        gemini_critique = Gemini_model.query_json(
            crituque_prompt("Gemini", course_markdown, gemini_answer, gpt_answer)
            , temperature=0)

        # Step 3. 仲裁
        GPT_model.change_system_prompt(judge_system_prompt())
        Gemini_model.change_system_prompt(judge_system_prompt())
        gpt_judge_answer = GPT_model.query_json(
            judge_prompt(course_markdown, gemini_answer, gpt_answer, gpt_critique, gemini_critique
                         ), temperature=0)
        gemini_judge_answer = Gemini_model.query_json(
            judge_prompt(course_markdown, gemini_answer, gpt_answer, gpt_critique, gemini_critique
                         ), temperature=0)

        # 存檔
        with open(save_path, "w", encoding="utf-8") as out:
            json.dump({
                "gpt_answer": json.loads(gpt_answer),
                "gemini_answer": json.loads(gemini_answer),
                "gpt_critique": json.loads(gpt_critique),
                "gemini_critique": json.loads(gemini_critique),
                "gpt_judge_final": json.loads(gpt_judge_answer),
                "gemini_judge_final": json.loads(gemini_judge_answer)
            }, out, indent=2, ensure_ascii=False)

        course_elapsed = time.time() - course_start_time
        print(f"✅ Debate results saved: {save_path} (Time: {course_elapsed:.2f}s)")




if __name__ == "__main__":
    # main()
    Disscussion()


