#FEATURES
# Generate meme, with image and text specified
# Saves all images and text
# Allows "remixed" memes by randomly generating memes from previous images and text

import os
import time
import discord
import requests
from PIL import Image
from generate import makeMeme
from dotenv import load_dotenv
from random import choice
from discord import Embed

import content
import settings

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot = discord.Bot()


@bot.slash_command(name="hello", description="hi")
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(name="meme", description="Creates a meme!")
async def meme(ctx, image, toptext="", bottomtext=""):
    try:
        img = requests.get(image).content
    except:
        await ctx.respond("Invalid Image Link")
        return
    if (not is_url_image(image)):
        await ctx.respond("Invalid Content")
        return

    # Write image to file
    temp_image = guild_file(ctx.guild.id, f"{time.time_ns()}_download.temp")
    with open(temp_image, "wb") as handler:
        handler.write(img)

    # Makes the meme
    temp_meme = guild_file(ctx.guild.id, f"{time.time_ns()}_meme.jpg")
    makeMeme(toptext, bottomtext, temp_image, temp_meme)
    await ctx.respond(file=discord.File(temp_meme))

    # Adds text to files
    content.add_toptext(ctx.guild.id, toptext)
    content.add_bottomtext(ctx.guild.id, bottomtext)
    content.add_imagelink(ctx.guild.id, image)

    # Deletes the meme
    os.remove(temp_image)
    os.remove(temp_meme)

@bot.slash_command(name="random", description="Generates a random meme!")
async def random(ctx):
    toptext = content.random_toptext(ctx.guild.id)
    bottomtext = content.random_bottomtext(ctx.guild.id)
    imagelink = content.random_imagelink(ctx.guild.id)

    try:
        imgcontent = requests.get(imagelink).content
    except:
        await ctx.respond("Exception occurred:\nTarget image link could not be accessed.")
        return

    temp_path = guild_file(ctx.guild.id, f"{time.time_ns()}_download.temp")
    temp_out = guild_file(ctx.guild.id, f"{time.time_ns()}_meme.jpg")
    with open(temp_path, "wb") as imgfile:
        imgfile.write(imgcontent)
    
    # Makes the meme
    makeMeme(toptext, bottomtext, temp_path, temp_out)
    await ctx.respond(file=discord.File(temp_out))

    # Deletes the meme
    os.remove(temp_path)
    os.remove(temp_out)

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

@bot.slash_command(name="create", description="Developer Tool: Creates the files for a new server.")
async def create(ctx):
    await on_guild_join(ctx.guild)
    await ctx.respond(":thumbsup:")

@bot.slash_command(name="savechannel", description="Sets the provided channel as the channel in which to place saved memes.")
async def setsave(ctx, channel : discord.Option((discord.TextChannel), "Target Channel")):
    await ctx.respond(f"Set {channel} as save channel")
    settings.set_save_channel(ctx.guild.id, channel.id)

@bot.slash_command(name="savereact", description="Sets the emoji used to save a meme.")
async def setsavereact(ctx):
    await ctx.respond("React to this message with the desired emoji")

    def check(reaction, user):
        return user == ctx.author

    reaction, user = await bot.wait_for('reaction_add', check=check)
    settings.set_save_emoji(ctx.guild.id, reaction.emoji)
    await ctx.channel.send(f"Reaction updated to {reaction.emoji}")
    
    

@bot.event
async def on_reaction_add(reaction : discord.Reaction, user : discord.User):
    guild = reaction.message.guild
    emoji = reaction.emoji
    if not isinstance(emoji, str):
        emoji = str(emoji)

    if settings.does_save(guild.id) and emoji == settings.get_save_emoji(guild.id) and reaction.count == 1 and reaction.message.author.id == bot.user.id:
        if reaction.message.channel.id != settings.get_save_channel(guild.id):
            for attachment in reaction.message.attachments:
                url = attachment.url
                # Post in hall of fame
                channel = bot.get_channel(int(settings.get_save_channel(guild.id)))
                embed = discord.Embed()
                embed.set_image(url=url)
                icon = user.avatar.url
                embed.set_footer(text="Saved by " + user.display_name, icon_url=icon)
                await channel.send(embed=embed)

@bot.event
async def on_guild_join(guild : discord.Guild):
    serverdir = os.path.join(".", "servers", str(guild.id))
    settingsfile = os.path.join(serverdir, "settings.txt")
    toptextfile = os.path.join(serverdir, "toptext.txt")
    bottomtextfile = os.path.join(serverdir, "bottomtext.txt")
    imagefile = os.path.join(serverdir, "images.txt")

    if not os.path.isdir(serverdir):
        os.mkdir(serverdir)
        with open(settingsfile, "w", encoding="utf8") as settings:
            settings.writelines([
                u"saveemoji=💾\n",
                "savechannel=\n",
                "parentguild=\n"
            ])
        open(toptextfile, "w")
        open(bottomtextfile, "w")
        open(imagefile, "w")

def is_url_image(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

def guild_file(guild_id : int, rel_path : str) -> str:
    return os.path.join(".", "servers", str(guild_id), rel_path)

bot.run(token)
