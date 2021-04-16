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
import logging

#
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

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


@bot.command(name='play_url',help="this is the command to join the current ")
async def play_url(ctx,url="http://musicbird.leanstream.co/JCB086-MP3"):
    voicechannel = discord.utils.get(ctx.guild.channels, name=ctx.author.voice.channel.name)
    vc = await voicechannel.connect()
    vc.play(discord.FFmpegPCMAudio(url))
    await ctx.send("ran the join command")

@bot.command(name='radiofuzzsearch',
            help="this is the fuzzy (search like google) search for a radio station and get a url for a station to pass "
                 "to the getradiourl command, just type the command in and you can get more help")
async def radiofuzzsearch(ctx, search_terms=None):
    print(search_terms)
    if search_terms != None:
        results = radio_browser.search(name=search_terms)
    else:
        results=''

    # search_param_list = ['name=','country=','countrycode=','state=','language=','tag=','codec=']
    # if_check = False
    # for item in search_param_list:
    #     if item in search_terms:
    #         if_check = True
    #     else:
    #         continue
    # if if_check:
    #     results = radio_browser.search(search_terms)
    # elif not if_check:
    #     results = radio_browser.search(name=search_terms)
    # else:
    #     await ctx.send(f"something is wrong with your search request:\n{search_terms}")
    await ctx.send(f"there are {len(results)} results including unsupported results\n\n"
                   f"please look at the results and send the station uuid to the getradiourl command\n{chr(0)}")
    send_string = f'{chr(0)}'
    unsupported_station_count = 0
    for item in results:
        if 'm3u8' in item['url_resolved']:
            unsupported_station_count +=1
            continue
        name = r"{}".format(item['name'])
        language = r"{}".format(item['language'])
        country = r"{}".format(item['country'])
        tags = r"{}".format(item['tags'])
        station_uuid = r"{}".format(item['stationuuid'])
        send_string += f"name: {name} language: {language} country: {country} tags: {tags} station uid: {station_uuid}\n\n"
    print(f'there were {unsupported_station_count} unsupported stations')
    if len(send_string) >= 2000:
        await ctx.send(f"{send_string[:1966] + '~~text cut off! be more specific!'}")
    else:
        await ctx.send(f"{send_string}")
    await ctx.send(f' \n\n\nthere was {unsupported_station_count} unsupported stations')
    if search_terms == None:
        await ctx.send(f"you can use the site https://www.radio-browser.info/#!/search to find a station you want and "
                       f"paste the exact name as the search term")


@bot.command(name='leave')
async def leave(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)
