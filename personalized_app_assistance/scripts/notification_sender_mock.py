import requests
import pandas as pd

def send_notification(customer_id, category, subcategory):
    print(f"Bildirim gönderiliyor: Müşteri ID {customer_id}, Kategori: {category} - {subcategory}")

def send_notifications(top_categories):
    for index, row in top_categories.iterrows():
        customer_id = row['customernumber']
        category = row['category']
        subcategory = row['subcategory']
        send_notification(customer_id, category, subcategory)

if __name__ == "__main__":
    from category_analysis_mock import analyze_categories
    from data_processing_mock import load_and_process_data
    
    df = load_and_process_data()
    top_categories = analyze_categories(df)
    send_notifications(top_categories)
