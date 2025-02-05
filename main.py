import discord
from discord.ext import commands
import os
from help_cog import help_cog
from music_cog import music_cog
from GoogleScrapper import GoogleScrapper
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

#client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

# @client.event
# async def on_ready():
#     print('We have logged in!')
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$play'):
#         await message.channel.send('Playing')

# bot.remove_command("help")
#
# bot.add_cog(help_cog(bot))
# bot.add_cog(music_cog(bot))
# @client.command()
# async def hello(ctx):
#     await ctx.send('Hello')

bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(GoogleScrapper(bot))


bot.run(DISCORD_TOKEN)
