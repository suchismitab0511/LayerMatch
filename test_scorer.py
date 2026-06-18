from extractor.jd_extractor import extract_jd_structure
from extractor.candidate_extractor import extract_candidate_structure
from scorer.scorer import calculate_final_score
from parser.resume_parser import parse_all_resumes
import json

with open("data/job_description.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

jd_data = extract_jd_structure(jd_text)
print("JD extracted.\n")

resumes = parse_all_resumes("data/resumes/")

for filename, resume_text in resumes.items():
    if not resume_text.strip():
        continue

    candidate_data = extract_candidate_structure(resume_text)
    result = calculate_final_score(jd_data, candidate_data, jd_text, resume_text)

    print(f"--- {filename} ({candidate_data.get('name', 'Unknown')}) ---")
    print(json.dumps(result, indent=2))
    print()