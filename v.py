import os
import secrets

import discord
from discord.commands import ApplicationContext, Option
import logging


logging.basicConfig(level=logging.DEBUG)



# bot = discord.Bot(debug_guilds=[...])
bot = discord.Bot()
bot.connections = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to {bot.guilds} !')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="CaveMC.NET"))

@bot.command()
async def moin(
    ctx: ApplicationContext,
    user: Option(discord.User,"benutzer"),
):
    """
    tset!
    """
    print("moin was called!")
    embed=discord.Embed(description=f" {ctx.author.mention} grüßt {user.mention} \n [für die Regeln klicken!](https://discordapp.com/channels/844208848121495572/926182897453510656/926238579938701322)", color=0x208edd)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_author(name="CaveMC Team", icon_url=bot.user.avatar.url)
    await ctx.respond(embed=embed)
    # await ctx.respond(bot.user.avatar.url)


@bot.command()
async def hallo(
    ctx: ApplicationContext,
    encoding: Option(
        str,
        choices=[
            "mp3",
            "wav",
            "pcm",
            "ogg",
            "mka",
            "mkv",
            "mp4",
            "m4a",
        ],
    ),
):
    pass

# @bot.command()
# async def help(
#     ctx: ApplicationContext
# ):
#     """
#     Bitte helfen Sie mir, ich bin in Gefahr!
#     """
#     pass

@bot.command()
async def start(
    ctx: ApplicationContext,
    encoding: Option(
        str,
        choices=[
            "mp3",
            "wav",
            "pcm",
            "ogg",
            "mka",
            "mkv",
            "mp4",
            "m4a",
        ],
    ),
):
    """
    Nimmt den Channel auf, in dem du drinnen bist!
    """
    voice = ctx.author.voice

    if not voice:

        embed=discord.Embed(description=f"Du bist in keinem Voice-Channel!" , color=0x208edd)
        # embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_author(name="CaveMC Team", icon_url=bot.user.avatar.url)
        return await ctx.respond(embed=embed)

    vc = await voice.channel.connect()
    bot.connections.update({ctx.guild.id: vc})

    if encoding == "mp3":
        sink = discord.sinks.MP3Sink()
    elif encoding == "wav":
        sink = discord.sinks.WaveSink()
    elif encoding == "pcm":
        sink = discord.sinks.PCMSink()
    elif encoding == "ogg":
        sink = discord.sinks.OGGSink()
    elif encoding == "mka":
        sink = discord.sinks.MKASink()
    elif encoding == "mkv":
        sink = discord.sinks.MKVSink()
    elif encoding == "mp4":
        sink = discord.sinks.MP4Sink()
    elif encoding == "m4a":
        sink = discord.sinks.M4ASink()
    else:
        return await ctx.respond("Invalid encoding.")

    vc.start_recording(
        sink,
        finished_callback,
        ctx.channel,
    )

    await ctx.respond("Die Aufnahme startet!")


async def finished_callback(sink, channel: discord.TextChannel, *args):
    recorded_users = [f"<@{user_id}>" for user_id, audio in sink.audio_data.items()]
    await sink.vc.disconnect()
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    await channel.send(f"Fertig! aufgenommene Benutzer: {', '.join(recorded_users)}.", files=files)



@bot.command()
async def stop(ctx):
    """
    Stoppt und speichert die Aufnahme.
    """
    if ctx.guild.id in bot.connections:
        vc = bot.connections[ctx.guild.id]
        vc.stop_recording()
        del bot.connections[ctx.guild.id]
        await ctx.delete()
    else:
        await ctx.respond("Not recording in this guild.")


bot.run(secrets.discordToken)