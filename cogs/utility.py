import discord
from discord.ext import commands
import os
from firebase_admin import storage
from firebase_admin import db
import requests

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild == None:
            return
        if message.author.bot:
            return
        if not message.content:
            return
        self.sniped[message.channel.id] = message

    @commands.command(name="snipe")
    async def snipe(self, ctx):
        message = self.sniped.get(ctx.channel.id)
        if message == None:
            return await ctx.send(embed=discord.Embed(
                title="Snipe",
                description="There are no recently deleted messages",
                color=0x2f3136))
        embed = discord.Embed(title="Sniped Message sent by %s" %
                              (message.author),
                              description=message.content,
                              color=0x2f3136,
                              timestamp=message.created_at)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3600)
    async def upload(self, ctx, file: discord.Attachment):
        # print(file.url)
        url = file.url
        r = requests.get(url, allow_redirects=True)

        open(f'./tmp/{file.filename}', 'wb').write(r.content)
        fileName = f"./tmp/{file.filename}"
        bucket = storage.bucket()
        blob = bucket.blob(f"Uploads/{ctx.author.name}_{file.filename}")
        blob.upload_from_filename(fileName)
        blob.make_public()

        embed = discord.Embed(title="Hooray!",
                            description=f"Your file link is, {blob.public_url}",
                            color=0xDF3A55)
        await ctx.send(embed=embed)
        
        user = ctx.author
        embeduser = discord.Embed(title="File Uploaded!",
                                  description="",
                                  color=0xDF3A55)
        embeduser.add_field(name="Filename",
                            value=ctx.author.name+"_"+file.filename,
                            inline=True)
        embeduser.add_field(name="URL",
                            value=blob.public_url,
                            inline=True)
        embeduser.add_field(name="File Type",
                            value=blob.content_type,
                            inline=False)
        embeduser.set_footer(text=f"Uploaded from server {ctx.guild.name}")
        await user.send(embed=embeduser)
        # print("your file url", blob.public_url)
        os.remove(f'./tmp/{file.filename}')

async def setup(bot):
    await bot.add_cog(Utility(bot))