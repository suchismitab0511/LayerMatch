import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

SCORING_WEIGHTS = {
    "semantic":   0.40,
    "skills":     0.25,
    "experience": 0.20,
    "education":  0.10,
    "recency":    0.05,
}

RESUME_DIR   = "data/resumes/"
JD_FILE      = "data/job_description.txt"
OUTPUT_FILE  = "output/ranked_candidates.json"