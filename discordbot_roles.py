import discord

client = discord.Client(intents=discord.Intents().all())

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 1081256312098275380:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == '🟥':
            role = discord.utils.get(guild.roles, name="Red")
            print(role)
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

@client.event
async def on_raw_reaction_remove(payload):
    pass

client.run("")