import config
import discord
from discord.ext import commands
import sqlite3

client = commands.Bot(command_prefix = "$")

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
             irl,
             game,
             username
             )""")

def start_bot():
    @client.event
    async def on_ready():
        print('Bot is ready.')

    @client.event
    async def on_member_join(member):
        print(f'{member} has joined the server')

    @client.event
    async def on_member_remove(member):
        print(f'{member} has left the server')

    @client.command()
    async def dnsbot(ctx, flag = None, *args):
        if flag == None:
            await ctx.send('Type "dnsbot -h" for help')
        elif flag[0] != '-':
            await ctx.send('No flag specified')
        else:
            arg_num = len(args)

            if flag == '-a' and arg_num == 3:
                try:
                    with conn:
                        c.execute("""INSERT INTO users (irl, game, username)
                                  VALUES (?, ?, ?)
                                  """, (args[0].lower(), args[1].lower(), args[2].lower()))
                    await ctx.send('Added {} to {} for user {}'.format(args[2], args[1], args[0]))
                except:
                    await ctx.send('Invalid arguments! Try checking to make sure it\'s $dnsbot {user} {game} {username}')
            elif flag == '-h':
                await ctx.send('`Usage: $dnsbot [-ahg] [args]\n' +
                               'a: add username for specified user and game [-a user game username]\n' +
                               'h: print this help message\n' +
                               'g: get the username for a specified user and game`')
            elif flag == '-g' and arg_num == 2:
                try:
                    with conn:
                        c.execute("""SELECT username FROM users
                                  WHERE irl=? AND game=? 
                                  """, (args[0].lower(), args[1].lower()))
                    response = c.fetchone()[0]
                    await ctx.send('{}\'s username for {} is '.format(args[0], args[1]) + response + '.')
                except:
                    await ctx.send('Invalid arguments!')
            else:
                await ctx.send('Invalid flag or number of arguments')

    client.run(config.token)

def main():
    start_bot()

if __name__ == '__main__':
    main()