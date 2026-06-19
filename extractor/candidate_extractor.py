from groq import Groq
import json
from config import GROQ_API_KEY
import time

client = Groq(api_key=GROQ_API_KEY)


PROMPT_TEMPLATE = """
You are an expert technical recruiter. Read the resume text below and extract structured information from it.

Return ONLY valid JSON, no extra text, no markdown formatting, no backticks. Follow this exact structure:

{{
  "name": "",
  "total_experience_years": 0,
  "skills": [],
  "work_history": [
    {{
      "role": "",
      "company": "",
      "start_date": "",
      "end_date": "",
      "description": ""
    }}
  ],
  "projects": [
    {{
      "title": "",
      "technologies": [],
      "description": ""
    }}
  ],
  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
    }}
  ],
  "certifications": []
}}

If a field is not mentioned, use an empty string, empty list, or 0. Do not invent information that isn't there. For total_experience_years, estimate based on work history dates if explicit total is not stated.

Resume Text:
{resume_text}
"""


def extract_candidate_structure(resume_text, retries=3):
    prompt = PROMPT_TEMPLATE.format(resume_text=resume_text)

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
            )
            raw_output = response.choices[0].message.content.strip()

            if raw_output.startswith("```"):
                raw_output = raw_output.strip("`")
                raw_output = raw_output.replace("json", "", 1).strip()

            return json.loads(raw_output)

        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait_time = 10 * (attempt + 1)
                print(f"  Rate limited. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"  Extraction failed: {e}")
                return None

    print("  All retries exhausted.")
    return None