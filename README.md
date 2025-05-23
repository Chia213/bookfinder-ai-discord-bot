# BookFinder AI Discord Bot

A Discord bot that uses AI to help users find books based on descriptions, themes, or partial information.

## Features
- Search for books by title, author, genre, or description
- Get book recommendations based on user preferences
- View book details including summaries, ratings, and availability
- Natural language interaction powered by AI

## Technology Stack
- Python 3.8+ with discord.py
- OpenAI API for natural language processing
- Google Books API / Open Library API for book data
- Asynchronous programming for performance

## Setup and Installation
1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your API keys (see `.env.example`)
6. Run the bot: `python main.py`

## Commands
- `/findbook [query]` - Search for books with AI-powered understanding
- `/recommend [preferences]` - Get personalized book recommendations
- `/bookhelp` - View help and usage information

## Project Structure
- `/src` - Source code
  - `/cogs` - Discord command cogs
  - `/services` - Service modules for API interactions
  - `/utils` - Utility functions
- `/docs` - Documentation
- `main.py` - Main entry point 