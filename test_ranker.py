from parser.resume_parser import parse_all_resumes
from extractor.jd_extractor import extract_jd_structure
from extractor.candidate_extractor import extract_candidate_structure
from scorer.scorer import calculate_final_score
from ranker.ranker import rank_candidates
import json

with open("data/job_description.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

jd_data = extract_jd_structure(jd_text)
print("JD extracted.\n")

resumes = parse_all_resumes("data/resumes/")

scored_candidates = []

for filename, resume_text in resumes.items():
    if not resume_text.strip():
        continue

    candidate_data = extract_candidate_structure(resume_text)

    scores = calculate_final_score(
        jd_data,
        candidate_data,
        jd_text,
        resume_text
    )

    scored_candidates.append({
        "filename": filename,
        "name": candidate_data.get("name", "Unknown"),
        "scores": scores,
        "candidate_data": candidate_data
    })

ranked = rank_candidates(scored_candidates)

print("=== FINAL RANKING ===\n")
for candidate in ranked:
    print(f"Rank #{candidate['rank']}: {candidate['name']}")
    print(f"  Final Score:    {candidate['scores']['final_score']}")
    print(f"  Semantic:       {candidate['scores']['semantic_score']}")
    print(f"  Skills:         {candidate['scores']['skill_score']}")
    print(f"  Experience:     {candidate['scores']['experience_score']}")
    print(f"  Education:      {candidate['scores']['education_score']}")
    print(f"  Matched Skills: {candidate['scores']['matched_skills']}")
    print()