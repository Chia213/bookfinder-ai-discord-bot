import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime, timedelta
from src.services.rag_service import RAGService
import json

logger = logging.getLogger('bookfinder.commands.analytics')

class AnalyticsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(
        name="myhistory",
        description="View your recent search history and preferences"
    )
    async def myhistory(self, interaction: discord.Interaction):
        """
        Show user's search history and personalized insights
        """
        await interaction.response.defer()
        
        try:
            # Get user's search history
            history = RAGService.get_user_history(interaction.user.id, limit=10)
            
            if not history:
                embed = discord.Embed(
                    title="📚 Your Search History",
                    description="You haven't made any searches yet! Try using `/findbook` or `/recommend` to get started.",
                    color=discord.Color.blue()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Get user preferences analysis
            preferences = RAGService.get_user_preferences(interaction.user.id)
            
            # Create main embed
            embed = discord.Embed(
                title="📚 Your BookFinder AI History",
                description=f"Here's your search activity and preferences",
                color=discord.Color.green()
            )
            
            # Add search history
            recent_searches = []
            for entry in history[-5:]:  # Last 5 searches
                timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%m/%d %H:%M")
                command = entry.get("command", "unknown").title()
                query = entry.get("query", "")[:50] + ("..." if len(entry.get("query", "")) > 50 else "")
                books_count = entry.get("books_found", 0)
                
                recent_searches.append(f"`{timestamp}` **{command}**: {query} ({books_count} books)")
            
            embed.add_field(
                name="🔍 Recent Searches",
                value="\n".join(recent_searches) if recent_searches else "No searches yet",
                inline=False
            )
            
            # Add favorite genres
            if preferences.get("genres"):
                embed.add_field(
                    name="📖 Your Favorite Genres",
                    value=", ".join(preferences["genres"][:5]),
                    inline=True
                )
            
            # Add favorite authors
            if preferences.get("authors"):
                embed.add_field(
                    name="✍️ Authors You've Discovered",
                    value=", ".join(preferences["authors"][:5]),
                    inline=True
                )
            
            # Add statistics
            embed.add_field(
                name="📊 Your Stats",
                value=f"Total Searches: **{preferences['total_interactions']}**\nCommands Used: **findbook**, **recommend**",
                inline=True
            )
            
            embed.set_footer(text="💡 Your search history helps me give better recommendations!")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error executing myhistory command: {e}")
            await interaction.followup.send(
                "Sorry, I couldn't retrieve your search history right now. Please try again later."
            )
    
    @app_commands.command(
        name="analytics",
        description="View system-wide usage analytics"
    )
    async def analytics(self, interaction: discord.Interaction):
        """
        Show system-wide analytics (for demonstration purposes)
        """
        await interaction.response.defer()
        
        try:
            # Get system analytics
            analytics = RAGService.get_analytics()
            
            embed = discord.Embed(
                title="🤖 BookFinder AI Analytics Dashboard",
                description="System-wide usage statistics",
                color=discord.Color.purple()
            )
            
            # Add analytics fields
            embed.add_field(
                name="📊 Total Usage",
                value=f"**{analytics.get('total_interactions', 0)}** total searches\n**{analytics.get('unique_users', 0)}** unique users",
                inline=True
            )
            
            embed.add_field(
                name="⚡ Command Breakdown",
                value=f"**/findbook**: {analytics.get('findbook_uses', 0)} uses\n**/recommend**: {analytics.get('recommend_uses', 0)} uses",
                inline=True
            )
            
            # Last activity
            if analytics.get('last_activity'):
                last_activity = datetime.fromisoformat(analytics['last_activity']).strftime("%Y-%m-%d %H:%M")
                embed.add_field(
                    name="🕒 Last Activity",
                    value=last_activity,
                    inline=True
                )
            
            # Add demonstration note
            embed.add_field(
                name="📝 RAG System Features",
                value="✅ User interaction logging\n✅ Search history tracking\n✅ Preference analysis\n✅ Personalized recommendations\n✅ Usage analytics",
                inline=False
            )
            
            embed.set_footer(text="📊 All user interactions are securely logged for improving recommendations")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error executing analytics command: {e}")
            await interaction.followup.send(
                "Sorry, I couldn't retrieve the analytics right now. Please try again later."
            )
    
    @app_commands.command(
        name="clearhistory",
        description="Clear your personal search history"
    )
    async def clearhistory(self, interaction: discord.Interaction):
        """
        Allow users to clear their search history (GDPR compliance)
        """
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Create confirmation embed
            embed = discord.Embed(
                title="⚠️ Clear Search History",
                description="Are you sure you want to clear your search history?\n\n**This will:**\n• Delete all your previous searches\n• Remove your preference data\n• Reset personalization features\n\n*This action cannot be undone.*",
                color=discord.Color.orange()
            )
            
            # Create view with confirmation buttons
            view = ClearHistoryView(interaction.user.id)
            
            await interaction.followup.send(embed=embed, view=view)
            
        except Exception as e:
            logger.error(f"Error executing clearhistory command: {e}")
            await interaction.followup.send(
                "Sorry, I couldn't process your request right now. Please try again later.",
                ephemeral=True
            )

class ClearHistoryView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id
    
    @discord.ui.button(label="Yes, Clear My History", style=discord.ButtonStyle.danger)
    async def confirm_clear(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Only the original user can confirm this action.", ephemeral=True)
            return
        
        try:
            # Actually implement data deletion for GDPR compliance
            deleted_count = self._delete_user_data(str(self.user_id))
            
            embed = discord.Embed(
                title="✅ History Cleared",
                description=f"Your search history has been cleared successfully.\n\n**Deleted:** {deleted_count} interactions\n\nFuture searches will start building a new preference profile.",
                color=discord.Color.green()
            )
            
            await interaction.response.edit_message(embed=embed, view=None)
            
        except Exception as e:
            logger.error(f"Error clearing user history: {e}")
            await interaction.response.send_message(
                "Sorry, there was an error clearing your history. Please try again later.",
                ephemeral=True
            )
    
    def _delete_user_data(self, user_id: str) -> int:
        """
        Actually delete user data from the log file (GDPR compliance)
        
        Args:
            user_id (str): User ID to delete data for
            
        Returns:
            int: Number of interactions deleted
        """
        import os
        from src.services.rag_service import RAGService
        
        if not os.path.exists(RAGService.LOG_FILE):
            return 0
            
        # Read all lines and filter out user's data
        remaining_lines = []
        deleted_count = 0
        
        try:
            with open(RAGService.LOG_FILE, "r", encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry.get("user_id") == user_id:
                            deleted_count += 1
                        else:
                            remaining_lines.append(line.strip())
                    except json.JSONDecodeError:
                        # Keep malformed lines
                        remaining_lines.append(line.strip())
            
            # Write back the filtered data
            with open(RAGService.LOG_FILE, "w", encoding='utf-8') as f:
                for line in remaining_lines:
                    f.write(line + "\n")
                    
            logger.info(f"GDPR: Deleted {deleted_count} interactions for user {user_id}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error deleting user data: {e}")
            raise
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel_clear(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Only the original user can cancel this action.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="❌ Cancelled",
            description="Your search history remains intact.",
            color=discord.Color.blue()
        )
        
        await interaction.response.edit_message(embed=embed, view=None)

async def setup(bot):
    await bot.add_cog(AnalyticsCog(bot)) 