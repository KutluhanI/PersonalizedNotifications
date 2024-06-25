import pandas as pd

def load_and_process_data():
    data_path = "data/mock_data.csv"
    df = pd.read_csv(data_path)
    return df

if __name__ == "__main__":
    df = load_and_process_data()
    print(df.head())
