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
    
    @client.event
    async def on_raw_reaction_add(payload):
        message_id = payload.message_id
        if message_id == 1154104952063529102:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

            # We need to change the lines below to account for new roles with new emojis.
            if payload.emoji.name == '🟥':
                role = discord.utils.get(guild.roles, name="Projecteers")
            elif payload.emoji.name == '🟨':
                role = discord.utils.get(guild.roles, name="Yellow")
            elif payload.emoji.name == '🟦':
                role = discord.utils.get(guild.roles, name="Blue")

            if role is not None:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)            
                if member is not None:
                    await member.add_roles(role)
                else:
                    print("Member not found")
            else: #Error handling? "UnboundLocalError: cannot access local variable 'role' where it is not associated with a value"
                print("Role not found")

    # Create the code to remove a role when a user unreacts to an emoji.
    @client.event
    async def on_raw_reaction_remove(payload):
        pass



    client.run(token)
