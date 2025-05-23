import discord
from discord.ext import commands
import asyncio
import os
import logging
import traceback
from src import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bookfinder')

# Initialize the bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot instance
bot = commands.Bot(
    command_prefix=config.BOT_PREFIX,
    intents=intents,
    help_command=None  # We'll create our own help command
)

# Event: Bot is ready
@bot.event
async def on_ready():
    logger.info(f'Bot logged in as {bot.user.name} ({bot.user.id})')
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{config.BOT_PREFIX}bookhelp"
        )
    )
    
    # Sync commands
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

# Event: Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
        return
        
    logger.error(f"Command error: {error}")
    logger.error(traceback.format_exc())
    
    await ctx.send("An error occurred while processing your command. Please try again later.")

# Function to load all cogs
async def load_extensions():
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'src.cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: {filename}')
            except Exception as e:
                logger.error(f'Failed to load extension {filename}: {e}')
                logger.error(traceback.format_exc())

# Main function to run the bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(config.DISCORD_TOKEN)

# Entry point
if __name__ == "__main__":
    asyncio.run(main()) 