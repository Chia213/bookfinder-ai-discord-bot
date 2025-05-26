import discord
from discord import app_commands
from discord.ext import commands
import json
import logging
from src.services.openai_service import OpenAIService
from src.services.book_service import BookService
from src.services.rag_service import RAGService

logger = logging.getLogger('bookfinder.commands.recommend')

class RecommendCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(
        name="recommend",
        description="Get book recommendations based on your preferences"
    )
    @app_commands.describe(
        preferences="Describe books, authors, or genres you enjoy"
    )
    async def recommend(self, interaction: discord.Interaction, preferences: str):
        """
        Slash command to get book recommendations based on user preferences
        """
        await interaction.response.defer()
        
        book_details = []  # Initialize here for logging
        success_response = None
        
        try:
            # Handle vague preferences
            if preferences.lower() in ["i have no idea", "no idea", "don't know", "anything", "surprise me", "jag vet inte", "ingen aning"]:
                # Get user's previous preferences from RAG
                user_prefs = RAGService.get_user_preferences(interaction.user.id)
                
                if user_prefs.get("genres") or user_prefs.get("authors"):
                    # Use their history for recommendations
                    enhanced_preferences = f"Based on your previous interests in {', '.join(user_prefs.get('genres', [])[:3])}, recommend something new"
                else:
                    # Give popular/general recommendations
                    enhanced_preferences = "Recommend popular, well-reviewed books across different genres for someone exploring new reads"
            else:
                # Check if user has previous preferences from RAG
                user_prefs = RAGService.get_user_preferences(interaction.user.id)
                enhanced_preferences = preferences
                
                if user_prefs.get("genres") or user_prefs.get("authors"):
                    enhanced_preferences += f" (Previously liked: {', '.join(user_prefs.get('genres', [])[:3])})"
            
            # Create a recommendation prompt for the AI
            system_prompt = """
            You are a knowledgeable librarian who helps users find books they might enjoy.
            Based on the user's preferences, suggest 3-5 specific books they might like.
            
            IMPORTANT: Always respond with a simple, conversational recommendation text, NOT JSON.
            Include:
            - Book titles and authors
            - Brief reasons why each book matches their preferences
            - Mix of different genres if preferences are vague
            
            Keep your response natural and conversational, like a librarian talking to a customer.
            """
            
            # Get recommendations from AI
            ai_recommendation = await OpenAIService.generate_response(
                f"Based on these preferences, recommend specific books: {enhanced_preferences}",
                system_prompt
            )
            
            # Try to extract book titles and authors from the AI response for searching
            book_search_prompt = """
            Extract book titles and authors from this recommendation text.
            Return as JSON array with format: [{"title": "Book Title", "author": "Author Name"}]
            If you can't extract clear titles/authors, return empty array: []
            """
            
            try:
                book_search_response = await OpenAIService.generate_response(
                    f"Extract books from: {ai_recommendation}",
                    book_search_prompt
                )
                book_searches = json.loads(book_search_response)
                
                # Search for actual book details
                for search in book_searches[:3]:
                    try:
                        search_query = {
                            'title': search.get('title'),
                            'author': search.get('author')
                        }
                        
                        books = await BookService.search_books(search_query)
                        
                        if books and len(books) > 0:
                            book_details.append(books[0])
                    except Exception as e:
                        logger.error(f"Error searching for book: {e}")
                        continue
                        
            except Exception as e:
                logger.info(f"Could not extract book details for searching: {e}")
                # Continue without book details - just use AI response
            
            # Create response message
            response_content = f"📚 **Book Recommendations**\n\n{ai_recommendation}"
            
            if user_prefs.get("total_interactions", 0) > 0:
                response_content += f"\n\n💡 *Based on your {user_prefs['total_interactions']} previous searches, I've personalized these recommendations!*"
            
            # Create embeds for found books (if any)
            embeds = []
            for book in book_details[:3]:
                embed = discord.Embed(
                    title=book['title'],
                    description=book.get('description', 'No description available')[:300] + 
                               ('...' if book.get('description', '') and len(book['description']) > 300 else ''),
                    color=discord.Color.green(),
                    url=book.get('previewLink', '')
                )
                
                embed.set_author(name=", ".join(book.get('authors', ['Unknown Author'])))
                
                # Add fields
                if book.get('publishedDate'):
                    embed.add_field(
                        name="Published", 
                        value=book.get('publishedDate', 'Unknown'), 
                        inline=True
                    )
                
                if book.get('categories'):
                    embed.add_field(
                        name="Genre", 
                        value=", ".join(book['categories']), 
                        inline=True
                    )
                
                # Add thumbnail if available
                if book.get('imageLinks', {}).get('thumbnail'):
                    embed.set_thumbnail(url=book['imageLinks']['thumbnail'])
                
                embeds.append(embed)
            
            # Send the response
            if embeds:
                await interaction.followup.send(content=response_content, embeds=embeds)
            else:
                await interaction.followup.send(content=response_content)
            
            # Log successful interaction
            success_response = f"Recommended books based on: {preferences}"
            RAGService.log_interaction(
                user_id=interaction.user.id,
                query=preferences,
                books_found=book_details,
                command_type="recommend",
                response_text=success_response
            )
            
        except Exception as e:
            logger.error(f"Error executing recommend command: {e}")
            
            # Provide a helpful fallback response
            fallback_message = """📚 **Book Recommendations**

Here are some popular books across different genres:

**Fantasy:** "The Name of the Wind" by Patrick Rothfuss
**Mystery:** "The Thursday Murder Club" by Richard Osman  
**Science Fiction:** "Project Hail Mary" by Andy Weir
**Romance:** "Beach Read" by Emily Henry
**Non-fiction:** "Atomic Habits" by James Clear

Try being more specific about genres or authors you like for better personalized recommendations!"""
            
            await interaction.followup.send(fallback_message)
            
            # Log the interaction
            RAGService.log_interaction(
                user_id=interaction.user.id,
                query=preferences,
                books_found=[],
                command_type="recommend",
                response_text="Fallback recommendations provided"
            )

async def setup(bot):
    await bot.add_cog(RecommendCog(bot)) 