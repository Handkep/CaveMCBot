import os
from discord.ext import commands
import discord
from numpy import array
from discord.ui import Button, View
import secrets
import random
import logging
import yaml

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()

bot = commands.Bot(intents=intents)

client = discord.Client()
@bot.event
async def on_ready():
    pass


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"{message.author} schrieb {message.content}")
    # print(f"{message.author} hat {message.author.roles}")
    print(f"{message.author} hat {message.author.mention}")
    embed=discord.Embed(title="ONLINE", description="Moin, bin nun Online :) Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut consequat semper viverra nam libero. Lectus magna fringilla urna porttitor rhoncus dolor purus. Sodales ut etiam sit amet nisl. Venenatis a condimentum vitae sapien. Orci phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Laoreet sit amet cursus sit amet dictum sit amet. Metus vulputate eu scelerisque felis imperdiet proin fermentum. Ac turpis egestas maecenas pharetra convallis. Dui sapien eget mi proin. Convallis aenean et tortor at risus. Nisi est sit amet facilisis magna etiam. Imperdiet proin fermentum leo vel. Scelerisque varius morbi enim nunc faucibus a. Est placerat in egestas erat imperdiet sed euismod. Sapien et ligula ullamcorper malesuada proin libero nunc consequat interdum. Tincidunt dui ut ornare lectus sit. Augue interdum velit euismod in pellentesque massa placerat duis ultricies. Eleifend donec pretium vulputate sapien nec sagittis aliquam malesuada bibendum.", color=0x208edd)
    embed=discord.Embed(description=f"{message.author.mention}\n hat {message.content} geschrieben", color=0x208edd)

@bot.slash_command(name="ac_basic_example")
async def test(ctx):
    print("hallo")
    await ctx.respond("Not recording in this guild.")
bot.run(secrets.discordToken)