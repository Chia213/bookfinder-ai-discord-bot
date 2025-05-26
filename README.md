# 📚 BookFinder AI

*Discord bot that learns your reading taste and finds books you'll love*

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-blue?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-green?logo=openai&logoColor=white)](https://openai.com)

**What it does:** Type `/findbook fantasy magic` → Get personalized book recommendations that improve over time

**Tech:** Python • OpenAI • Discord.py • Google Books API

## 📸 See It In Action

### 🧠 **Smart Recommendations Based on Your History**
![RAG Personalized Recommendations](screenshots/rag-personalized-recommendations.png)
*"Based on your 10 previous searches, here are personalized samurai book recommendations"*

### 🔍 **Natural Language Search**  
![AI Book Search](screenshots/ai-book-search.png)
*Just type what you want: "murder mysteries" → AI finds and explains relevant books*

### 📊 **Track Your Reading Journey**
![User Analytics Dashboard](screenshots/user-analytics-dashboard.png)
*See your favorite genres, discovered authors, and complete search history*

### 📚 **Rich Book Display with Covers**
![Professional Book Display](screenshots/professional-book-display.png)
*Beautiful Discord embeds with book covers, descriptions, and metadata*

## 🎯 Commands

| Command | What it does | Example |
|---------|-------------|---------|
| `/findbook [query]` | Find books using natural language | `/findbook fantasy books with magic systems` |
| `/recommend [preferences]` | Get personalized suggestions | `/recommend I love epic fantasy and sci-fi` |
| `/myhistory` | View your search history | `/myhistory` |
| `/analytics` | See your reading patterns | `/analytics` |
| `/clearhistory` | Delete all your data (GDPR) | `/clearhistory` |
| `/bookhelp` | Show all commands | `/bookhelp` |

## ✨ Key Features

- **🤖 Smart Search** - Understands "books like Harry Potter but darker"
- **🧠 Learns Your Taste** - Gets better recommendations over time  
- **📊 Reading Analytics** - Discover your favorite genres and authors
- **🔒 Privacy First** - Delete your data anytime
- **📚 Rich Results** - Book covers, descriptions, and metadata

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/bookfinder-ai-discord-bot.git
cd bookfinder-ai-discord-bot
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Add your API keys to .env file
DISCORD_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
GOOGLE_BOOKS_API_KEY=your_google_books_key

# 3. Run
python main.py
```

## 🎭 Usage Examples

**Natural Language Queries:**
```
/findbook fantasy books with complex magic systems like Brandon Sanderson
/findbook mystery novels set in Victorian London  
/findbook something similar to The Martian but fantasy
```

**Personalized Recommendations:**
```
/recommend I enjoyed The Name of the Wind and Dune
/recommend more books like what I've searched for before
/recommend dark fantasy with strong character development
```

## 🏗️ How It Works

### **The Learning System**
- Every search gets logged with your preferences
- AI analyzes your reading patterns over time
- Recommendations become more accurate with each interaction
- You can see exactly what data is stored and delete it anytime

### **Technology Stack**
- **Python 3.8+** - Core application
- **Discord.py 2.3+** - Discord integration
- **OpenAI GPT-3.5** - Natural language processing
- **Google Books API** - Book database
- **JSON Logging** - User preference storage

### **Privacy & Data**
- **GDPR Compliant** - Full data control
- **Transparent Storage** - See all your data with `/myhistory`
- **Easy Deletion** - Remove everything with `/clearhistory`
- **Local Storage** - Data stays in your server's log files

## 🏆 Project Highlights

- **🧠 AI Learning** - Implements retrieval-augmented generation (RAG)
- **📊 User Analytics** - Behavioral modeling and preference tracking
- **🔒 Privacy Engineering** - GDPR compliance from day one
- **🏗️ Clean Architecture** - Modular, maintainable codebase
- **📱 Modern UX** - Rich Discord embeds and intuitive commands

## 🏗️ Project Structure

```
bookfinder-ai-discord-bot/
├── src/                          # Source code directory
│   ├── cogs/                     # Discord command modules
│   │   ├── findbook.py           # AI-powered book search command
│   │   ├── recommend.py          # Personalized recommendations using RAG
│   │   ├── analytics.py          # User analytics & system statistics
│   │   ├── bookhelp.py           # Help and guidance commands
│   │   └── __init__.py
│   ├── services/                 # Business logic services
│   │   ├── openai_service.py     # OpenAI GPT-3.5 integration
│   │   ├── book_service.py       # Google Books & Open Library APIs
│   │   ├── rag_service.py        # RAG system & user interaction logging
│   │   └── __init__.py
│   ├── utils/                    # Utility functions
│   │   └── __init__.py
│   ├── bot.py                    # Main bot application
│   ├── config.py                 # Configuration management
│   └── __init__.py
├── screenshots/                  # Project demonstration images
│   ├── ai-book-search.png
│   ├── professional-book-display.png
│   ├── rag-personalized-recommendations.png
│   └── user-analytics-dashboard.png
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── user_interactions.log         # RAG system data storage
├── README.md                     # Project documentation
└── .gitignore                    # Git ignore patterns
```

### **🎯 Architecture Overview**

- **`src/cogs/`** - Modular Discord commands using discord.py's Cog system
- **`src/services/`** - Clean separation of business logic from presentation
- **`src/bot.py`** - Core Discord bot setup and event handling
- **`src/config.py`** - Centralized configuration and environment management
- **RAG System** - User interaction logging and personalized recommendations
- **Multi-API Design** - Primary/fallback pattern for reliability

## 🎓 Academic Context

This project demonstrates advanced AI concepts for an AI/ML course:
- **Retrieval-Augmented Generation (RAG)** - AI that learns from interactions
- **Natural Language Processing** - Understanding user intent
- **User Experience Design** - Making AI accessible through Discord
- **Privacy-Compliant AI** - Responsible data handling

## 🤝 Contributing

Built as an educational project showcasing practical AI implementation. The focus is on demonstrating how modern AI can be made user-friendly while respecting privacy.

## 📝 License

Open source project - feel free to learn from and build upon this code!

