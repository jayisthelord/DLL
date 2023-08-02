import discord
from discord.ext import commands
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixdb = db.reference('prefixes/')
    
    @commands.command()
    @commands.is_owner()
    async def prefixes(self, ctx):
        await ctx.send(f"```json\n{json.dumps(self.prefixdb.get(), indent=2)}\n```")

async def setup(bot):
    await bot.add_cog(Developer(bot))