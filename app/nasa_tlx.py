def calculate_nasa_tlx_score(scores):
    # Пример простой обработки данных
    normalized_scores = {k: v / 10 for k, v in scores.items()}
    average_score = sum(normalized_scores.values()) / len(normalized_scores)
    return average_score
