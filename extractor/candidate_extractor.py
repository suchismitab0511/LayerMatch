from groq import Groq
import json
from config import GROQ_API_KEY

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


def extract_candidate_structure(resume_text):
    prompt = PROMPT_TEMPLATE.format(resume_text=resume_text)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    raw_output = response.choices[0].message.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        raw_output = raw_output.replace("json", "", 1).strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        print(f"  Failed to parse response as JSON: {e}")
        print(f"  Raw response was: {raw_output}")
        return None