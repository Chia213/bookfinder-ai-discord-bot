const { OpenAI } = require('openai');
const config = require('../../config/config');

class OpenAIService {
  constructor() {
    this.openai = new OpenAI({
      apiKey: config.openai.apiKey,
    });
  }

  /**
   * Generate a response using the OpenAI API
   * @param {string} prompt - The user's prompt
   * @param {string} systemPrompt - The system message to guide the AI
   * @returns {Promise<string>} - The AI response
   */
  async generateResponse(prompt, systemPrompt) {
    try {
      const response = await this.openai.chat.completions.create({
        model: config.openai.model,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: prompt }
        ],
        max_tokens: config.openai.maxTokens,
        temperature: 0.7,
      });

      return response.choices[0].message.content;
    } catch (error) {
      console.error('Error generating OpenAI response:', error);
      throw new Error('Failed to generate AI response');
    }
  }

  /**
   * Parse a user's book query to extract search parameters
   * @param {string} query - The user's natural language query about books
   * @returns {Promise<Object>} - Parsed search parameters
   */
  async parseBookQuery(query) {
    const systemPrompt = `
      You are a helpful AI assistant that extracts search parameters from user queries about books.
      Extract the following information if present:
      - Book title or partial title
      - Author name
      - Genre
      - Topics or themes
      - Publication year or time period
      - Any other relevant search criteria
      
      Format your response as a JSON object with these fields.
      Only include fields that you can extract from the query.
    `;

    try {
      const response = await this.generateResponse(query, systemPrompt);
      return JSON.parse(response);
    } catch (error) {
      console.error('Error parsing book query:', error);
      // Return a basic object with the full query as a fallback
      return { generalQuery: query };
    }
  }

  /**
   * Enhance book descriptions or generate recommendations
   * @param {Array} books - Array of book data
   * @param {string} userQuery - The original user query
   * @returns {Promise<string>} - Enhanced response about the books
   */
  async enhanceBookResults(books, userQuery) {
    if (!books || books.length === 0) {
      return this.generateResponse(
        `I couldn't find any books matching "${userQuery}". Can you suggest some similar books or authors?`,
        "You are a knowledgeable librarian who helps users find books they might enjoy. When no exact matches are found, suggest alternatives based on the query."
      );
    }

    const booksData = books.map(book => {
      return {
        title: book.title,
        author: book.authors?.join(', ') || 'Unknown',
        description: book.description || 'No description available',
        publishedDate: book.publishedDate || 'Unknown',
        categories: book.categories?.join(', ') || 'Unknown'
      };
    }).slice(0, 3); // Limit to top 3 books to keep context window manageable

    const systemPrompt = `
      You are a knowledgeable librarian who helps users find books they might enjoy.
      Based on the user's query and the books found, create a helpful, conversational response that:
      1. Mentions the books found
      2. Provides brief context about each book's content, themes, or significance
      3. Explains why these books might match what the user is looking for
      
      Keep your response concise and focused on the books' relevance to the query.
    `;

    return this.generateResponse(
      `User query: "${userQuery}"\nBooks found: ${JSON.stringify(booksData)}`,
      systemPrompt
    );
  }
}

module.exports = new OpenAIService(); 