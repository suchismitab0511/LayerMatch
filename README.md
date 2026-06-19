# LayerMatch

AI-powered candidate ranking system that ranks resumes against a job description using semantic understanding, not just keyword matching.

## What it does

1. Takes a job description and a folder of resumes (PDF/DOCX)
2. Extracts structured info from both using an LLM (Groq + Llama 3.3)
3. Compares them using sentence embeddings (semantic similarity, not exact keyword match)
4. Scores each candidate on multiple signals: semantic match, skills, experience, education
5. Ranks candidates and generates a plain-English explanation for each ranking
6. Saves results as JSON and CSV

## Tech Stack

- Python
- Groq API (Llama 3.3 70B) — for structured extraction and explanations
- sentence-transformers — for semantic embeddings (runs locally)
- pdfplumber / python-docx — for resume parsing
- NumPy — for similarity calculations

## How to run

```bash
git clone https://github.com/<your-username>/LayerMatch.git
cd LayerMatch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with:
```
GROQ_API_KEY=your_key_here
```

Add your job description to `data/job_description.txt` and resumes (PDF/DOCX) to `data/resumes/`.

Run:
```bash
python main.py
```

Results are saved in `output/`.

## Project Structure

```
LayerMatch/
├── main.py
├── config.py
├── parser/           - reads PDF/DOCX resumes
├── extractor/         - extracts structured JD + candidate data using LLM
├── scorer/             - embeddings + scoring logic
├── ranker/             - sorts candidates by score
├── explainer/         - generates explanation per candidate
├── output_writer/   - saves results
├── data/                 - input JD and resumes
└── output/             - ranked results (JSON + CSV)
```

## Scoring

Final score is a weighted combination of:
- Semantic match (40%)
- Skill match (25%)
- Experience fit (20%)
- Education fit (10%)
- Recency (5%) — currently a placeholder, not fully implemented yet

## Known Limitations

- Recency scoring not fully built yet
- No OCR support for scanned/image-only PDFs yet
- Skill matching threshold is not extensively tested

## Status

Core pipeline is working end-to-end. Still adding: comparison demo, UI, recency scoring.
