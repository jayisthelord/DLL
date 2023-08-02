import discord
from discord.ext import commands
import random
import requests
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import wget

cred = credentials.Certificate("./Firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dll-1fe73-default-rtdb.firebaseio.com',
    'storageBucket': 'dll-1fe73.appspot.com'
})

configs = db.reference('config/')
token = configs.child('token')

def get_prefix(bot, message):
    ref = db.reference(f'prefixes/{message.guild.id}')
    prefix = ref.get()
    return prefix if prefix else '> '

bot = commands.Bot(command_prefix=get_prefix,
                   intents=discord.Intents().all()) 

@bot.event
async def on_message(message): 
    if message.author.id == bot.user.id:
        return
    
    ref = db.reference(f'prefixes/{message.guild.id}')
    prefix = ref.get()
    if message.content in [f'<!@{bot.user.id}>', f'<@{bot.user.id}>']:
        await message.reply(f'Hey, {message.author.name} if youre wondering how to use me use `{prefix}help`')

    await bot.process_commands(message)

@bot.event
async def on_guild_join(guild):
    default_prefix = '!'
    ref = db.reference(f'prefixes/{guild.id}')
    ref.set(default_prefix)

@bot.event
async def on_guild_remove(guild):
    ref = db.reference(f'prefixes/{guild.id}')
    ref.delete()

@bot.event
async def on_ready():
        await bot.load_extension("jishaku")
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
                                                            name=f'{len(bot.users)} Users!'))

@bot.command(aliases=['bi'])
async def botinfo(ctx):
    colors = [0xffffff, 0x0c0c0c]
    embed = discord.Embed(title="DLL",
                          description="",
                          color=random.choice(colors))
    embed.add_field(name="Stats",
                    value=f"Users `{len(bot.users)}`\nLatency `{round (bot.latency * 1000)}`\nGuilds `{len(bot.guilds)}`")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, *, new_prefix):
    server_id = str(ctx.guild.id)
    ref = db.reference(f'prefixes/{server_id}')
    if new_prefix == "reset":
        ref.set("> ")
        await ctx.send(f"The server prefix has been reseted to `> `!")
    else:
        ref.set(new_prefix)
        await ctx.send(f"The server prefix has been updated to `{new_prefix}`!")

bot.run(token.get())