import discord
from discord import app_commands
from discord.ext import commands

class BookHelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(
        name="bookhelp",
        description="Get help with using the BookFinder bot and its commands"
    )
    async def bookhelp(self, interaction: discord.Interaction):
        """
        Help command to provide information about the bot's functionality
        """
        help_embed = discord.Embed(
            title="📚 BookFinder AI Bot - Help Guide",
            description="I can help you find books and get recommendations based on your preferences. Here are the commands you can use:",
            color=discord.Color.blue()
        )
        
        # Add command fields
        help_embed.add_field(
            name="/findbook [query]",
            value="Search for books based on description, title, author, or theme.\n" +
                  "Example: `/findbook a mystery novel set in Paris with a female detective`",
            inline=False
        )
        
        help_embed.add_field(
            name="/recommend [preferences]",
            value="Get personalized book recommendations based on your preferences.\n" +
                  "Example: `/recommend fantasy books with strong character development like Name of the Wind`",
            inline=False
        )
        
        help_embed.add_field(
            name="🔥 NEW: RAG System Commands",
            value="**`/myhistory`** - View your search history and preferences (private)\n" +
                  "**`/analytics`** - View system usage statistics\n" +
                  "**`/clearhistory`** - Clear your personal data",
            inline=False
        )
        
        help_embed.add_field(
            name="Tips for Better Results",
            value="• Be specific about genres, themes, or plot elements\n" +
                  "• Mention similar books or authors you enjoy\n" +
                  "• Include time periods or settings if relevant\n" +
                  "• Specify if you're looking for a specific reading level or audience",
            inline=False
        )
        
        help_embed.add_field(
            name="🤖 RAG Features",
            value="• **Personalized Recommendations**: Based on your search history\n" +
                  "• **Data Persistence**: All interactions are saved and analyzed\n" +
                  "• **Privacy Controls**: You can view and clear your data anytime\n" +
                  "• **Usage Analytics**: System-wide statistics available",
            inline=False
        )
        
        help_embed.set_footer(
            text="BookFinder AI uses OpenAI, Google Books API, and RAG system for intelligent recommendations"
        )
        
        await interaction.response.send_message(embed=help_embed)

async def setup(bot):
    await bot.add_cog(BookHelpCog(bot)) 