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
from discord import Embed

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
server = int(os.getenv('HALO'))
fameID = int(os.getenv('HOF'))
save = int(os.getenv('SAVE'))

bot = discord.Bot()


@bot.slash_command(name="hello", description="hi")
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(name="meme", description="Creates a meme!")
async def hello(ctx, image, toptext="", bottomtext=""):
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
    # Deletes the meme
    os.remove("./memes/" + id + ".jpg")

@bot.slash_command(name="random", description="Generates a random meme!")
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
    # Deletes the meme
    os.remove("./memes/" + id + ".jpg")

@bot.slash_command(name="stats", description="Meme Stats :)")
async def stats(ctx):
   with open("imageid", "r") as file:
        id = file.readline()
   unique = len(os.listdir("./images"))
   embed = Embed()
   embed.title = "Stats"
   embed.add_field(name="Original memes", value=str(unique))
   embed.add_field(name="Total memes", value=str(id)) 
   embed.color = (15648364)
   await ctx.respond(embed=embed)

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji.id == save and reaction.count == 1 and reaction.message.author.id == bot.user.id:
        if reaction.message.channel.id != fameID:
            for attachment in reaction.message.attachments:
                url = attachment.url
                # Post in hall of fame
                channel = bot.get_channel(fameID)
                embed = discord.Embed()
                embed.set_image(url=url)
                icon = user.avatar.url
                embed.set_footer(text="Saved by " + user.display_name, icon_url=icon)
                await channel.send(embed=embed)
                

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

bot.run(token)
