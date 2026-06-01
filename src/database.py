import os
from langchain_community.utilities import SQLDatabase

def get_db_connection():
    """
    Get information about database from .env
    """
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    
    return SQLDatabase.from_uri(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
        sample_rows_in_table_info=3
    )