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
            # Check if user has previous preferences from RAG
            user_prefs = RAGService.get_user_preferences(interaction.user.id)
            enhanced_preferences = preferences
            
            if user_prefs.get("genres") or user_prefs.get("authors"):
                enhanced_preferences += f" (Previously liked: {', '.join(user_prefs.get('genres', [])[:3])})"
            
            # Create a recommendation prompt for the AI
            system_prompt = """
            You are a knowledgeable librarian who helps users find books they might enjoy.
            Based on the user's preferences, suggest 3-5 specific books they might like.
            For each book, include:
            - Title (exact spelling)
            - Author name (exact spelling)
            - A brief reason why it matches their preferences
            - Genre or category

            Format your response as a JSON array of book objects with these fields.
            Be specific with book titles and authors so they can be easily searched.
            """
            
            # Get recommendations from AI
            ai_recommendation_json = await OpenAIService.generate_response(
                f"Based on these preferences, recommend specific books: {enhanced_preferences}",
                system_prompt
            )
            
            # Parse the JSON response
            try:
                recommendations = json.loads(ai_recommendation_json)
                
                # Validate the format
                if not isinstance(recommendations, list):
                    raise ValueError("Response is not an array")
                    
            except Exception as e:
                logger.error(f"Error parsing AI recommendations: {e}")
                logger.info(f"Raw AI response: {ai_recommendation_json}")
                
                # Send the raw response if parsing fails
                await interaction.followup.send(
                    f"Here are some book recommendations based on your preferences:\n\n{ai_recommendation_json}"
                )
                
                # Log after successful response
                RAGService.log_interaction(
                    user_id=interaction.user.id,
                    query=preferences,
                    books_found=[],
                    command_type="recommend",
                    response_text=ai_recommendation_json[:200]
                )
                return
                
            # Find details for the first 3 recommended books
            for rec in recommendations[:3]:
                try:
                    # Search for book details
                    search_query = {
                        'title': rec.get('title'),
                        'author': rec.get('author')
                    }
                    
                    books = await BookService.search_books(search_query)
                    
                    if books and len(books) > 0:
                        # Add the book with the reason from AI
                        book = books[0]
                        book['reason'] = rec.get('reason')
                        book_details.append(book)
                    else:
                        # If book not found, just add the AI recommendation
                        book_details.append({
                            'title': rec.get('title'),
                            'authors': [rec.get('author')],
                            'reason': rec.get('reason'),
                            'description': 'No additional details found',
                            'categories': [rec.get('genre')] if rec.get('genre') else []
                        })
                except Exception as e:
                    logger.error(f"Error fetching details for book \"{rec.get('title')}\": {e}")
                    # Continue with other recommendations
            
            # Create a response message
            response_content = f"📚 **Book Recommendations Based On Your Preferences**\n\nHere are some books you might enjoy based on your preferences: \"{preferences}\"\n"
            
            if user_prefs.get("total_interactions", 0) > 0:
                response_content += f"\n💡 *Based on your {user_prefs['total_interactions']} previous searches, I've personalized these recommendations!*\n"
            
            # Create embeds for the books
            embeds = []
            for book in book_details:
                embed = discord.Embed(
                    title=book['title'],
                    description=book.get('reason', 'Recommended based on your preferences'),
                    color=discord.Color.green(),
                    url=book.get('previewLink', '')
                )
                
                embed.set_author(name=", ".join(book.get('authors', ['Unknown Author'])))
                
                # Add fields
                embed.add_field(
                    name="Description", 
                    value=(book.get('description', 'No description available')[:200] + 
                           ('...' if book.get('description', '') and len(book['description']) > 200 else '')), 
                    inline=False
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
            await interaction.followup.send(content=response_content, embeds=embeds)
            
            # Log successful interaction ONLY after everything works
            success_response = f"Recommended {len(book_details)} books"
            RAGService.log_interaction(
                user_id=interaction.user.id,
                query=preferences,
                books_found=book_details,
                command_type="recommend",
                response_text=success_response
            )
            
        except Exception as e:
            logger.error(f"Error executing recommend command: {e}")
            
            # Only log error if we haven't already logged a success
            if success_response is None:
                RAGService.log_interaction(
                    user_id=interaction.user.id,
                    query=preferences,
                    books_found=book_details,  # May be empty or partial
                    command_type="recommend",
                    response_text="Error occurred"
                )
            
            await interaction.followup.send(
                "Sorry, I encountered an error while generating book recommendations. Please try again later."
            )

async def setup(bot):
    await bot.add_cog(RecommendCog(bot)) 