import discord
from discord.ext import commands
from enum import IntEnum

# Add emoji and role name for reaction role
# We need to change the lines below to account for new roles with new emojis.
reaction_data = {
    '🟥': {'name': "Projecteers"},
    '🟨': {'name': "Yellow"},
    '🟦': {'name': "Blue"},
}

class CONST_ID(IntEnum):
    TARGET_MESSAGE = 1154104952063529102


class RoleAssigner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        message_id = payload.message_id
        if message_id == CONST_ID.TARGET_MESSAGE:
            guild_id = payload.guild_id
            guild = self.bot.get_guild(guild_id)
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
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload:discord.RawReactionActionEvent):
        message_id = payload.message_id
        if message_id == CONST_ID.TARGET_MESSAGE:
            guild_id = payload.guild_id
            guild = self.bot.get_guild(guild_id)
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


async def setup(bot):
    await bot.add_cog(RoleAssigner(bot))