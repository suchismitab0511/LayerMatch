from groq import Groq
import json
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


PROMPT_TEMPLATE = """
You are an expert technical recruiter reviewing a candidate ranking result.

Based on the data below, write a concise recruiter-style explanation (4-6 sentences) covering:
- Why this candidate ranked where they did
- Their key strengths relevant to the job
- Any notable skill gaps or weaknesses
- A clear hiring recommendation

Be direct and specific. Use the actual skill names. Do not be generic.

IMPORTANT: The "Matched Skills" section below shows skills the candidate DID have.
Any required skill NOT appearing in matched skills is a GAP.

Job Title: {job_title}
Required Skills: {required_skills}

Candidate Name: {name}
Rank: #{rank}
Final Score: {final_score} out of 1.0

Score Breakdown:
- Semantic Match: {semantic_score}
- Skill Match: {skill_score} (fraction of required skills matched)
- Experience Score: {experience_score}
- Education Score: {education_score}

Skills candidate HAS that match job requirements:
{matched_skills}

Skills candidate is MISSING from job requirements:
{missing_skills}

Candidate Work History:
{work_history}

Write the explanation now:
"""


def explain_candidate(candidate, jd_data):
    scores = candidate["scores"]
    candidate_data = candidate["candidate_data"]

    required_skills = jd_data.get("required_skills", [])
    matched_skill_names = [m[0] for m in scores.get("matched_skills", [])]
    missing_skills = [s for s in required_skills if s not in matched_skill_names]

    matched_skills_text = "\n".join([
        f"  {m[0]} -> {m[1]} (similarity: {m[2]})"
        for m in scores.get("matched_skills", [])
    ]) or "  None"

    missing_skills_text = "\n".join([
        f"  {s}" for s in missing_skills
    ]) or "  None"

    work_history_text = "\n".join([
        f"  {w.get('role', '')} at {w.get('company', '')} "
        f"({w.get('start_date', '')} - {w.get('end_date', '')})"
        for w in candidate_data.get("work_history", [])
    ]) or "  No work history listed"

    prompt = PROMPT_TEMPLATE.format(
        job_title=jd_data.get("job_title", "Software Engineer"),
        required_skills=", ".join(required_skills),
        name=candidate.get("name", "Unknown"),
        rank=candidate.get("rank", "?"),
        final_score=scores.get("final_score", 0),
        semantic_score=scores.get("semantic_score", 0),
        skill_score=scores.get("skill_score", 0),
        experience_score=scores.get("experience_score", 0),
        education_score=scores.get("education_score", 0),
        matched_skills=matched_skills_text,
        missing_skills=missing_skills_text,
        work_history=work_history_text,
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()