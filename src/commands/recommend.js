const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const openaiService = require('../services/openaiService');
const bookService = require('../services/bookService');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('recommend')
    .setDescription('Get book recommendations based on your preferences')
    .addStringOption(option =>
      option.setName('preferences')
        .setDescription('Describe books, authors, or genres you enjoy')
        .setRequired(true)),

  async execute(interaction) {
    await interaction.deferReply();
    
    try {
      const preferences = interaction.options.getString('preferences');
      
      // Create a recommendation prompt for the AI
      const systemPrompt = `
        You are a knowledgeable librarian who helps users find books they might enjoy.
        Based on the user's preferences, suggest 3-5 specific books they might like.
        For each book, include:
        - Title (exact spelling)
        - Author name (exact spelling)
        - A brief reason why it matches their preferences
        - Genre or category

        Format your response as a JSON array of book objects with these fields.
        Be specific with book titles and authors so they can be easily searched.
      `;
      
      // Get recommendations from AI
      const aiRecommendationJson = await openaiService.generateResponse(
        `Based on these preferences, recommend specific books: ${preferences}`,
        systemPrompt
      );
      
      let recommendations;
      try {
        recommendations = JSON.parse(aiRecommendationJson);
        
        // Validate the format
        if (!Array.isArray(recommendations)) {
          throw new Error('Response is not an array');
        }
      } catch (error) {
        console.error('Error parsing AI recommendations:', error);
        console.log('Raw AI response:', aiRecommendationJson);
        
        // Send the raw response if parsing fails
        await interaction.editReply(`Here are some book recommendations based on your preferences:\n\n${aiRecommendationJson}`);
        return;
      }
      
      // Find details for the first 3 recommended books
      const bookDetails = [];
      
      for (const rec of recommendations.slice(0, 3)) {
        try {
          // Search for book details
          const searchQuery = {
            title: rec.title,
            author: rec.author
          };
          
          const books = await bookService.searchBooks(searchQuery);
          
          if (books.length > 0) {
            // Add the book with the reason from AI
            const book = books[0];
            book.reason = rec.reason;
            bookDetails.push(book);
          } else {
            // If book not found, just add the AI recommendation
            bookDetails.push({
              title: rec.title,
              authors: [rec.author],
              reason: rec.reason,
              description: 'No additional details found',
              categories: [rec.genre].filter(Boolean)
            });
          }
        } catch (error) {
          console.error(`Error fetching details for book "${rec.title}":`, error);
          // Continue with other recommendations
        }
      }
      
      // Create a response message
      let responseContent = `📚 **Book Recommendations Based On Your Preferences**\n\nHere are some books you might enjoy based on your preferences: "${preferences}"\n`;
      
      // Create embeds for the books
      const embeds = bookDetails.map(book => {
        const embed = new EmbedBuilder()
          .setTitle(book.title)
          .setAuthor({ name: book.authors?.join(', ') || 'Unknown Author' })
          .setDescription(book.reason || 'Recommended based on your preferences')
          .addFields(
            { name: 'Description', value: (book.description?.substring(0, 200) + (book.description?.length > 200 ? '...' : '')) || 'No description available' },
            { name: 'Genre', value: book.categories?.join(', ') || 'Unknown', inline: true }
          )
          .setColor(0x00FF99);
          
        if (book.imageLinks?.thumbnail) {
          embed.setThumbnail(book.imageLinks.thumbnail);
        }
        
        if (book.previewLink) {
          embed.setURL(book.previewLink);
        }
        
        return embed;
      });
      
      // Send the response
      await interaction.editReply({ content: responseContent, embeds });
      
    } catch (error) {
      console.error('Error executing recommend command:', error);
      await interaction.editReply('Sorry, I encountered an error while generating book recommendations. Please try again later.');
    }
  },
}; 