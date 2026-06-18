import numpy as np
from scorer.embedder import get_embedding
from config import SCORING_WEIGHTS

SKILL_MATCH_THRESHOLD = 0.55


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def calculate_semantic_score(jd_text, resume_text):
    jd_embedding = get_embedding(jd_text)
    resume_embedding = get_embedding(resume_text)

    if jd_embedding is None or resume_embedding is None:
        return 0.0

    score = cosine_similarity(jd_embedding, resume_embedding)
    return float(max(0.0, min(1.0, score)))


def calculate_skill_score(jd_skills, candidate_skills):
    if not jd_skills:
        return 1.0, []
    if not candidate_skills:
        return 0.0, []  

    jd_embeddings = [get_embedding(skill) for skill in jd_skills]
    candidate_embeddings = [get_embedding(skill) for skill in candidate_skills]

    matched_count = 0
    matched_skills = []

    for jd_skill, jd_emb in zip(jd_skills, jd_embeddings):
        best_match_score = 0.0
        best_match_skill = None

        for cand_skill, cand_emb in zip(candidate_skills, candidate_embeddings):
            sim = cosine_similarity(jd_emb, cand_emb)
            if sim > best_match_score:
                best_match_score = sim
                best_match_skill = cand_skill

        if best_match_score >= SKILL_MATCH_THRESHOLD:
            matched_count += 1
            matched_skills.append((jd_skill, best_match_skill, round(float(best_match_score), 2)))

    score = matched_count / len(jd_skills)
    return float(score), matched_skills


def calculate_experience_score(jd_min_years, jd_max_years, candidate_years):
    if jd_min_years == 0 and jd_max_years == 0:
        return 1.0  # no experience requirement stated

    if candidate_years >= jd_min_years:
        if jd_max_years > 0 and candidate_years > jd_max_years:
            # overqualified, still good but not perfect penalty for mismatch
            return 0.85
        return 1.0

    # underqualified - partial credit based on how close they are
    if jd_min_years == 0:
        return 1.0
    gap_ratio = candidate_years / jd_min_years
    return float(max(0.0, gap_ratio))


def calculate_education_score(jd_education_requirement, candidate_education_list):
    if not jd_education_requirement:
        return 1.0
    if not candidate_education_list:
        return 0.0

    jd_edu_embedding = get_embedding(jd_education_requirement)

    best_score = 0.0
    for edu in candidate_education_list:
        degree_text = edu.get("degree", "")
        if not degree_text:
            continue
        cand_emb = get_embedding(degree_text)
        sim = cosine_similarity(jd_edu_embedding, cand_emb)
        if sim > best_score:
            best_score = sim

    return float(max(0.0, min(1.0, best_score)))


def calculate_final_score(jd_data, candidate_data, jd_full_text, resume_full_text):
    semantic_score = calculate_semantic_score(jd_full_text, resume_full_text)

    skill_score, matched_skills = calculate_skill_score(
        jd_data.get("required_skills", []),
        candidate_data.get("skills", [])
    )

    experience_score = calculate_experience_score(
        jd_data.get("min_experience_years", 0),
        jd_data.get("max_experience_years", 0),
        candidate_data.get("total_experience_years", 0)
    )

    education_score = calculate_education_score(
        jd_data.get("education_requirement", ""),
        candidate_data.get("education", [])
    )

    recency_score = 0.7  # placeholder, will be replaced with real recency logic later

    final_score = (
        semantic_score * SCORING_WEIGHTS["semantic"] +
        skill_score * SCORING_WEIGHTS["skills"] +
        experience_score * SCORING_WEIGHTS["experience"] +
        education_score * SCORING_WEIGHTS["education"] +
        recency_score * SCORING_WEIGHTS["recency"]
    )

    return {
        "final_score": round(float(final_score), 4),
        "semantic_score": round(semantic_score, 4),
        "skill_score": round(skill_score, 4),
        "experience_score": round(experience_score, 4),
        "education_score": round(education_score, 4),
        "recency_score": round(recency_score, 4),
        "matched_skills": matched_skills,
    }