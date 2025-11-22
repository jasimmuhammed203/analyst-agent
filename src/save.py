import pandas as pd

def save_to_csv(json_list, path="output/ai_startup_news.csv"):
    """
    Save the final structured list to a CSV file.
    """
    df = pd.DataFrame(json_list)
    df.to_csv(path, index=False)