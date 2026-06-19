import os
from parser.resume_parser import parse_all_resumes
from extractor.jd_extractor import extract_jd_structure
from extractor.candidate_extractor import extract_candidate_structure
from scorer.scorer import calculate_final_score
from ranker.ranker import rank_candidates
from explainer.explainer import explain_candidate
from output_writer.writer import save_results
from config import RESUME_DIR, JD_FILE

def validate_inputs():
    errors = []

    with open(JD_FILE, "r", encoding="utf-8") as f:
        jd_content = f.read().strip()
    if not jd_content:
        errors.append("job_description.txt is empty")

    resume_files = [
        f for f in os.listdir(RESUME_DIR)
        if f.endswith((".pdf", ".docx"))
    ]
    if not resume_files:
        errors.append("No PDF or DOCX files found in data/resumes/")

    if errors:
        print("\nERROR — Cannot proceed:")
        for e in errors:
            print(f"  - {e}")
        exit(1)

    print(f"  Found JD: {len(jd_content)} characters")
    print(f"  Found {len(resume_files)} resume(s)\n")


def main():
    print("\n" + "="*60)
    print("   LAYERMATCH — AI Candidate Ranking Engine")
    print("="*60 + "\n")

    print("Validating inputs...")
    validate_inputs()

    print("[1/5] Reading job description...")
    with open(JD_FILE, "r", encoding="utf-8") as f:
        jd_text = f.read()
    jd_data = extract_jd_structure(jd_text)
    print(f"      Job Title: {jd_data.get('job_title', 'Unknown')}")
    print(f"      Required Skills: {len(jd_data.get('required_skills', []))}\n")

    print("[2/5] Parsing resumes...")
    resumes = parse_all_resumes(RESUME_DIR)
    valid_resumes = {k: v for k, v in resumes.items() if v.strip()}
    print()

    print("[3/5] Extracting candidate profiles + scoring...")
    scored_candidates = []
    for filename, resume_text in valid_resumes.items():
        print(f"      Processing: {filename}")
        candidate_data = extract_candidate_structure(resume_text)
        scores = calculate_final_score(jd_data, candidate_data, jd_text, resume_text)
        scored_candidates.append({
            "filename": filename,
            "name": candidate_data.get("name", "Unknown"),
            "scores": scores,
            "candidate_data": candidate_data
        })
    print()

    print("[4/5] Ranking candidates...")
    ranked = rank_candidates(scored_candidates)
    print()

    print("[5/5] Generating explanations...")
    for candidate in ranked:
        print(f"      Explaining: {candidate['name']}")
        candidate["explanation"] = explain_candidate(candidate, jd_data)
    print()

    print("Saving results...")
    json_path, csv_path = save_results(ranked, jd_data)

    print("\n" + "="*60)
    print("   RANKING COMPLETE")
    print("="*60)
    for candidate in ranked:
        print(f"\n  #{candidate['rank']} {candidate['name']} "
              f"— Score: {candidate['scores']['final_score']}")
        print(f"     {candidate['explanation'][:120]}...")
    print()


if __name__ == "__main__":
    main()