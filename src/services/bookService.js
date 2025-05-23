const axios = require('axios');
const config = require('../../config/config');

class BookService {
  constructor() {
    this.googleBooksApi = axios.create({
      baseURL: config.bookApi.google.baseUrl,
      params: {
        key: config.bookApi.google.apiKey
      }
    });

    this.openLibraryApi = axios.create({
      baseURL: config.bookApi.openLibrary.baseUrl
    });
  }

  /**
   * Search for books using Google Books API
   * @param {Object} params - Search parameters
   * @returns {Promise<Array>} - Array of book data
   */
  async searchGoogleBooks(params) {
    try {
      let query = '';

      // Build query string from parameters
      if (params.title) query += `intitle:${params.title} `;
      if (params.author) query += `inauthor:${params.author} `;
      if (params.genre || params.categories) {
        const category = params.genre || params.categories;
        query += `subject:${category} `;
      }
      if (params.generalQuery) query += params.generalQuery;

      // Default to a general search if no specific parameters were provided
      if (!query.trim()) {
        query = params.generalQuery || 'popular books';
      }

      const response = await this.googleBooksApi.get('/volumes', {
        params: {
          q: query.trim(),
          maxResults: 5
        }
      });

      if (!response.data.items) {
        return [];
      }

      return response.data.items.map(item => {
        const volumeInfo = item.volumeInfo || {};
        return {
          id: item.id,
          title: volumeInfo.title || 'Unknown Title',
          authors: volumeInfo.authors || ['Unknown Author'],
          description: volumeInfo.description || 'No description available',
          publishedDate: volumeInfo.publishedDate,
          categories: volumeInfo.categories,
          imageLinks: volumeInfo.imageLinks,
          previewLink: volumeInfo.previewLink
        };
      });
    } catch (error) {
      console.error('Error searching Google Books:', error);
      throw new Error('Failed to search for books');
    }
  }

  /**
   * Get detailed information about a book by ID
   * @param {string} bookId - Google Books volume ID
   * @returns {Promise<Object>} - Detailed book data
   */
  async getBookDetails(bookId) {
    try {
      const response = await this.googleBooksApi.get(`/volumes/${bookId}`);
      const volumeInfo = response.data.volumeInfo || {};
      
      return {
        id: response.data.id,
        title: volumeInfo.title || 'Unknown Title',
        authors: volumeInfo.authors || ['Unknown Author'],
        description: volumeInfo.description || 'No description available',
        publishedDate: volumeInfo.publishedDate,
        categories: volumeInfo.categories,
        pageCount: volumeInfo.pageCount,
        imageLinks: volumeInfo.imageLinks,
        previewLink: volumeInfo.previewLink,
        infoLink: volumeInfo.infoLink,
        language: volumeInfo.language,
        publisher: volumeInfo.publisher,
        averageRating: volumeInfo.averageRating,
        ratingsCount: volumeInfo.ratingsCount
      };
    } catch (error) {
      console.error('Error getting book details:', error);
      throw new Error('Failed to get book details');
    }
  }

  /**
   * Search Open Library as a fallback
   * @param {string} query - Search query
   * @returns {Promise<Array>} - Array of book data
   */
  async searchOpenLibrary(query) {
    try {
      const response = await this.openLibraryApi.get('/search.json', {
        params: {
          q: query,
          limit: 5
        }
      });

      if (!response.data.docs || response.data.docs.length === 0) {
        return [];
      }

      return response.data.docs.map(book => {
        return {
          id: book.key,
          title: book.title || 'Unknown Title',
          authors: book.author_name || ['Unknown Author'],
          publishedDate: book.first_publish_year?.toString(),
          categories: book.subject,
          imageLinks: {
            thumbnail: book.cover_i 
              ? `https://covers.openlibrary.org/b/id/${book.cover_i}-M.jpg` 
              : null
          },
          previewLink: `https://openlibrary.org${book.key}`
        };
      });
    } catch (error) {
      console.error('Error searching Open Library:', error);
      return []; // Return empty array as fallback
    }
  }

  /**
   * Search for books using both APIs, with Google Books as primary
   * @param {Object} params - Search parameters
   * @returns {Promise<Array>} - Combined array of book data
   */
  async searchBooks(params) {
    try {
      // Try Google Books API first
      const googleBooks = await this.searchGoogleBooks(params);
      
      // If we got results, return them
      if (googleBooks.length > 0) {
        return googleBooks;
      }
      
      // Otherwise fall back to Open Library
      const queryString = params.generalQuery || 
                         (params.title ? params.title : '') + 
                         (params.author ? ' ' + params.author : '');
                         
      return this.searchOpenLibrary(queryString);
    } catch (error) {
      console.error('Error in book search:', error);
      // Try Open Library as last resort if Google Books fails
      const queryString = params.generalQuery || 
                         (params.title ? params.title : '') + 
                         (params.author ? ' ' + params.author : '');
      return this.searchOpenLibrary(queryString);
    }
  }
}

module.exports = new BookService(); 