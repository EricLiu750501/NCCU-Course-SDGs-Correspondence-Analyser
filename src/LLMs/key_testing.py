'''

billing : https://platform.openai.com/settings/organization/billing/overview

'''

# works

from openai import OpenAI
from google import genai


from dotenv import load_dotenv
import os

def main():
  load_dotenv()
  openai_api_key = os.getenv("OPENAI_API_KEY")
  gemini_api_key = os.getenv("GEMINI_API_KEY")
  test_gpt(openai_api_key)
  test_gemini(gemini_api_key)



def test_gpt(key):
  print("Testing GPT-4o-mini")
  client = OpenAI(
    api_key= key
  )

  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
      {"role": "user", "content": "write a haiku about ai"}
    ]
  )
  print(completion.choices[0].message);
  print('-' * 20)

def test_gemini(key):
  print("Testing Gemini")
  client = genai.Client(api_key=key)

  response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents="Explain how AI works in a few words",
  )
  print(response.text)
  print('-' * 20)



if main() == "__main__":
  main()
