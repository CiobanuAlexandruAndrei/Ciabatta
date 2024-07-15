def calculate_keyword_difficulty(competition_index, search_volume, cpc, max_search_volume=500000, max_cpc=50):
    # Ensure values are not None
    competition_index = competition_index or 0
    search_volume = search_volume or 0
    cpc = cpc or 0
    
    norm_competition_index = competition_index / 100
    norm_search_volume = search_volume / max_search_volume
    norm_cpc = cpc / max_cpc
    
    difficulty_score = (norm_competition_index * 0.5) + (norm_search_volume * 0.3) + (norm_cpc * 0.2)
    
    difficulty_score = difficulty_score * 100
    
    return difficulty_score