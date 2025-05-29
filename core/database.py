import psycopg2
from config.db_config import DB_CONFIG

def connect_to_db():
    return psycopg2.connect(**DB_CONFIG)
