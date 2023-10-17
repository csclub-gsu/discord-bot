import discord
from discord.ext import commands
from enum import IntEnum


class CONST_ID(IntEnum):
    QUESTION_CHANNEL = 1159522268364406905
    LIST_ANSWER_CHANNEL = 1161287625248866404


class EventPolls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # the following code updates the poll whenever a user reacts on an emoji or adds a question
    # this needs to be called in order to update the list  
    async def update_question_list(self):
        messages = [message async for message in self.bot.get_channel(CONST_ID.QUESTION_CHANNEL).history(limit=123)]
        store_messages = []
        for msg in messages:
            count = 0
            for reaction in msg.reactions:
                if reaction.me: count+=reaction.count
            store_messages.append([count, msg.content])
        
        for idx, msg in enumerate(sorted(store_messages, key=lambda x: x[0], reverse=True)):
            store_messages[idx] = f'{idx}. {msg[1]} (votes: {msg[0]})'

        channel = self.bot.get_channel(CONST_ID.LIST_ANSWER_CHANNEL)
        await channel.send('\n'.join(store_messages))


    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        if msg.channel.id == CONST_ID.QUESTION_CHANNEL and not msg.author.bot:
            reaction = '⬆️'
            await msg.add_reaction(reaction)
            await self.update_question_list()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        if payload.channel_id == CONST_ID.QUESTION_CHANNEL and not payload.member.bot:
            if payload.emoji.name == '⬆️':
                await self.update_question_list()


async def setup(bot):
    await bot.add_cog(EventPolls(bot))