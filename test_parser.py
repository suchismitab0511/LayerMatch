from parser.resume_parser import parse_all_resumes

resumes = parse_all_resumes("data/resumes/")

for name, text in resumes.items():
    print(f"\n--- {name} ---")
    print(text[:300])  # print first 300 characters only