import discord
import asyncio

#read token.txt
with open('token.txt', 'r') as f:
    token = f.read()
    
def run_bot():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    @client.event
    async def on_message(message):
        if message.content.startswith('hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await message.channel.send(msg)

    client.run(token)
