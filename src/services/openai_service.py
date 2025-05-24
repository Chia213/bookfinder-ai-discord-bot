import openai
import json
import logging
from src import config

logger = logging.getLogger('bookfinder.openai')

# Configure OpenAI
client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    @staticmethod
    async def generate_response(prompt, system_prompt):
        """
        Generate a response using OpenAI API
        
        Args:
            prompt (str): The user's prompt
            system_prompt (str): The system message to guide the AI
            
        Returns:
            str: The AI response
        """
        try:
            response = client.chat.completions.create(
                model=config.AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=config.MAX_TOKENS,
                temperature=0.9,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {e}")
            # Return a fallback response when quota is exceeded
            if "insufficient_quota" in str(e) or "429" in str(e):
                return "I'm experiencing API quota limits, but I'll still search for books using the book databases."
            raise RuntimeError("Failed to generate AI response")
    
    @staticmethod
    async def parse_book_query(query):
        """
        Parse user's natural language query about books
        
        Args:
            query (str): User's natural language query
            
        Returns:
            dict: Extracted search parameters
        """
        system_prompt = """        You are a helpful AI assistant that extracts search parameters from user queries about books.                IMPORTANT: Always include a "general_query" field with the user's original query.                Extract the following information if present:        - title: Book title or partial title        - author: Author name          - genre: Genre or category        - general_query: Always include the original user query                Format your response as a valid JSON object. Example:        {"title": "samurai", "genre": "historical fiction", "general_query": "samurai books"}                If you cannot extract specific fields, return:        {"general_query": "user's original query here"}        """
        
        try:
            response = await OpenAIService.generate_response(query, system_prompt)
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error parsing book query: {e}")
            # Return basic object with full query as fallback
            return {"general_query": query}
    
    @staticmethod
    async def enhance_book_results(books, user_query):
        """
        Enhance book descriptions or generate recommendations
        
        Args:
            books (list): Array of book data
            user_query (str): The original user query
            
        Returns:
            str: Enhanced response about the books
        """
        if not books or len(books) == 0:
            return f"I couldn't find any books matching '{user_query}'. You might want to try different keywords or check the spelling."
        
        # Prepare book data for the AI
        books_data = []
        for book in books[:3]:  # Limit to top 3 books
            books_data.append({
                "title": book.get("title", "Unknown"),
                "author": ", ".join(book.get("authors", ["Unknown"])),
                "description": book.get("description", "No description available"),
                "publishedDate": book.get("publishedDate", "Unknown"),
                "categories": ", ".join(book.get("categories", ["Unknown"]))
            })
        
        try:
            system_prompt = """
            You are a knowledgeable librarian who helps users find books they might enjoy.
            Based on the user's query and the books found, create a helpful, conversational response that:
            1. Mentions the books found
            2. Provides brief context about each book's content, themes, or significance
            3. Explains why these books might match what the user is looking for
            
            Keep your response concise and focused on the books' relevance to the query.
            """
            
            prompt = f"User query: \"{user_query}\"\nBooks found: {json.dumps(books_data)}"
            return await OpenAIService.generate_response(prompt, system_prompt)
        except:
            # Fallback response when AI is unavailable
            book_titles = [book.get("title", "Unknown") for book in books[:3]]
            return f"Found {len(books)} books matching '{user_query}': {', '.join(book_titles)}" 