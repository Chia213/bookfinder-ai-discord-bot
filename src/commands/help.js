const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('bookhelp')
    .setDescription('Get help with using the BookFinder bot and its commands'),

  async execute(interaction) {
    const helpEmbed = new EmbedBuilder()
      .setColor(0x0099FF)
      .setTitle('📚 BookFinder AI Bot - Help Guide')
      .setDescription('I can help you find books and get recommendations based on your preferences. Here are the commands you can use:')
      .addFields(
        { 
          name: '/findbook [query]', 
          value: 'Search for books based on description, title, author, or theme.\n' +
                 'Example: `/findbook a mystery novel set in Paris with a female detective`' 
        },
        { 
          name: '/recommend [preferences]', 
          value: 'Get personalized book recommendations based on your preferences.\n' +
                 'Example: `/recommend fantasy books with strong character development like Name of the Wind`' 
        },
        { 
          name: 'Tips for Better Results', 
          value: '• Be specific about genres, themes, or plot elements\n' +
                 '• Mention similar books or authors you enjoy\n' +
                 '• Include time periods or settings if relevant\n' +
                 '• Specify if you\'re looking for a specific reading level or audience'
        }
      )
      .setFooter({ 
        text: 'BookFinder AI uses OpenAI and book databases to provide intelligent recommendations' 
      });

    await interaction.reply({ embeds: [helpEmbed] });
  },
}; 