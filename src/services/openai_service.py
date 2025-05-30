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
        system_prompt = """
        You are a helpful AI assistant that extracts search parameters from user queries about books.
        
        IMPORTANT RULES:
        1. If the query asks for books by people you don't know (like "my neighbor"/"min granne", "my friend"/"min vän", "my teacher"/"min lärare"), respond in the same language as the query:
           - English: {"error": "I don't have information about books written by people in your personal life. Please provide the author's full name if you know it."}
           - Swedish: {"error": "Jag har ingen information om böcker skrivna av personer i ditt privatliv. Ange författarens fullständiga namn om du vet det."}
        
        2. If the query asks for impossible information (like future bestsellers, books based on personal mood without context), respond in the same language:
           - English: {"error": "I can't predict future bestsellers or read your mind. Please be more specific about genres, authors, or themes you're interested in."}
           - Swedish: {"error": "Jag kan inte förutsäga framtida bestsellers eller läsa dina tankar. Var mer specifik om genrer, författare eller teman du är intresserad av."}
        
        3. If the query is too vague or nonsensical, respond in the same language:
           - English: {"error": "I need more specific information to help you find books. Try mentioning a genre, author, or theme you're interested in."}
           - Swedish: {"error": "Jag behöver mer specifik information för att hjälpa dig hitta böcker. Försök nämna en genre, författare eller tema du är intresserad av."}
        
        For valid queries (in any language), extract the following information if present:
        - title: Book title or partial title
        - author: Author name (only if it's a real, known author)
        - genre: Genre or category
        - general_query: Always include the original user query
        
        Format your response as a valid JSON object. Example:
        {"title": "samurai", "genre": "historical fiction", "general_query": "samurai books"}
        
        If you cannot extract specific fields but the query is valid, return:
        {"general_query": "user's original query here"}
        """
        
        try:
            response = await OpenAIService.generate_response(query, system_prompt)
            
            # Check if response is None or empty
            if not response:
                logger.warning(f"OpenAI returned empty response for query: {query}")
                return {"general_query": query}
            
            # Try to parse JSON response
            try:
                parsed_response = json.loads(response)
                return parsed_response
            except json.JSONDecodeError as json_error:
                logger.warning(f"Failed to parse JSON response: {response}. Error: {json_error}")
                return {"general_query": query}
                
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
        
        # Prepare book data for the AI with null safety
        books_data = []
        for book in books[:3]:  # Limit to top 3 books
            authors = book.get("authors") or ["Unknown"]
            categories = book.get("categories") or ["Unknown"]
            
            books_data.append({
                "title": book.get("title", "Unknown"),
                "author": ", ".join(authors),
                "description": book.get("description", "No description available"),
                "publishedDate": book.get("publishedDate", "Unknown"),
                "categories": ", ".join(categories)
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