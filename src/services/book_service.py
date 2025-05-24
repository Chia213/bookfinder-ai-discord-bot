import requests
import logging
import random
from src import config

logger = logging.getLogger('bookfinder.book')

class BookService:
    """Service for fetching book information from APIs"""
    
    @staticmethod
    async def search_google_books(params):
        """
        Search for books using Google Books API
        
        Args:
            params (dict): Search parameters
            
        Returns:
            list: Array of book data
        """
        try:
            query = ""
            
            # Build query string from parameters
            if params.get('title'):
                query += f"intitle:{params['title']} "
            if params.get('author'):
                query += f"inauthor:{params['author']} "
            if params.get('genre') or params.get('categories'):
                category = params.get('genre') or params.get('categories')
                query += f"subject:{category} "
            if params.get('general_query'):
                query += params['general_query']
                
            # If no query built, use the general query directly
            if not query.strip():
                query = params.get('general_query', 'bestseller books')
                
            # Add some randomization to avoid same results
            start_index = random.randint(0, 10)
                
            # Make API request
            response = requests.get(
                f"{config.GOOGLE_BOOKS_BASE_URL}/volumes",
                params={
                    'q': query.strip(),
                    'maxResults': 10,  # Get more results for variety
                    'startIndex': start_index,  # Add randomization
                    'key': config.GOOGLE_BOOKS_API_KEY
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'items' not in data:
                return []
                
            # Process results with null safety
            books = []
            for item in data['items']:
                volume_info = item.get('volumeInfo', {})
                books.append({
                    'id': item.get('id'),
                    'title': volume_info.get('title', 'Unknown Title'),
                    'authors': volume_info.get('authors') or ['Unknown Author'],
                    'description': volume_info.get('description', 'No description available'),
                    'publishedDate': volume_info.get('publishedDate'),
                    'categories': volume_info.get('categories') or [],
                    'imageLinks': volume_info.get('imageLinks'),
                    'previewLink': volume_info.get('previewLink')
                })
                
            return books
            
        except Exception as e:
            logger.error(f"Error searching Google Books: {e}")
            raise RuntimeError("Failed to search for books")
    
    @staticmethod
    async def get_book_details(book_id):
        """
        Get detailed information about a book by ID
        
        Args:
            book_id (str): Google Books volume ID
            
        Returns:
            dict: Detailed book data
        """
        try:
            response = requests.get(
                f"{config.GOOGLE_BOOKS_BASE_URL}/volumes/{book_id}",
                params={'key': config.GOOGLE_BOOKS_API_KEY}
            )
            
            response.raise_for_status()
            data = response.json()
            volume_info = data.get('volumeInfo', {})
            
            return {
                'id': data.get('id'),
                'title': volume_info.get('title', 'Unknown Title'),
                'authors': volume_info.get('authors') or ['Unknown Author'],
                'description': volume_info.get('description', 'No description available'),
                'publishedDate': volume_info.get('publishedDate'),
                'categories': volume_info.get('categories') or [],
                'pageCount': volume_info.get('pageCount'),
                'imageLinks': volume_info.get('imageLinks'),
                'previewLink': volume_info.get('previewLink'),
                'infoLink': volume_info.get('infoLink'),
                'language': volume_info.get('language'),
                'publisher': volume_info.get('publisher'),
                'averageRating': volume_info.get('averageRating'),
                'ratingsCount': volume_info.get('ratingsCount')
            }
            
        except Exception as e:
            logger.error(f"Error getting book details: {e}")
            raise RuntimeError("Failed to get book details")
    
    @staticmethod
    async def search_open_library(query):
        """
        Search Open Library as a fallback
        
        Args:
            query (str): Search query
            
        Returns:
            list: Array of book data
        """
        try:
            response = requests.get(
                f"{config.OPEN_LIBRARY_BASE_URL}/search.json",
                params={'q': query, 'limit': 10}
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'docs' not in data or len(data['docs']) == 0:
                return []
                
            # Process results with null safety
            books = []
            for book in data['docs']:
                books.append({
                    'id': book.get('key'),
                    'title': book.get('title', 'Unknown Title'),
                    'authors': book.get('author_name') or ['Unknown Author'],
                    'publishedDate': str(book.get('first_publish_year', '')),
                    'categories': book.get('subject') or [],
                    'imageLinks': {
                        'thumbnail': f"https://covers.openlibrary.org/b/id/{book.get('cover_i')}-M.jpg" if book.get('cover_i') else None
                    },
                    'previewLink': f"https://openlibrary.org{book.get('key')}"
                })
                
            return books
            
        except Exception as e:
            logger.error(f"Error searching Open Library: {e}")
            return []  # Return empty array as fallback
    
    @staticmethod
    async def search_books(params):
        """
        Search for books using both APIs, with Google Books as primary
        
        Args:
            params (dict): Search parameters
            
        Returns:
            list: Combined array of book data
        """
        try:
            # Try Google Books API first
            google_books = await BookService.search_google_books(params)
            
            # If we got results, return them
            if google_books and len(google_books) > 0:
                return google_books
                
            # Otherwise fall back to Open Library
            query_string = params.get('general_query', '') or \
                          (params.get('title', '') + ' ' + params.get('author', '')).strip()
                          
            return await BookService.search_open_library(query_string)
            
        except Exception as e:
            logger.error(f"Error in book search: {e}")
            # Try Open Library as last resort if Google Books fails
            query_string = params.get('general_query', '') or \
                          (params.get('title', '') + ' ' + params.get('author', '')).strip()
            return await BookService.search_open_library(query_string) 