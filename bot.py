import discord
from discord.ext import commands
import asyncio

# Add emoji and role name for reaction role
# We need to change the lines below to account for new roles with new emojis.
reaction_data = {
    '🟥': {'name': "Projecteers"},
    '🟨': {'name': "Yellow"},
    '🟦': {'name': "Blue"},
}

#read token.txt
with open('token.txt', 'r') as f:
    token = f.read()
    
def run_bot():
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix="!", intents=intents)
    
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
    
    @client.event
    async def on_raw_reaction_add(payload):
        message_id = payload.message_id
        if message_id == 1154104952063529102:
            guild_id = payload.guild_id
            guild = client.get_guild(guild_id)
            role = None
            
            if payload.emoji.name in reaction_data:
                role = discord.utils.get(guild.roles, name=reaction_data[payload.emoji.name]['name'])

            if role is not None:
                member = guild.get_member(payload.user_id)            
                if member is not None:
                    await member.add_roles(role)
                else:
                    print("Member not found")
            else: #Error handling? "UnboundLocalError: cannot access local variable 'role' where it is not associated with a value"
                print("Role not found")

    # When a user unreacts to an emoji remove the role
    @client.event
    async def on_raw_reaction_remove(payload):
        message_id = payload.message_id
        if message_id == 1154104952063529102:
            guild_id = payload.guild_id
            guild = client.get_guild(guild_id)
            role = None
            
            if payload.emoji.name in reaction_data:
                role = discord.utils.get(guild.roles, name=reaction_data[payload.emoji.name]['name'])
            
            if role is not None:
                member = guild.get_member(payload.user_id)          
                if member is not None:
                    await member.remove_roles(role)
                else:
                    print("Member not found")

            else: #Error handling? "UnboundLocalError: cannot access local variable 'role' where it is not associated with a value"
                print("Role not found")



    client.run(token)
