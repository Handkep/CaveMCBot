import os
from discord.ext import commands
import discord
# from numpy import array
from discord.ui import Button, View
import secrets
import random
import logging
import yaml


logging.basicConfig(level=logging.INFO)


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".", intents=intents)

roleIdForNotifying = 953940038230634566


todos = [["option1","✅"],["option2","🟥"],["optssion3","✅"],["option4","🟥"]]
print(todos)
with open('todos.yaml',"r") as f:
    todos = yaml.safe_load(f)
print(todos)

# with open('todos.yaml', 'w') as f:
#     yaml.dump(todos, f)


# todos
def buildTodoString(todo: array):
    buf = ""
    for i in enumerate(todo):
        print(i)
        buf += "`" + str(i[0]+1) + "." + i[1][1] + " " + i[1][0] + "` \n"
        
    print(buf)
    return buf
def removeTodoOption(todo: list, option):
    print(option)
    for i in enumerate(todo):
        for j in option:
            if j == i[1][0]:
                print("del "+str(i))
                del todo[i[0]]
    with open('todos.yaml', 'w') as f:
        yaml.dump(todos, f)
def addTodoOption(todo:list,option:str):
    buf = []
    buf.append(option)
    buf.append("🟥")
    todo.append(buf)
    with open('todos.yaml', 'w') as f:
        yaml.dump(todos, f)

    return buf
def checkTodoOption(todo:list,option:str):
    for i in enumerate(todo):
        for j in option:
            if j == i[1][0]:
                todo[i[0]][1] = "✅"
    with open('todos.yaml', 'w') as f:
        yaml.dump(todos, f)


def getTodoEmbed():
    with open('todos.yaml',"r") as f:
        todos = yaml.safe_load(f)
    return discord.Embed(title="TODO", description=buildTodoString(todos), color=0x208edd)
client = discord.Client()
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to {bot.guilds} !')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="CaveMC.NET"))
    # embed=discord.Embed(title="ONLINE", description=buildTodoString(todos), color=0x208edd)
    # embed.set_footer(text="der CaveMC Bot")
    buttonCheckOption = discord.ui.Button(label="Aufgabe abhaken✔️",style=discord.ButtonStyle.green)
    buttonAddOption = discord.ui.Button(label="Aufgabe hinzufügen")
    buttonDeleteOption = discord.ui.Button(label="Aufgabe löschen",style=discord.ButtonStyle.red)
    buttonBack = discord.ui.Button(label="Zurück")
    
    selectCheckOption= discord.ui.Select()
    selectAddOption= discord.ui.Select()
    selectDeleteOption= discord.ui.Select()

    for i in todos:
        selectCheckOption.add_option(label=i[0])
        selectAddOption.add_option(label=i[0])
        selectDeleteOption.add_option(label=i[0])

    inputAddOption = discord.ui.InputText(label="Aufgabe:",style=discord.InputTextStyle.short)

    addModal = discord.ui.Modal(title="Aufgabe zur ToDo-Liste hinzufügen")
    addModal.add_item(inputAddOption)
    checkView = discord.ui.View(selectCheckOption,buttonBack)
    deleteView = discord.ui.View(selectDeleteOption,buttonBack)
    defaultView = discord.ui.View(buttonCheckOption,buttonAddOption,buttonDeleteOption)

    async def buttonCheckOption_callback(interaction):
        await interaction.response.edit_message(embed=getTodoEmbed(),view=checkView)
        return
    buttonCheckOption.callback = buttonCheckOption_callback

    async def buttonAddOption_callback(interaction):
        await interaction.response.send_modal(addModal)
        return
    buttonAddOption.callback = buttonAddOption_callback

    async def buttonDeleteOption_callback(interaction):
        async for message in interaction.channel.history(limit=200):
            if message.author == bot.user:
                await message.delete()
    buttonDeleteOption.callback = buttonDeleteOption_callback

    async def buttonBack_callback(interaction):
        await interaction.response.edit_message(embed=getTodoEmbed(),view=defaultView)
        return
    buttonBack.callback = buttonBack_callback

    async def selectCheckOption_callback(interaction):
        # await interaction.response.edit_message(embed=getTodoEmbed(),view=defaultView)
        print(interaction.data)
        checkTodoOption(todos,interaction.data["values"])
        await interaction.response.edit_message(embed=getTodoEmbed(),view=defaultView)

        return
    selectCheckOption.callback = selectCheckOption_callback

    async def selectDeleteOption_callback(interaction):
        # await interaction.response.edit_message(embed=getTodoEmbed(),view=defaultView)
        print(interaction.data)
        removeTodoOption(todos,interaction.data["values"])


        await interaction.response.edit_message(embed=getTodoEmbed(),view=defaultView)

        return
    selectDeleteOption.callback = selectDeleteOption_callback





    async def addModal_callback(interaction):
        print(interaction.data["components"][0]["components"][0]["value"])
        option =addTodoOption(todos, interaction.data["components"][0]["components"][0]["value"])
        
        selectCheckOption.add_option(label=option[0])
        selectAddOption.add_option(label=option[0])
        selectDeleteOption.add_option(label=option[0])

        # await interaction.delete_original_message()
        print(interaction.message)
        await interaction.message.edit(embeds=[getTodoEmbed()],view=defaultView)
        await interaction.response.send_message()
        
        # await z = interaction.original_message()
        # await interaction.edit_original_message(embeds=[getTodoEmbed()],view=defaultView)
        return 
    addModal.callback = addModal_callback

    for i in bot.guilds:
        for j in i.roles:   
            if j.id == roleIdForNotifying:
                print(j.members)
                for k in j.members:
                    await k.send(embed=getTodoEmbed(),view=defaultView)
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
    print(message.author.mention)
    with open("embeded_messages/test.txt") as f:
        print(f)
    # await message.channel.send(embed=embed)
    # for i in message.author.roles:
    #     if i.id == roleIdForNotifying:
    #         print(i.members)
    #         for j in i.members:
    #             await j.send(embed=embed)
    # await message.author.send(embed=embed)
    # await message.author.send("aögijagöijaegegö")

@bot.command()
async def test(ctx):
    print("yayy")
bot.run(secrets.discordToken)