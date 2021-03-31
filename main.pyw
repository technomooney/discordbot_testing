# bot.py
import os
from discord.ext import commands
from discord.voice_client import VoiceClient
import discord
import dotenv
import requests
import aiohttp
import time
import pyradios
import subprocess



env_file="./.env"
dotenv.load_dotenv(env_file)
print('main program')
radio_browser = pyradios.radios.RadioBrowser()
# Variables impoterted from the .env file.
CUSTOM_PREFIXES = eval(os.getenv('CUSTOM_PREFIXES'))
ADMIN_VARS = eval(os.getenv("ADMIN_VARS"))
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv("DISCORD_GUILD")

# You'd need to have some sort of persistence here,
# possibly using the json module to save and load
# or a database

default_prefix = ['1!']


async def determine_prefix(ctx, message):
    guild = message.guild
    # Only allow custom prefixs in guild
    if guild:
        return CUSTOM_PREFIXES.get(guild.id, default_prefix)
    else:
        return default_prefix


bot = commands.Bot(command_prefix=determine_prefix)


@bot.command(name='setprefix')
@commands.guild_only()
async def set_prefix(ctx, *, prefixes=""):
    # You'd obviously need to do some error checking here
    # All I'm doing here is if prefixes is not passed then
    # set it to default
    print(ctx.guild.id)
    CUSTOM_PREFIXES[ctx.guild.id] = prefixes.split() or default_prefix
    await ctx.send("Prefixes set!")


@bot.event
async def on_ready():
    guilds = bot.guilds
    await bot.change_presence(activity=discord.Game(f"with discord.py! \n default prefix: {default_prefix[0]}"))
    print('ran presence change!')
    print(
        f'\'{bot.user}\' is connected to the following guild:\n')
    for item in guilds:
        print(item)


@bot.event
async def on_member_join(member):
    print(f'{member} has joined {discord.client.Member.guild}')


@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! \n responded in {round(bot.latency * 1000, 4)} ms')


@bot.command(name="restart", aliases=["reset","reconnect","reboot"],help="""this is a command that restarts the bot 
and saves settings changed like the close command\n 
**_this can only be used by people who have the \"admin\" role_**""")
@commands.has_any_role(*ADMIN_VARS['admin_roles'])
async def restart(ctx,reason="no reason given"):
    dotenv.set_key(env_file, "CUSTOM_PREFIXES", str(CUSTOM_PREFIXES))
    dotenv.set_key(env_file, "ADMIN_VARS", str(ADMIN_VARS))
    await bot.change_presence(status=discord.Status.offline)
    await ctx.send('Ok, be right back!')
    print(reason)
    time.sleep(1)
    print("Bot Closed")# This is optional, but it is there to tell you.
    print('restarting the bot... using a new instance ')
    await bot.close()
    time.sleep(3)
    pid = os.getpid()
    subprocess.Popen([f'kill {pid} && /home/marty/PycharmProjects/venv/bin/python /home/marty/PycharmProjects/DiscordBot/main.pyw'],shell=True)
    pid = os.getpid()
    print(pid)
    time.sleep(1)
    subprocess.Popen([f'kill {pid}'])
    exit(3)

@bot.command(name="8ball", help="send a question to be answered by the api at 8ball.delegator.com\n")
async def _8ball(ctx, *, question):
    answer = _8ball_api(question)
    await ctx.send(f"Question: {answer['question']}\n Answer: {answer['answer']}")
    await ctx.send(f'the response type was {answer["type"]}')


def _8ball_api(question):
    url = 'https://8ball.delegator.com/magic/JSON/'
    response = requests.get(url + question).json()
    return response['magic']


@bot.command(aliases=["quit"])
@commands.has_any_role(*ADMIN_VARS['admin_roles'])
async def close(ctx):
    dotenv.set_key(env_file, "CUSTOM_PREFIXES", str(CUSTOM_PREFIXES))
    dotenv.set_key(env_file, "ADMIN_VARS", str(ADMIN_VARS))
    await bot.change_presence(status=discord.Status.offline)
    await ctx.send('Ok, Bye!')
    time.sleep(1)
    await bot.close()
    print("Bot Closed")  # This is optional, but it is there to tell you.


@bot.command(name="pissybot", help=""""generate an insult using the evilinsult.com api, defaults to english
 use one of the following language code for a different lang
cn,de,el,en,es,fr,ru,sw""")
async def pissy_bot(ctx, language="en"):
    if language not in ["cn", "de", "el", "en", "es", "fr", "ru", "sw"]:
        await ctx.send(
            f" the language code `{language}` is not supported, use the help command for more info, defaulting to `en`")
        response = requests.get(f"https://evilinsult.com/generate_insult.php?lang={'en'}").text
        # print("if1 hit")
    else:
        # the mentions need <@userid> where uderid is the users numeral discord ID
        response = f"<@{ctx.author.id}>:\n" + requests.get(
            f"https://evilinsult.com/generate_insult.php?lang={language}").text
        # print("else hit")
    await ctx.send(response)


@bot.command(name='play',help="this is the command to join the current ")
async def play(ctx,time_fraim=10):
    # author = ctx.message.author
    # channel = ctx.author.voice.channel
    # vc = await channel.connect()
    # print(channel, type(channel))
    # # vc = await discord.voice_client.VoiceClient.voice_connect()
    # print()
    # print(vc)
    voicechannel = discord.utils.get(ctx.guild.channels, name=ctx.author.voice.channel.name)
    vc = await voicechannel.connect()
    async with aiohttp.ClientSession() as session:
        async with session.get('http://musicbird.leanstream.co/JCB086-MP3') as response:
            print(response.read())
    request_stream = requests.get('http://musicbird.leanstream.co/JCB086-MP3', stream=True)
    print(request_stream.content)
    print(request_stream.content.decode())
    vc.play(discord.FFmpegAudio(get_stream_data("http://musicbird.leanstream.co/JCB086-MP3")))
    await ctx.send("ran the join command")

async def get_stream_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:


@bot.command(name='leave')
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)
