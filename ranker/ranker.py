def rank_candidates(scored_candidates):
    sorted_candidates = sorted(
        scored_candidates,
        key=lambda x: x["scores"]["final_score"],
        reverse=True
    )

    for index, candidate in enumerate(sorted_candidates):
        candidate["rank"] = index + 1

    return sorted_candidates