import config
import discord
from discord.ext import commands
import sqlite3
from commands import start_bot

def initialize_bot_client():
    client = commands.Bot(command_prefix = "$")
    return client

def initialize_db():
    conn = sqlite3.connect(':memory:')

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
                 irl,
                 game,
                 username
                 )""")

    return (conn, c)

def main():
    client = initialize_bot_client()
    conn, c = initialize_db()
    start_bot(client, conn, c)
    client.run(config.token)

if __name__ == '__main__':
    main()
