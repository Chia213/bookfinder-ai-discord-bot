# BookFinder AI Discord Bot - Setup Guide

This guide will help you set up and run the BookFinder AI Discord Bot on your local machine or server.

## Prerequisites

- [Node.js](https://nodejs.org/) (v16.9.0 or higher)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- [Discord Developer Account](https://discord.com/developers/applications)
- [OpenAI API Key](https://platform.openai.com/)
- [Google Cloud Platform Account](https://console.cloud.google.com/) (for Google Books API)

## Step 1: Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and name your bot
3. Navigate to the "Bot" tab and click "Add Bot"
4. Under the "Privileged Gateway Intents" section, enable:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
5. Save changes
6. Copy your bot's token by clicking "Reset Token" and then "Copy"
7. Under the "OAuth2" > "URL Generator" tab:
   - Select the "bot" and "applications.commands" scopes
   - Select the following bot permissions:
     - Send Messages
     - Embed Links
     - Attach Files
     - Read Message History
     - Use Slash Commands
8. Copy the generated URL and open it in your browser to invite the bot to your server

## Step 2: API Keys Setup

### OpenAI API Key
1. Create or log into your [OpenAI account](https://platform.openai.com/)
2. Navigate to the API section
3. Generate an API key and copy it

### Google Books API Key
1. Create or log into your [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Books API for your project
4. Create an API key from the "Credentials" section
5. Copy your API key

## Step 3: Local Setup

1. Clone the repository:
   ```
   git clone https://github.com/Chia213/bookfinder-ai-discord-bot.git
   cd bookfinder-ai-discord-bot
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file in the root directory with the following content:
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
   Replace all placeholder values with your actual API keys.

4. Deploy the slash commands to your Discord server:
   ```
   npm run deploy-commands
   ```

5. Start the bot:
   ```
   npm start
   ```

## Step 4: Usage

Once the bot is running and has been added to your server, you can use the following slash commands:

- `/findbook [query]` - Search for books based on your description
- `/recommend [preferences]` - Get book recommendations based on your preferences

Example queries:
- `/findbook a novel about time travel in Victorian England`
- `/recommend fantasy books similar to Lord of the Rings`

## Troubleshooting

- **Bot not responding**: Check that your bot token is correct and that the bot has the necessary permissions
- **Commands not working**: Ensure you've deployed the commands using `npm run deploy-commands`
- **API errors**: Verify your API keys and check your console logs for specific error messages
- **Rate limiting**: If you're hitting API rate limits, consider implementing caching or reducing usage

## Deployment

For production deployment, consider using services like:
- [Heroku](https://www.heroku.com/)
- [Railway](https://railway.app/)
- [Render](https://render.com/)
- [Digital Ocean](https://www.digitalocean.com/)

Make sure to set up your environment variables on your hosting platform. 