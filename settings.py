# Allows access to a guild's settings
import os

def get_save_emoji(guild_id : int) -> str:
    """Returns the emoji id of the emoji set as this server's save emoji."""
    with open(guild_file(guild_id, "settings.txt"), "r", encoding="utf8") as f:
        lines = f.readlines()
        maybe_channel = list(filter(lambda l : l.startswith("saveemoji="), lines))
        if len(maybe_channel) != 1:
            print(f"{guild_id} is missing a save emoji")
            return ""
        return maybe_channel[0].split("=")[1].strip()
    
def set_save_emoji(guild_id : int, react):
    with open(guild_file(guild_id, "settings.txt"), "r", encoding="utf8") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if line.startswith("saveemoji="):
                lines[index] = f"saveemoji={react}\n"

    with open(guild_file(guild_id, "settings.txt"), "w", encoding="utf8") as f:
        f.writelines(lines)

def set_save_channel(guild_id : int, channel_id : str):
    with open(guild_file(guild_id, "settings.txt"), "r", encoding="utf8") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if line.startswith("savechannel="):
                lines[index] = f"savechannel={channel_id}\n"

    with open(guild_file(guild_id, "settings.txt"), "w", encoding="utf8") as f:
        f.writelines(lines)

def get_save_channel(guild_id : int):
    """Returns the channel ID of the channel saved images are sent to."""
    with open(guild_file(guild_id, "settings.txt"), "r", encoding="utf8") as f:
        lines = f.readlines()
        maybe_channel = list(filter(lambda l : l.startswith("savechannel="), lines))
        if len(maybe_channel) != 1:
            print(f"{guild_id} is missing a save channel")
            return ""
        return maybe_channel[0].split("=")[1].strip()

def does_save(guild_id : int) -> bool:
    """Returns True if the guild has a saving channel set, False otherwise."""
    with open(guild_file(guild_id, "settings.txt"), "r", encoding="utf8") as f:
        lines = f.readlines()
        maybe_channel = list(filter(lambda l : l.startswith("savechannel="), lines))
        if len(maybe_channel) != 1:
            print(f"{guild_id} is missing a save channel")
            return ""
        return len(maybe_channel[0].split("=")[1]) > 0

def guild_file(guild_id : int, rel_path : str) -> str:
    return os.path.join(".", "servers", str(guild_id), rel_path)