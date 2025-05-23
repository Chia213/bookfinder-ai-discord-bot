require('dotenv').config();

module.exports = {
  // Discord configuration
  discord: {
    token: process.env.DISCORD_TOKEN,
    prefix: process.env.BOT_PREFIX || '!',
  },
  
  // OpenAI configuration
  openai: {
    apiKey: process.env.OPENAI_API_KEY,
    model: process.env.AI_MODEL || 'gpt-3.5-turbo',
    maxTokens: 500,
  },
  
  // Book API configuration
  bookApi: {
    google: {
      apiKey: process.env.GOOGLE_BOOKS_API_KEY,
      baseUrl: 'https://www.googleapis.com/books/v1',
    },
    openLibrary: {
      baseUrl: 'https://openlibrary.org/api',
    },
  },
}; 