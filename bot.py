import discord
from discord.ext import commands
import os
from datetime import datetime, timedelta
from dateutil import tz
import asyncio
from dbsetup import setup_db
import sqlite3
from enum import IntEnum

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

class CONST_ID(IntEnum):
    EVENT_REMINDER_CHANNEL = 1063232263929737367

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

@client.event
async def on_scheduled_event_create(event:discord.ScheduledEvent):
    NYC = tz.gettz("America/New_York")
    date = event.start_time - timedelta(days=1)
    dtm = datetime(date.year, date.month, date.day, 10, 0, 0, 0, NYC)
    conn = sqlite3.connect("reminders.db")
    c = conn.cursor()
    c.execute("INSERT INTO reminders (time, startDate, title, link) VALUES (?, ?, ?, ?)", (dtm, event.start_time, event.name, event.url))
    conn.commit()
    conn.close()

# This will run every 60s to check if there's any event that needs a reminder
async def event_clock():
    while True:
        await asyncio.sleep(60) 
        conn = sqlite3.connect("reminders.db")
        NYC = tz.gettz("America/New_York")
        c = conn.cursor()
        c.execute("SELECT * FROM reminders")
        results = c.fetchall()
        for id, trigger_datetime, start_datetime, title, link in results:
            if datetime.strptime(trigger_datetime, '%Y-%m-%d %H:%M:%S%z') < datetime.now(NYC):
                ch = client.get_channel(CONST_ID.EVENT_REMINDER_CHANNEL)
                if ch:
                    event_datetime = datetime.fromisoformat(start_datetime)
                    await ch.send(content=f"@everyone\n\nWe have our {title} event on {event_datetime.astimezone(NYC).strftime('%B %d at %I:%M %p')}!\n\n{link}",)
                    c.execute("DELETE FROM reminders WHERE id = ?", (id,))

        conn.commit()
        conn.close()


async def load_modules():
    for filename in os.listdir("cogs"): 
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def run_bot():
    with open('token.txt', 'r') as f: #read token.txt
        token = f.read()
        async with client: # wait for the client to load
            setup_db()
            await load_modules() # load all the modules
            client.loop.create_task(event_clock())
            await client.start(token) # start the bot