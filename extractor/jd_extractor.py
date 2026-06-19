from groq import Groq
import json
from config import GROQ_API_KEY
import time

client = Groq(api_key=GROQ_API_KEY)


PROMPT_TEMPLATE = """
You are an expert technical recruiter. Read the job description below and extract structured information from it.

Return ONLY valid JSON, no extra text, no markdown formatting, no backticks. Follow this exact structure:

{{
  "job_title": "",
  "seniority_level": "",
  "required_skills": [],
  "preferred_skills": [],
  "min_experience_years": 0,
  "max_experience_years": 0,
  "education_requirement": "",
  "domain": "",
  "responsibilities": [],
  "soft_skills": []
}}

If a field is not mentioned, use an empty string, empty list, or 0. Do not invent information that isn't there.

Job Description:
{jd_text}
"""


def extract_jd_structure(jd_text, retries=3):
    prompt = PROMPT_TEMPLATE.format(jd_text=jd_text)

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