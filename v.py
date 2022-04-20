from dis import disco
import os
import secrets
import yaml
import discord
from discord.commands import ApplicationContext, Option, permissions
# from discord.ext.commands import UserConverter
import logging
import sys

logger = logging.getLogger('application')
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s [%(levelname)s] %(message)s",
    format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


# bot = discord.Bot(debug_guilds=[...])

with open("config.yaml","r") as f:
    config = yaml.safe_load(f)

bot = discord.Bot()
bot.connections = {}


async def no_permission(ctx:discord.ApplicationContext):
    await ctx.respond("du darfst das nicht")

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to {bot.guilds}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="CaveMC.NET"))

@bot.command()
async def moin(
    ctx: ApplicationContext,
    user: Option(discord.User,"benutzer"),
):
    """
    tset!
    """
    logger.info(f'{ctx.author.display_name} has used /moin')
    await no_permission(ctx)
    return
    embed=discord.Embed(description=f" {ctx.author.mention} grüßt {user.mention} \n [für die Regeln klicken!](https://discordapp.com/channels/844208848121495572/926182897453510656/926238579938701322)", color=0x208edd)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_author(name="CaveMC Team", icon_url=bot.user.avatar.url)
    await ctx.respond(embed=embed)
    # await ctx.respond(bot.user.avatar.url)

@bot.command()
async def ankündigung(
    ctx: ApplicationContext,
    text: Option(str,"Inhalt der Ankündigung"),
    kanal: Option(str,choices=[i for i in config["announcements"]]),
    ping: Option(discord.User,"Ping")
):
    """
    Sendet eine Ankündigung in den Ankündigungskanal
    """
    logger.info(f'{ctx.author.display_name} has used /ankündigung: text={text}, Channel={kanal}')
    kanalid = config["announcements"][kanal]
    await ctx.respond(f"Ankündigung wurde in {ctx.bot.get_channel(int(kanalid)).mention} gesendet!")
    # print(ctx.guild.)
    # msg = "****\n" + text + "\n" + ctx.author.mention # + "\n @everyone"
    embed=discord.Embed(description=text, color=0x208edd)
    embed.title="Ankündigung:"
    # embed.description = ctx.author.mention
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_author(name="CaveMC Team", icon_url=bot.user.avatar.url)
    # embed.set_footer(text=f"{ctx.author.mention} Copyright CaveMC © 2021-2022 <@239335585183956992> ")
    embed.set_footer(text=f"Ankündigu von {ctx.author.display_name}\nCopyright CaveMC © 2021-2022",icon_url=ctx.author.avatar.url)
    # await ctx.bot.get_channel(int(config["announcements"][kanal])).send("Ankündigung @everyone",embed=embed)
    await ctx.bot.get_channel(int(config["announcements"][kanal])).send(f"Ankündigung {ping.mention}",embed=embed)
    return


@bot.command(default_permission=False)
@permissions.has_role(953940038230634566)#, guild_id=844208848121495572) 
async def hallo(
    ctx: ApplicationContext
):
    with open('hallo.txt',"r",encoding="utf-8") as f:
        txt = f.read()
        print(txt)

        embed=discord.Embed(description=txt, color=0x208edd)
        # embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_author(name="CaveMC Team", icon_url=bot.user.avatar.url)
        embed.set_footer(text="Copyright CaveMC © 2021-2022")
        await ctx.respond(embed=embed)
    
@bot.command()
async def help(
    ctx: ApplicationContext
):
    """
    Bitte helfen Sie mir, ich bin in Gefahr!
    """
    with open('help.txt',"r",encoding="utf-8") as f:
        txt = f.read()
        embed=discord.Embed(description=txt, color=0x20dd9f)
        embed.set_thumbnail(url="https://public.am.files.1drv.com/y4m1WE2nIfYlzvnmvxnywpi2IXB9YYEj5U3ErIGYcnX7y1HdfLibQxeOwcqg_RGwbrlOvZj0aOhUfCMgxAGNG1CI11vfg9A49mTa3T4V-Je0tC8ezcTYs8NDAWHzD9KKJE3rwMWC7ndajp8-B_nDGOEe5r4iWt7NetoyvIulQONJSQi1HJGanhAlUaSRuu7v3G3izb_qDGVs-3PBjlhiw_sFOg0Qa7xMXFCZ06LG3Lgdm8")
        embed.set_author(name="CaveMC Team", icon_url=bot.user.avatar.url)
        embed.set_footer(text="Copyright CaveMC © 2021-2022")
        await ctx.respond("Du hast Hilfe angefordert, hier kommt sie :)",embed=embed)

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
    files = []
    for user_id, audio in sink.audio_data.items():
        user = await bot.fetch_user(user_id)
        files.append(discord.File(audio.file, f"{user}.{sink.encoding}"))
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