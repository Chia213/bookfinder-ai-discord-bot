# Environment Variables Setup

For the BookFinder AI Discord Bot to function properly, you need to set up environment variables with your API keys and Discord credentials. Create a `.env` file in the root directory of the project with the following structure:

```
# Discord Bot Token from https://discord.com/developers/applications
DISCORD_TOKEN=your_discord_bot_token_here
CLIENT_ID=your_discord_client_id_here

# OpenAI API Key from https://platform.openai.com/account/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Google Books API Key from https://console.cloud.google.com/
GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here

# Bot settings
BOT_PREFIX=!
AI_MODEL=gpt-3.5-turbo
```

## How to Get These Keys

### Discord Credentials
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create or select your application
3. In the "Bot" tab, you can find or reset your bot token
4. The Client ID is available in the "General Information" tab

### OpenAI API Key
1. Visit [OpenAI API Keys](https://platform.openai.com/account/api-keys)
2. Create a new API key if you don't have one
3. Copy the key (you won't be able to see it again)

### Google Books API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project if you don't have one
3. Enable the Google Books API
4. Create credentials (API key)
5. Copy the key

## Model Selection

The `AI_MODEL` variable determines which OpenAI model to use. Options include:
- `gpt-3.5-turbo` (faster, cheaper)
- `gpt-4` (more capable but more expensive)

For most book finding and recommendation tasks, `gpt-3.5-turbo` works well.

## Security Notes

- **NEVER commit your `.env` file to version control**
- Keep your API keys confidential
- Consider setting usage limits on your API keys to prevent unexpected charges
- Regularly rotate your keys if you suspect they might be compromised 