import pandas as pd

def analyze_data(user_data_path, shop_data_path, purchase_history_path, negative_samples_path):
    # Verileri yükleme
    user_data = pd.read_csv(user_data_path)
    shop_data = pd.read_csv(shop_data_path)
    purchase_history = pd.read_csv(purchase_history_path)
    negative_samples = pd.read_csv(negative_samples_path)
    
    # Satın alma geçmişi ve mağaza verilerini birleştirme
    purchase_history = purchase_history.merge(shop_data, on='shop_id')

    # Kullanıcı başına toplam harcama ve satın alma sayısı
    user_totals = purchase_history.groupby('user_id').agg(
        total_spent=pd.NamedAgg(column='amount_spent', aggfunc='sum'),
        total_purchases=pd.NamedAgg(column='items_bought', aggfunc='sum'),
        total_transactions=pd.NamedAgg(column='shop_id', aggfunc='count')
    ).reset_index()

    # Kullanıcı başına kategori bazında harcama
    top_categories = purchase_history.groupby(['user_id', 'category']).agg(
        category_spent=pd.NamedAgg(column='amount_spent', aggfunc='sum')
    ).reset_index()

    # En çok ilgi duyulan 3 kategori
    top_3_categories = top_categories.sort_values(by=['user_id', 'category_spent'], ascending=[True, False]) \
                                     .groupby('user_id').head(3)

    # Kullanıcı başına kategori harcamaları pivot tablo
    category_summary = top_3_categories.pivot(index='user_id', columns='category', values='category_spent').fillna(0)
    category_summary.columns = [f"spent_on_{col}" for col in category_summary.columns]
    
    # Kullanıcı başına aylık ortalama harcama
    purchase_history['month'] = pd.to_datetime(purchase_history['purchase_date']).dt.to_period('M')
    monthly_spending = purchase_history.groupby(['user_id', 'month']).agg(
        monthly_spent=pd.NamedAgg(column='amount_spent', aggfunc='sum')
    ).groupby('user_id').agg(
        avg_monthly_spent=pd.NamedAgg(column='monthly_spent', aggfunc='mean')
    ).reset_index()
    
    # Kullanıcı özetlerini birleştirme
    user_summary = user_totals.merge(category_summary, on='user_id', how='left').merge(monthly_spending, on='user_id', how='left').fillna(0)
    
    # Kullanıcı verileri ile birleştirme
    final_summary = user_data.merge(user_summary, on='user_id', how='left').fillna(0)
    
    return final_summary

if __name__ == "__main__":
    user_data_path = 'data/user_data.csv'
    shop_data_path = 'data/shop_data.csv'
    purchase_history_path = 'data/purchase_history.csv'
    negative_samples_path = 'data/negative_samples.csv'
    
    final_summary = analyze_data(user_data_path, shop_data_path, purchase_history_path, negative_samples_path)
    final_summary.to_csv('data/user_summary.csv', index=False)
    print("Generated user summary report.")
