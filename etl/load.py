import sqlite3
from pandas import DataFrame

def load(df: DataFrame, airflow: bool = False):
    
    if airflow:
        db_path = "/opt/airflow/data/movies.db"
    else:
        db_path = "local_data/movies.db"
    
    conn = sqlite3.connect(db_path)
    df.to_sql("movies", conn, if_exists="replace", index=False)
    conn.close()