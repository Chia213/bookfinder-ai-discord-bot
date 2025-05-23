const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const openaiService = require('../services/openaiService');
const bookService = require('../services/bookService');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('findbook')
    .setDescription('Find books based on description, title, author, or theme')
    .addStringOption(option =>
      option.setName('query')
        .setDescription('Describe the book you\'re looking for')
        .setRequired(true)),

  async execute(interaction) {
    await interaction.deferReply();
    
    try {
      const query = interaction.options.getString('query');
      
      // Let the AI parse the natural language query
      const searchParams = await openaiService.parseBookQuery(query);
      console.log('Parsed search parameters:', searchParams);
      
      // Search for books
      const books = await bookService.searchBooks(searchParams);
      
      if (books.length === 0) {
        // If no books found, use AI to provide a helpful response
        const aiResponse = await openaiService.enhanceBookResults([], query);
        await interaction.editReply(aiResponse);
        return;
      }
      
      // Get AI to enhance the book results with context
      const aiResponse = await openaiService.enhanceBookResults(books, query);
      
      // Create embeds for the books
      const embeds = books.slice(0, 3).map(book => {
        const embed = new EmbedBuilder()
          .setTitle(book.title)
          .setAuthor({ name: book.authors?.join(', ') || 'Unknown Author' })
          .setDescription(book.description?.substring(0, 300) + (book.description?.length > 300 ? '...' : '') || 'No description available')
          .addFields(
            { name: 'Published', value: book.publishedDate || 'Unknown', inline: true },
            { name: 'Categories', value: book.categories?.join(', ') || 'Unknown', inline: true }
          )
          .setColor(0x0099FF);
          
        if (book.imageLinks?.thumbnail) {
          embed.setThumbnail(book.imageLinks.thumbnail);
        }
        
        if (book.previewLink) {
          embed.setURL(book.previewLink);
        }
        
        return embed;
      });
      
      // Send the AI's response first
      await interaction.editReply({ content: aiResponse });
      
      // Then send the book embeds
      if (embeds.length > 0) {
        await interaction.followUp({ embeds });
      }
    } catch (error) {
      console.error('Error executing findbook command:', error);
      await interaction.editReply('Sorry, I encountered an error while searching for books. Please try again later.');
    }
  },
}; 