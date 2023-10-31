import os.path

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path, verbose=True)

OPEN_AI_API_KEY = os.environ.get('OPEN_AI_API_KEY')
DB_CONNECTION = os.environ.get('DB_CONNECTION')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
