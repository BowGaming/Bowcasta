from discord.ext import commands
from discord import Embed, Forbidden
from discord import TextChannel, Thread
import time
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

        # Manual overrides for blocking/allowing channels
        self.blocked_channels = {}
        self.allowed_channels = {689387320142463035}
        self.blocked_forums = {}
        self.allowed_forums = {}

        # Cooldown duration in seconds
        self.cooldown_seconds = 60
        self.last_executed = {}

    def is_blocked_channel(self, channel):
        guild = channel.guild
    
        # Manual allowlist
        if channel.id in self.allowed_channels:
            return False
        if isinstance(channel, Thread) and channel.parent and channel.parent.id in self.allowed_forums:
            return False
    
        # Manual blocklist
        if channel.id in self.blocked_channels:
            return True
        if isinstance(channel, Thread) and channel.parent and channel.parent.id in self.blocked_forums:
            return True
    
        # @everyone permission check
        everyone_role = guild.default_role
        
        if isinstance(channel, Thread):
            parent = channel.parent
            if parent:
                overwrite = parent.overwrites_for(everyone_role)
                if overwrite.send_messages is not False:
                    return True
        else:
            overwrite = channel.overwrites_for(everyone_role)
            if overwrite.send_messages is not False:
                return True
    
        return False
    
    @commands.Cog.listener()
    async def on_message(self, message) :
        """Checks messages in the review channel and enforces format."""
        if message.author.bot :
            return

        # Ignore normal channels
        if not self.is_blocked_channel(message.channel):
            return
            
        if "daken" not in message.content.lower():
            return

        channel_id = message.channel.id
    
        # cooldown check
        now = time.time()
        last_time = self.last_executed.get(channel_id, 0)
        if now - last_time < self.cooldown_seconds:
            return  # still in cooldown
    
        await message.reply(embed=self.akihiro_message)
    
        # update last time used
        self.last_executed[channel_id] = now
        
async def setup(bot: commands.Bot) :
    """Standard setup function for discord.py cogs."""
    await bot.add_cog(AkihiroCog(bot))
