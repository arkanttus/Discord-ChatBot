import discord
from discord.ext import commands
import settings
import random
from app_chatbot.bot import chatbot


class ChatBot(commands.Bot):
    def __init__(self, intents):
        super(ChatBot, self).__init__(command_prefix='$', intents=intents)

    async def on_ready(self):
        print(f'{self.user} ta ONLINE poah !')
    
    async def on_message(self, message):
        if message.author == self.user:
            return

        bot_msg = chatbot.get_response(message.content)
        response = str(bot_msg)
        print(response)
        await message.channel.send(response)
    
    
intents = discord.Intents.default()
intents.members = True
bot_client = ChatBot(intents)
bot_client.run(settings.TOKEN)