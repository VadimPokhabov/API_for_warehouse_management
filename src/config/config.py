import os
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv('POSTGRES_NAME')
DB_PASS = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB')
