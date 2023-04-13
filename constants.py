from pathlib import Path
from urllib.parse import urljoin

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / 'images'

SERVER = 'http://localhost:8000'  # ip here, like http://127.0.0.1/

API_URL = urljoin(SERVER, 'api/')
RECIPES_NUMBER = 10
