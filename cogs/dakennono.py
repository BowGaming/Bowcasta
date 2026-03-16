from discord.ext import commands
from discord import Embed, Forbidden
from discord import TextChannel, Thread
import re

class AkihiroCog(commands.Cog) :
    def __init__(self, bot) :
        self.bot = bot
      
        # Message
        self.akihiro_message = Embed(
            description=(
                "Please do not use the name 'Daken' as this is actually a slur.\n"
                "Instead, use one of these alternatives: Akihiro, Dark Wolverine, Hellverine, Fang."
            ),
        )

        # Ignored channels due to title reasons
        self.ignored_channels = {1424723487955619840,689387320142463035,1483188598688976978}
        self.ignored_forums = {1432707413181599775}


    @commands.Cog.listener()
    async def on_message(self, message) :
        """Checks messages in the review channel and enforces format."""
        if message.author.bot :
            return

    # Ignore normal channels
    if isinstance(message.channel, TextChannel):
        if message.channel.id in self.ignored_channels:
            return
    # Ignore threads inside forums
    if isinstance(message.channel, Thread):
        if message.channel.parent and message.channel.parent.id in self.ignored_forums:
            return
            
        if "daken" in message.content.lower():
          await message.reply(embed=self.akihiro_message)

async def setup(bot: commands.Bot) :
    """Standard setup function for discord.py cogs."""
    await bot.add_cog(AkihiroCog(bot))
