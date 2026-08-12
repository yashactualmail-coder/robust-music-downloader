from fuzzywuzzy import fuzz

def verify_match(expected_title: str, top_result: str, threshold: int = 80) -> bool:
    """
    Verifies if the top result matches the expected title.
    """
    # Clean strings: lowercase, remove common extra tags
    expected_clean = expected_title.lower().strip()
    result_clean = top_result.lower().strip()
    
    # Calculate similarity
    similarity = fuzz.partial_ratio(expected_clean, result_clean)
    
    if similarity >= threshold:
        return True
    return False
