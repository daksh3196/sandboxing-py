def calculate_confidence(distances, analysis):
    best_distance = distances[0]
    retrieval_score = max(0.0, 1 - best_distance)

    # 2️⃣ Completeness confidence
    completeness = 1.0
    if not analysis.strengths:
        completeness -= 0.3
    if not analysis.mistakes:
        completeness -= 0.3
    if not analysis.training_focus:
        completeness -= 0.4

    # 3️⃣ Final confidence (weighted)
    final_confidence = (0.6 * retrieval_score) + (0.4 * completeness)

    return round(min(max(final_confidence, 0), 1), 2)
