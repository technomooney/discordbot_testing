# bot.py
import os
from discord.ext import commands as c
import dotenv
import requests
dotenv.load_dotenv()
import pyradios

radio_browser = pyradios.radios.RadioBrowser()

CUSTOM_PREFIXES = eval(os.getenv('CUSTOM_PREFIXES'))
print(CUSTOM_PREFIXES)
print(type(CUSTOM_PREFIXES))
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv("DISCORD_GUILD")

#You'd need to have some sort of persistance here,
#possibly using the json module to save and load
#or a database

default_prefix = ['1!']


async def determine_prefix(ctx, message):
    guild = message.guild
    #Only allow custom prefixs in guild
    if guild:
        return CUSTOM_PREFIXES.get(guild.id, default_prefix)
    else:
        return default_prefix

client = c.Bot(command_prefix=determine_prefix)

@client.command(name='setprefix')
@c.guild_only()
async def set_prefix(ctx, *, prefixes=""):
    #You'd obviously need to do some error checking here
    #All I'm doing here is if prefixes is not passed then
    #set it to default
    print(ctx.guild.id)
    CUSTOM_PREFIXES[ctx.guild.id] = prefixes.split() or default_prefix
    await ctx.send("Prefixes set!")




@client.event
async def on_ready():
    guilds = client.guilds
    print(
        f'\'{client.user}\' is connected to the following guild:\n')
    for item in guilds:
        print(item)


@client.event
async def on_member_join(member):
    print(f'{member} has joined {GUILD}')




@client.command()
async def ping(ctx):
    await ctx.send(f'pong! \n responded in {round(client.latency * 1000,4)} ms')


@client.command(name="8ball",help="send a question to be answered by the api at 8ball.delegator.com\n")
async def _8ball(ctx, *, question):
    answer = _8ball_api(question)
    await ctx.send(f"Question: {answer['question']}\n Answer: {answer['answer']}")
    await ctx.send(f'the response type was {answer["type"]}')


def _8ball_api(question):
    url = 'https://8ball.delegator.com/magic/JSON/'
    response = requests.get(url+question).json()
    return response['magic']


@client.command(aliases=["quit"])
@c.has_any_role('admin','Admin')
async def close(ctx):
    dotenv.set_key('.env',"CUSTOM_PREFIXES",str(CUSTOM_PREFIXES))
    await ctx.send('Ok, Bye!')
    await client.close()
    print("Bot Closed")  # This is optional, but it is there to tell you.




@client.command(name="pissybot",help=""""generate an insult using the evilinsult.com api, defaults to english
 use one of the following language code for a different lang
cn,de,el,en,es,fr,ru,sw""")
async def pissy_bot(ctx,language="en"):
    if language not in ["cn","de","el","en","es","fr","ru","sw"]:
        await ctx.send(f" the language code `{language}` is not supported, use the help command for more info, defaulting to `en`")
        response = requests.get(f"https://evilinsult.com/generate_insult.php?lang={'en'}").text
    else:
        response = requests.get(f"https://evilinsult.com/generate_insult.php?lang={language}").text
    await ctx.send(response)

client.run(TOKEN)
