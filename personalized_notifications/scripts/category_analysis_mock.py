import pandas as pd

def analyze_categories(df):
    category_interest = df.groupby(['customernumber', 'category', 'subcategory']).size().reset_index(name='interest_count')
    category_interest = category_interest.sort_values(by='interest_count', ascending=False)
    return category_interest

if __name__ == "__main__":
    from mock_data_processing import load_and_process_data
    df = load_and_process_data()
    top_categories = analyze_categories(df)
    print(top_categories)
    top_categories.to_csv("../results/analysis_results.csv", index=False)
