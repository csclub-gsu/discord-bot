import discord
from discord.ext import commands
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    await client.tree.sync()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message:discord.Message):
    if message.content.startswith('hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)


async def load_modules():
    for filename in os.listdir("cogs"): 
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def run_bot():
    with open('token.txt', 'r') as f: #read token.txt
        token = f.read()
        async with client: # wait for the client to load
            await load_modules() # load all the modules
            await client.start(token) # start the bot