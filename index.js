const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

client.once('ready', () => {
  console.log(`[ONLINE] Bot conectado com sucesso como ${client.user.tag}!`);
});

client.on('messageCreate', (message) => {
  if (message.author.bot) return;

  if (message.content === '!ping') {
    message.reply(`🏓 Pong! Latência: ${Math.round(client.ws.ping)}ms`);
  }

  // Novo comando de exemplo
  if (message.content === '!sobre') {
    message.reply('🤖 Bot gerenciado via BotCloud Manager e hospedado no Render!');
  }
});

client.login(process.env.DISCORD_TOKEN);