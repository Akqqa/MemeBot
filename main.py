#FEATURES
# Generate meme, with image and text specified
# Saves all images and text
# Allows "remixed" memes by randomly generating memes from previous images and text

import os
import discord
import requests
from PIL import Image
from generate import makeMeme
from dotenv import load_dotenv
from random import choice

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
server = int(os.getenv('HC'))

bot = discord.Bot()

@bot.slash_command(guild_ids=[server], name="hello", description="hi")
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(guild_ids=[server], name="meme", description="Creates a meme!")
async def meme(ctx, image, toptext="", bottomtext=""):
    try:
        img = requests.get(image).content
    except:
        await ctx.respond("Invalid Image Link")
        return
    if (not is_url_image(image)):
        await ctx.respond("Invalid Content")
        return
    # Get img id
    with open("imageid", "r") as file:
        id = file.readline()
    with open("imageid", "w") as file:
        file.write(str(int(id) + 1))
    # Write image to file
    with open("./images/" + id + ".jpg", "wb") as handler:
        handler.write(img)
    # Makes the meme
    makeMeme(toptext, bottomtext, "./images/" + id + ".jpg", "./memes/" + id + ".jpg")
    await ctx.respond(file=discord.File("./memes/" + id + ".jpg"))
    # Adds text to files
    with open("toptext.txt", "a") as file:
        file.write(toptext + "\n")
    with open("bottomtext.txt", "a") as file:
        file.write(bottomtext + "\n")

@bot.slash_command(guild_ids=[server], name="random", description="Generates a random meme!")
async def random(ctx):
    with open("toptext.txt", "r") as file:
        lines = file.readlines()
        toptext = choice(lines)
    with open("bottomtext.txt", "r") as file:
        lines = file.readlines()
        bottomtext = choice(lines)
    # Gets path
    path = choice(os.listdir("./images")) #change dir name to whatever
    print(path)
    # Gets id
    with open("imageid", "r") as file:
        id = file.readline()
    with open("imageid", "w") as file:
        file.write(str(int(id) + 1))
    # Makes the meme
    makeMeme(toptext, bottomtext, "./images/" + path, "./memes/" + id + ".jpg")
    await ctx.respond(file=discord.File("./memes/" + id + ".jpg"))

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

bot.run(token)