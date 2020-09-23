# bot.py
import os

import discord
from discord.ext import commands as c
from dotenv import load_dotenv
import json
import requests


command_prefix='pb!'
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv("DISCORD_GUILD")
# client = discord.Client()
client = c.Bot(command_prefix=command_prefix)
bot = c.Bot(command_prefix=command_prefix)


@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)

    print(
        f'\'{client.user}\' is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
        )

@client.event
async def on_member_join(member):
    print(f'{member} has joined {GUILD}')

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! \n responded in {round(client.latency * 1000,4)} ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx,*,question):
    answer = requested_8ball(question)
    await ctx.send(answer['answer'])
    await ctx.send(f'the response type was {answer["type"]}')

def requested_8ball(question):
    url = 'https://8ball.delegator.com/magic/JSON/'
    response = requests.get(url+question).json()
    return response['magic']

client.run(TOKEN)
