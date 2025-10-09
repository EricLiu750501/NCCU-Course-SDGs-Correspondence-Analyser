
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


critique_system_prompt = [ # TODO: 可能要改一下 SDG_X 不然LLM不懂
    {
        "role": "system",
        "content": """
You are an SDG classification reviewer.
Your job: critique another model's SDG classification output.

Rules:
1. STRICTLY return JSON only.
2. Only include SDGs where you suggest a change.
3. JSON format must be:
{
  "critique": "short textual critique (<=40 words).",
  "suggested_changes": {
    "SDG_X": {
      "new_score": float (0.001–10.000),
      "reason": "why the score should be changed, <=30 words"
    },
    ...
  }
}
4. If no changes are needed:
{
  "critique": "No major issues found.",
  "suggested_changes": {}
}
5. Do not invent evidence. Only critique based on provided course text.
"""
    }
]


judge_system_prompt = [
    {
        "role": "system",
        "content": """
You are an impartial judge comparing two SDG classification outputs.

Rules:
1. STRICTLY return JSON only.
2. Decide per SDG which model is better.
3. JSON format must be:
{
    "No Poverty": {"winner": "A" | "B" | "Tie", "justification": "short reason"},
    "Zero Hunger": {...},
    ...
    "Partnerships for the Goals": {...}
}
4. Judge each SDG on:
   - explicitness of evidence
   - alignment with course text
   - reasoning clarity
5. Do not automatically favor one model. Allow mixed results across SDGs.
"""
    }
]


 

class GPT:
    def __init__(self):
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            api_key=openai_api_key,
        )
        self.messages = system_prompt.copy()

    def query_json(self, prompt:str, temperature:int=0, modelType:str="gpt-4o-mini") -> str: #TODO:注意 modelType 被換成 gpt-4o
        self.messages.append({"role": "user", "content": prompt})
        responses = self.client.chat.completions.create(
            model=modelType,
            messages =  self.messages,
            temperature=temperature,
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
        



def debate_experiment():
    print("testing GPT 4o and Gemini flash 2.5 Debate")
    # 準備要跑的 prompts
    prompt_files = getPrompt(course_code_list="地政課程_debate_repeat_gpt-4o-mini.json")
    # course_files = getPrompt(prompt_folder="./details", course_code_list="地政課程.json") # 獲取課程 markdown

    result_folder = "./experiment/debate/repeat_debate_4o/"
    os.makedirs(result_folder, exist_ok=True)

    for reps in range(6, 11): #TODO: 先 1~5 跑完再跑 6~10
        for file_path in prompt_files:
            GPT_model = GPT()
            Gemini_model = Gemini()

            with open(file_path, "r", encoding="utf-8") as f:
                course_prompt = f.read()

            course_name = Path(file_path).stem
            course_markdown_file = os.path.join(f"./details/{course_name}.md")
            save_path = os.path.join(result_folder, f"{course_name}_{reps}.json")

            with open(course_markdown_file, "r", encoding="utf-8") as f:
                course_markdown = f.read()

            # Check if the result file already exists
            if os.path.exists(save_path):
                print(f"⏭️ 跳過已存在的課程結果: {course_name} : {save_path}")
                continue

            print(f"Running debate for {course_name}")
            print(save_path)
            with open(save_path, "w", encoding="utf-8") as out:
                json.dump({},out , indent=2, ensure_ascii=False)
            
            course_start_time = time.time()

            # Step 1. 獨立回答
            gpt_answer = GPT_model.query_json(course_prompt)
            gemini_answer = Gemini_model.query_json(course_prompt, temperature=0)

            # Step 2. Cross-exam
            gpt_critique_prompt = f"""
    You are Model A (GPT). Below is Model B (Gemini)'s analysis.  
    Compare scores and reasons with your own. Identify disagreements.  
    For each disagreement: defend your score OR explain if Model B is better.  
    Please read Course Information carefully before critiquing.

    Course Information:
    {course_markdown}

    --

    Model B Answer:
    {gemini_answer} 

    --

    Model A Answer:
    {gpt_answer}
    """
            GPT_model.change_system_prompt(critique_system_prompt)
            gpt_critique = GPT_model.query_json(gpt_critique_prompt, temperature=0)

            gemini_critique_prompt = f"""
    You are Model B (Gemini). Below is Model A (GPT)'s analysis.  
    Compare scores and reasons with your own. Identify disagreements.  
    For each disagreement: defend your score OR explain if Model A is better.  
    Please read Course Information carefully before critiquing.

    Course Information:
    {course_markdown}

    --

    Model A Answer:
    {gpt_answer}

    --

    Model B Answer:
    {gemini_answer} 

    """
            Gemini_model.change_system_prompt(critique_system_prompt)
            gemini_critique = Gemini_model.query_json(gemini_critique_prompt, temperature=0)

            # Step 3. 仲裁
            judge_prompt = f"""
    You are the Judge. Two models (GPT=Model A, Gemini=Model B) debated their SDG scores.  
    Task:
    1. For each SDG, compare their scores & reasons.  
    2. Decide which score is more reasonable, OR propose compromise.  
    3. Output final_score, final_reason, and source ("A" | "B" | "compromise").  
    4. Please read Course Information carefully before judging.


    Course Information:
    {course_markdown}

    --

    Model A Answer:
    {gpt_answer}

    --

    Model B Answer:
    {gemini_answer}

    --

    Model A Critique:
    {gpt_critique}  

    --

    Model B Critique:
    {gemini_critique}
    """
            GPT_model.change_system_prompt(judge_system_prompt)
            Gemini_model.change_system_prompt(judge_system_prompt)
            gpt_judge_answer = GPT_model.query_json(judge_prompt, temperature=0)
            gemini_judge_answer = Gemini_model.query_json(judge_prompt, temperature=0)

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
    debate_experiment()

