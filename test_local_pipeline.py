from etl.transform import transform
from etl.load import load

if __name__ == "__main__":
    df = transform()
    print(df.head())
    load(df)
    print("ETL Feito com sucesso!")