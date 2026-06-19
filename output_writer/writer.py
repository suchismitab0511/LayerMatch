import json
import csv
import os
from datetime import datetime


def save_results(ranked_candidates, jd_data, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output = {
        "job_title": jd_data.get("job_title", "Unknown"),
        "generated_at": timestamp,
        "total_candidates": len(ranked_candidates),
        "ranked_candidates": []
    }

    for candidate in ranked_candidates:
        output["ranked_candidates"].append({
            "rank": candidate["rank"],
            "name": candidate["name"],
            "filename": candidate["filename"],
            "final_score": candidate["scores"]["final_score"],
            "score_breakdown": {
                "semantic": candidate["scores"]["semantic_score"],
                "skills": candidate["scores"]["skill_score"],
                "experience": candidate["scores"]["experience_score"],
                "education": candidate["scores"]["education_score"],
            },
            "matched_skills": candidate["scores"]["matched_skills"],
            "explanation": candidate.get("explanation", ""),
        })

    json_path = os.path.join(output_dir, f"ranked_candidates_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"  JSON saved: {json_path}")

    csv_path = os.path.join(output_dir, f"ranked_candidates_{timestamp}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Rank", "Name", "File", "Final Score",
            "Semantic", "Skills", "Experience", "Education", "Explanation"
        ])
        for candidate in output["ranked_candidates"]:
            writer.writerow([
                candidate["rank"],
                candidate["name"],
                candidate["filename"],
                candidate["final_score"],
                candidate["score_breakdown"]["semantic"],
                candidate["score_breakdown"]["skills"],
                candidate["score_breakdown"]["experience"],
                candidate["score_breakdown"]["education"],
                candidate["explanation"]
            ])
    print(f"  CSV saved: {csv_path}")

    return json_path, csv_path