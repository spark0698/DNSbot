import config
import discord
from discord.ext import commands
import sqlite3

client = commands.Bot(command_prefix = "$")

conn = sqlite3.connect('users.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
             irl,
             discord
             )""")

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server")

client.run(config.token)