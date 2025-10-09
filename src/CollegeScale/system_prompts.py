
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


def critique_system_prompt(who):
    system_prompt_A = [
        {
            "role": "system",
            "content": """
You are Model A in a two-model SDG classification review.
Your job: Compare your SDG scores with Model B's and revise your own scores if needed.

Rules:
1. STRICTLY return JSON only.
2. Only include SDGs where YOU will revise YOUR score.
3. JSON format:
{
  "critique": "Overall assessment of differences (≤40 words)",
  "revisions": {
    "SDG_X (name of the SDGs)": {
      "your_original": float,
      "model_b_score": float,
      "your_revised": float,
      "reason": "Why you're changing (≤30 words)"
    }
  }
}
4. If no revisions needed:
{
  "critique": "No revisions needed. Model B's analysis aligns with mine.",
  "revisions": {}
}
5. Base decisions ONLY on provided course text. Do not invent evidence.
6. Be willing to revise if Model B's reasoning is more accurate.
"""
        }
    ]
    system_prompt_B = [
        {
            "role": "system",
            "content": """
You are Model B in a two-model SDG classification review.
Your job: Compare your SDG scores with Model A's and revise your own scores if needed.

Rules:
1. STRICTLY return JSON only.
2. Only include SDGs where YOU will revise YOUR score.
3. JSON format:
{
  "critique": "Overall assessment of differences (≤40 words)",
  "revisions": {
    "SDG_X (name of the SDGs)": {
      "your_original": float,
      "model_b_score": float,
      "your_revised": float,
      "reason": "Why you're changing (≤30 words)"
    }
  }
}
4. If no revisions needed:
{
  "critique": "No revisions needed. Model B's analysis aligns with mine.",
  "revisions": {}
}
5. Base decisions ONLY on provided course text. Do not invent evidence.
6. Be willing to revise if Model B's reasoning is more accurate.
"""
        }
    ]

    return system_prompt_A if who == "GPT" else system_prompt_B



def judge_system_prompt():
    
    return [
    {
        "role": "system",
        "content": """
You are an impartial judge synthesizing two SDG classification analyses.
Your job: Determine the most accurate score for each SDG based on course evidence.

Rules:
1. STRICTLY return JSON only.
2. JSON format:
{
  "No Poverty": {
    "final_score": float (0.001-10.0),
    "source": "model_a" | "model_b" | "revised_a" | "revised_b" | "synthesized",
    "reasoning": "Why this score is most accurate (≤50 words)",
    "model_comparison": {
      "model_a_original": float,
      "model_a_revised": float | null,
      "model_b_original": float,
      "model_b_revised": float | null
    }
  },
  "Zero Hunger": {...},
   ...
  "Partnerships for the Goals": {...}

  ...
}
3. Judge based on:
   - Explicit evidence in course text
   - Quality of reasoning
   - Alignment with SDG definitions
4. "synthesized" means you determined a score different from both models based on evidence.
5. Do not favor either model systematically.
"""
    }
]


def crituque_prompt(who, course_markdown, my_answer, other_answer):

    crituque_prompt_A = f"""
Compare your SDG analysis with Model B's.
Revise your scores if Model B's reasoning better aligns with the course text.

Course Information:
{course_markdown}

Your Original Analysis:
{my_answer}

Model B's Analysis:
{other_answer}

For each disagreement: determine whose interpretation is more accurate based on the course text.
"""

    crituque_prompt_B = f"""
Compare your SDG analysis with Model A's.
Revise your scores if Model A's reasoning better aligns with the course text.

Course Information:
{course_markdown}

Your Original Analysis:
{my_answer}

Model B's Analysis:
{other_answer}

For each disagreement: determine whose interpretation is more accurate based on the course text.
"""
    return crituque_prompt_A if who == "GPT" else crituque_prompt_B


def judge_prompt(course_markdown, gemini_answer, gpt_answer, gpt_critique, gemini_critique):
    user_prompt = f"""
Compare two models' SDG analyses and their mutual critiques.
Determine the most accurate score for each SDG.

Course Information:
{course_markdown}

Model A (GPT) Original Analysis:
{gpt_answer}

Model B (Gemini) Original Analysis:
{gemini_answer}

Model A's Revisions after seeing Model B:
{gpt_critique}

Model B's Revisions after seeing Model A:
{gemini_critique}

For each SDG:
1. Compare all versions (original + revised from both models)
2. Identify which reasoning best aligns with course evidence
3. Determine final score and justify your decision
"""
    return user_prompt

