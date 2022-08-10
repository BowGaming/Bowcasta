import discord
from discord.ext import commands
from discord.ext.commands import *
from typing import *

import datetime

class OwnerCog(commands.Cog, name = "Owner"):
	"""Owner commands"""

	def __init__(self, bot):
		self.bot = bot

	async def cog_check(self, ctx):
		return await self.bot.is_owner(ctx.author)

	@commands.command()
	async def shutdown(self, ctx):
		"""Shuts down the bot"""
		try: await ctx.reply("Shutting down...")
		except discord.Forbidden: await ctx.author.send("Shutting down...")

		print(f"Shutting down...")
		print(discord.utils.utcnow().strftime("%d/%m/%Y %I:%M:%S:%f"))

		await self.bot.close()


	@commands.group(name="cogs", aliases=["cog"])
	async def cogs(self, ctx):
		"""Cog management"""
		return

	@cogs.command(name = 'load')
	async def loadcog(self, ctx, *, cog: str):
		"""Loads cog. Remember to use dot path. e.g: cogs.owner"""
		try: await self.bot.load_extension(cog)
		except Exception as e: return await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
		else: await ctx.send(f'Successfully loaded `{cog}`.')
		print('---')
		print(f'{cog} was loaded.')
		print('---')

	@cogs.command(name = 'unload')
	async def unloadcog(self, ctx, *, cog: str):
		"""Unloads cog. Remember to use dot path. e.g: cogs.owner"""
		try: 
			await self.canceltasks(cog)
			await self.bot.unload_extension(cog)
		except Exception as e: return await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
		else: await ctx.send(f'Successfully unloaded `{cog}`.')
		print('---')
		print(f'{cog} was unloaded.')
		print('---')

	@cogs.command(name = 'reload')
	async def reloadcog(self, ctx, *, cog: str):
		"""Reloads cog. Remember to use dot path. e.g: cogs.owner"""
		try: 
			await self.canceltasks(cog)
			await self.bot.reload_extension(cog)
		except Exception as e: return await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
		else: await ctx.send(f'Successfully reloaded `{cog}`.')
		self.bot.recentcog = cog
		print('---')
		print(f'{cog} was reloaded.')
		print('---')

	@commands.command(hidden = True, aliases = ['crr'])
	async def cogrecentreload(self, ctx):
		"""Reloads most recent reloaded cog"""
		if not self.bot.recentcog: return await ctx.send("You haven't recently reloaded any cogs.")

		return await ctx.invoke(self.reloadcog, cog = self.bot.recentcog)

		try:
			await self.canceltasks(self.bot.recentcog)
			await self.bot.reload_extension(self.bot.recentcog)
		except Exception as e: await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
		else: await ctx.send(f'Successfully reloaded `{self.bot.recentcog}`.')
		print('---')
		print(f'{self.bot.recentcog} was reloaded.')
		print('---')


	@commands.command()
	@commands.guild_only()
	async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
		"""
		Works like:
		!sync -> global sync
		!sync ~ -> sync current guild
		!sync * -> copies all global app commands to current guild and syncs
		!sync ^ -> clears all commands from the current guild target and syncs (removes guild commands)
		!sync id_1 id_2 -> syncs guilds with id 1 and 2
		"""
		if not guilds:
			if spec == "~":
				synced = await ctx.bot.tree.sync(guild=ctx.guild)
			elif spec == "*":
				ctx.bot.tree.copy_global_to(guild=ctx.guild)
				synced = await ctx.bot.tree.sync(guild=ctx.guild)
			elif spec == "^":
				ctx.bot.tree.clear_commands(guild=ctx.guild)
				await ctx.bot.tree.sync(guild=ctx.guild)
				synced = []
			else:
				synced = await ctx.bot.tree.sync()

			await ctx.send(
				f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
			)
			return

		ret = 0
		for guild in guilds:
			try:
				await ctx.bot.tree.sync(guild=guild)
			except discord.HTTPException:
				pass
			else:
				ret += 1

		await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


	async def canceltasks(self, name):
		async def canceller(self, x):
			try: await self.bot.tasks[x].cancel()
			except Exception: pass

		if name == 'cogs.comics':
			await canceller(self, 'releases')

		if name == 'cogs.polls':
			pass

		if name == 'funcs.postgresql':
			try: await self.bot.db.close()
			except Exception: print("Couldn't close PostgreSQL connection")

async def setup(bot):
	await bot.add_cog(OwnerCog(bot))