import discord
from discord import app_commands
from discord.ext import commands
import logging
from src.services.openai_service import OpenAIService
from src.services.book_service import BookService
from src.services.rag_service import RAGService

logger = logging.getLogger('bookfinder.commands.findbook')

class FindBookCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(
        name="findbook",
        description="Find books based on description, title, author, or theme"
    )
    @app_commands.describe(
        query="Describe the book you're looking for"
    )
    async def findbook(self, interaction: discord.Interaction, query: str):
        """
        Slash command to find books based on user's description
        """
        await interaction.response.defer()
        
        try:
            # Let the AI parse the natural language query
            search_params = await OpenAIService.parse_book_query(query)
            logger.info(f"Parsed search parameters: {search_params}")
            
            # Check if AI returned an error (for impossible queries)
            if "error" in search_params:
                error_message = search_params["error"]
                
                # Log the interaction with RAG
                RAGService.log_interaction(
                    user_id=interaction.user.id,
                    query=query,
                    books_found=[],
                    command_type="findbook",
                    response_text=error_message
                )
                
                await interaction.followup.send(error_message)
                return
            
            # Search for books
            books = await BookService.search_books(search_params)
            
            if not books:
                # If no books found, use AI to provide a helpful response
                ai_response = await OpenAIService.enhance_book_results([], query)
                
                # Log the interaction with RAG
                RAGService.log_interaction(
                    user_id=interaction.user.id,
                    query=query,
                    books_found=[],
                    command_type="findbook",
                    response_text=ai_response
                )
                
                await interaction.followup.send(ai_response)
                return
            
            # Get AI to enhance the book results with context
            ai_response = await OpenAIService.enhance_book_results(books, query)
            
            # Log the interaction with RAG BEFORE creating embeds
            RAGService.log_interaction(
                user_id=interaction.user.id,
                query=query,
                books_found=books,
                command_type="findbook",
                response_text=ai_response
            )
            
            # Create embeds for the books
            embeds = []
            for book in books[:3]:  # Limit to top 3 books
                embed = discord.Embed(
                    title=book['title'],
                    description=book.get('description', 'No description available')[:300] + 
                               ('...' if book.get('description', '') and len(book['description']) > 300 else ''),
                    color=discord.Color.blue(),
                    url=book.get('previewLink', '')
                )
                
                embed.set_author(name=", ".join(book.get('authors', ['Unknown Author'])))
                
                # Add fields
                embed.add_field(
                    name="Published", 
                    value=book.get('publishedDate', 'Unknown'), 
                    inline=True
                )
                
                if book.get('categories'):
                    embed.add_field(
                        name="Categories", 
                        value=", ".join(book['categories']), 
                        inline=True
                    )
                
                # Add thumbnail if available
                if book.get('imageLinks', {}).get('thumbnail'):
                    embed.set_thumbnail(url=book['imageLinks']['thumbnail'])
                
                embeds.append(embed)
            
            # Send the AI's response first
            await interaction.followup.send(content=ai_response)
            
            # Then send the book embeds
            if embeds:
                await interaction.followup.send(embeds=embeds)
                
        except Exception as e:
            logger.error(f"Error executing findbook command: {e}")
            
            # Log the error interaction
            RAGService.log_interaction(
                user_id=interaction.user.id,
                query=query,
                books_found=[],
                command_type="findbook",
                response_text="Error occurred"
            )
            
            await interaction.followup.send(
                "Sorry, I encountered an error while searching for books. Please try again later."
            )

async def setup(bot):
    await bot.add_cog(FindBookCog(bot)) 