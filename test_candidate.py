from parser.resume_parser import parse_all_resumes
from extractor.candidate_extractor import extract_candidate_structure
import json

resumes = parse_all_resumes("data/resumes/")

for filename, text in resumes.items():
    if not text.strip():
        continue
    print(f"\n--- {filename} ---")
    result = extract_candidate_structure(text)
    print(json.dumps(result, indent=2))