import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
BOT_PREFIX = os.getenv('BOT_PREFIX', '!')

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-3.5-turbo')
MAX_TOKENS = 500

# Google Books API configuration
GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY')
GOOGLE_BOOKS_BASE_URL = 'https://www.googleapis.com/books/v1'

# Open Library API configuration
OPEN_LIBRARY_BASE_URL = 'https://openlibrary.org' 