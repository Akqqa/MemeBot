#FEATURES
# Generate meme, with image and text specified
# Saves all images and text
# Allows "remixed" memes by randomly generating memes from previous images and text

import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
server = int(os.getenv('TEST_SERVER'))

bot = discord.Bot()

@bot.slash_command(guild_ids=[server], name="hello", description="hi")
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(guild_ids=[server], name="meme", description="Creates a meme!")
async def hello(ctx, toptext, bottomtext, image):
    img = requests.get(image).content
    # Get img id
    with open("imageid", "r") as file:
        id = file.readline()
    with open("imageid", "w") as file:
        file.write(str(int(id) + 1))

    with open("./images/" + id + ".jpg", "wb") as handler:
        handler.write(img)
    await ctx.respond("Hello!")

bot.run(token)