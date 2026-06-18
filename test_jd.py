from extractor.jd_extractor import extract_jd_structure
import json

with open("data/job_description.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

result = extract_jd_structure(jd_text)
print(json.dumps(result, indent=2))