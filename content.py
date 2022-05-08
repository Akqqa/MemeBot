# Retrieves content
from random import choice
import os

def guild_file(guild_id : int, rel_path : str) -> str:
    return os.path.join(".", "servers", str(guild_id), rel_path)

def add_toptext(guild_id : int, content : str):
    """Adds a toptext to the given guild."""
    with open(guild_file(guild_id, "toptext.txt"), "a") as file:
        file.write(content + "\n")

def add_bottomtext(guild_id : int, content : str):
    """Adds a bottomtext to the given guild."""
    with open(guild_file(guild_id, "bottomtext.txt"), "a") as file:
        file.write(content + "\n")

def add_imagelink(guild_id : int, content : str):
    """Adds a image link to the given guild."""
    with open(guild_file(guild_id, "images.txt"), "a") as file:
        file.write(content + "\n")

def random_toptext(guild_id : int) -> str:
    """Returns a random toptext from the given guild."""
    with open(guild_file(guild_id, "toptext.txt"), "r") as file:
        lines = file.readlines()
        return choice(lines)

def random_bottomtext(guild_id : int) -> str:
    """Return a random bottomtext from the given guild."""
    with open(guild_file(guild_id, "bottomtext.txt"), "r") as file:
        lines = file.readlines()
        return choice(lines)

def random_imagelink(guild_id : int) -> str:
    """Returns a random image link from the given guild."""
    with open(guild_file(guild_id, "images.txt"), "r") as file:
        lines = file.readlines()
        return choice(lines)

