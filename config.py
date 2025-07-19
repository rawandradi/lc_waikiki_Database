import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Generate a random secret key if not set in environment
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'lcwakiki_test')