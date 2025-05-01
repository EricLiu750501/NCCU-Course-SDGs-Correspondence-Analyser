'''

billing : https://platform.openai.com/settings/organization/billing/overview

'''

# works!

from openai import OpenAI
from google import genai
from google.genai import types


from dotenv import load_dotenv
import os

def test():
  load_dotenv()
  openai_api_key = os.getenv("OPENAI_API_KEY")
  gemini_api_key = os.getenv("GEMINI_API_KEY")
  # test_gpt(openai_api_key)
  test_gemini(gemini_api_key)

def test_gpt(key):
  print("Testing GPT-4o-mini")
  # client = OpenAI(
  #   api_key= key
  # )
  #
  # completion = client.chat.completions.create(
  #   model="gpt-4o-mini",
  #   store=True,
  #   messages=[
  #     {"role": "user", "content": "write a haiku about ai"}
  #   ]
  # )
  # print(completion.choices[0].message);
  g  = GPT()
  print(g.ask("write a haiku about ai"))
  print('-' * 20)

def test_gemini(key):
  print("Testing Gemini")
  # client = genai.Client(api_key=key)
  #
  # response = client.models.generate_content(
  #     model="gemini-2.0-flash",
  #     contents="Explain how AI works in a few words",
  # )
  # print(response.text)
  # print('-' * 20)
  g = Gemini()
  print(g.ask("write a haiku about ai"))
  print('-' * 20)



class GPT:
  def __init__(self):
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    self.client = OpenAI(
      api_key=openai_api_key,
    )

  def ask(self, prompt:str, temperature:int=0) -> str:
    responses = self.client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "user", "content": prompt}
      ],
      temperature=temperature
    )
    if responses.choices[0].message.content:
      return responses.choices[0].message.content
    else:
      return "None"


class Gemini:
  def __init__(self):
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    self.client = genai.Client(api_key=gemini_api_key)

  def ask(self, prompt:str, temperature:int=0):
    response = self.client.models.generate_content(
      model="gemini-2.0-flash",
      contents=prompt,
      config = types.GenerateContentConfig(
        temperature=temperature,
      )
    )
    if response.text:
      return response.text
    else:
      return "None"


  

if __name__ == "__main__":
  test()

