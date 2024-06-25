import pandas as pd
import numpy as np

def load_mock_data():
    data_path = "data/mock_data.csv"
    response_data_path = "data/mock_response_data.csv"
    df = pd.read_csv(data_path)
    response_df = pd.read_csv(response_data_path)
    return df, response_df

def analyze_top_categories(df):
    # Her müşteri için ilgi duyulan kategorileri say
    category_interest = df.groupby(['customernumber', 'category', 'subcategory']).size().reset_index(name='interest_count')

    # Müşterilerin en çok ilgilendiği üç kategoriyi bul
    top_categories = category_interest.sort_values(by=['customernumber', 'interest_count'], ascending=[True, False])
    top_categories = top_categories.groupby('customernumber').head(3).reset_index(drop=True)
    return top_categories

def generate_report(df, top_categories):
    # Müşteri bazında özet bilgileri oluştur
    report = top_categories.groupby('customernumber').apply(lambda x: {
        'Top Categories': x[['category', 'subcategory']].values.tolist(),
        'Total Interactions': x['interest_count'].sum()
    }).reset_index()

    report_df = pd.DataFrame(report[0].tolist(), index=report['customernumber'])
    report_df.index.name = 'customernumber'
    return report_df

def main():
    df, response_df = load_mock_data()
    top_categories = analyze_top_categories(df)
    report = generate_report(df, top_categories)
    
    # Raporu kaydet
    report.to_csv("results/top_categories_report.csv", index=True)
    print(report.head())

if __name__ == "__main__":
    main()
