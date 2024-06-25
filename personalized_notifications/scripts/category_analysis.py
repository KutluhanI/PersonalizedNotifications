def analyze_categories(df):
    df.createOrReplaceTempView("pageviews")
    query = """
    SELECT customernumber, category, subcategory, COUNT(*) AS interest_count
    FROM pageviews
    GROUP BY customernumber, category, subcategory
    ORDER BY interest_count DESC
    """
    category_interest = df.sql(query)
    return category_interest

if __name__ == "__main__":
    from data_processing import load_and_process_data
    df = load_and_process_data()
    top_categories = analyze_categories(df)
    top_categories.show()
    top_categories.write.csv("../results/analysis_results.csv", header=True)
