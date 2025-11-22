def is_high_information(article_text, min_length=200):
    """
    Filters out hype / low-information articles.
    """
    if len(article_text.strip()) < min_length:
        return False
    
    return True