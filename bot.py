import os
from pyexpat.errors import messages
from discord.ext import commands
import discord
# from dotenv import loa
import secrets
import random



intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".", intents=intents)

roleIdForNotifying = 953940038230634566



client = discord.Client()
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to {bot.guilds} !')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="CaveMC.NET"))
    embed=discord.Embed(title="ONLINE", description="Moin, bin nun Online :)", color=0x208edd)
    embed=discord.Embed(title="ONLINE", description="Moin, bin nun Online :) Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut consequat semper viverra nam libero. Lectus magna fringilla urna porttitor rhoncus dolor purus. Sodales ut etiam sit amet nisl. Venenatis a condimentum vitae sapien. Orci phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Laoreet sit amet cursus sit amet dictum sit amet. Metus vulputate eu scelerisque felis imperdiet proin fermentum. Ac turpis egestas maecenas pharetra convallis. Dui sapien eget mi proin. Convallis aenean et tortor at risus. Nisi est sit amet facilisis magna etiam. Imperdiet proin fermentum leo vel. Scelerisque varius morbi enim nunc faucibus a. Est placerat in egestas erat imperdiet sed euismod. Sapien et ligula ullamcorper malesuada proin libero nunc consequat interdum. Tincidunt dui ut ornare lectus sit. Augue interdum velit euismod in pellentesque massa placerat duis ultricies. Eleifend donec pretium vulputate sapien nec sagittis aliquam malesuada bibendum.", color=0x208edd)
    embed.set_footer(text="der CaveMC Bot")
    for i in bot.guilds:
        for j in i.roles:   
            if j.id == roleIdForNotifying:
                print(j.members)
                for k in j.members:
                    await k.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"{message.author} schrieb {message.content}")
    # print(f"{message.author} hat {message.author.roles}")
    print(f"{message.author} hat {message.author.mention}")
    embed=discord.Embed(title="ONLINE", description="Moin, bin nun Online :) Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut consequat semper viverra nam libero. Lectus magna fringilla urna porttitor rhoncus dolor purus. Sodales ut etiam sit amet nisl. Venenatis a condimentum vitae sapien. Orci phasellus egestas tellus rutrum tellus pellentesque eu tincidunt tortor. Laoreet sit amet cursus sit amet dictum sit amet. Metus vulputate eu scelerisque felis imperdiet proin fermentum. Ac turpis egestas maecenas pharetra convallis. Dui sapien eget mi proin. Convallis aenean et tortor at risus. Nisi est sit amet facilisis magna etiam. Imperdiet proin fermentum leo vel. Scelerisque varius morbi enim nunc faucibus a. Est placerat in egestas erat imperdiet sed euismod. Sapien et ligula ullamcorper malesuada proin libero nunc consequat interdum. Tincidunt dui ut ornare lectus sit. Augue interdum velit euismod in pellentesque massa placerat duis ultricies. Eleifend donec pretium vulputate sapien nec sagittis aliquam malesuada bibendum.", color=0x208edd)
    embed=discord.Embed(description=f"{message.author.mention}\n hat {message.content} geschrieben", color=0x208edd)
    print(message.author.mention)
    with open("embeded_messages/test.txt") as f:
        print(f)
    await message.channel.send(embed=embed)
    # for i in message.author.roles:
    #     if i.id == roleIdForNotifying:
    #         print(i.members)
    #         for j in i.members:
    #             await j.send(embed=embed)
    # await message.author.send(embed=embed)
    # await message.author.send("aögijagöijaegegö")

@bot.command()
async def test(ctx):
    pass




bot.run(secrets.discordToken)