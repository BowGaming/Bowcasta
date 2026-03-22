from discord.ext import commands
from discord import Embed, Forbidden
from discord import TextChannel, Thread
import time
import re

class CheckpermsCog(commands.Cog) :
    def __init__(self, bot) :
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
      
        if message.author.bot :
                return
          
        if "checkperms" not in message.content.lower():
                return
          
        guild = message.guild
        everyone = guild.default_role  # @everyone
    
        output = ""

        for channel in guild.channels:
            perms = channel.permissions_for(everyone)

            output += (
                f"**{channel.name}**\n"
                f"View: {perms.view_channel}\n"
                f"Send: {getattr(perms, 'send_messages', None)}\n"
                f"Connect: {getattr(perms, 'connect', None)}\n"
                f"----------------------\n"
            )

        # Discord has a 2000 character limit per message
        for i in range(0, len(output), 2000):
            await message.channel.send(output[i:i+2000])

async def setup(bot: commands.Bot) :
    """Standard setup function for discord.py cogs."""
    await bot.add_cog(CheckpermsCog(bot))
