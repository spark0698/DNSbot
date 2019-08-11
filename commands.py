import config
import discord
from discord.ext import commands
import sqlite3

def add_username(irl, game, username):
    try:
        with conn:
            c.execute("""INSERT INTO users (irl, game, username)
                      VALUES (?, ?, ?)
                      """, (irl.lower(), game.lower(), username.lower()))
        await ctx.send('Added {} to {} for user {}'.format(args[2], args[1], args[0]))
    except:
        await ctx.send('Invalid arguments! Try checking to make sure it\'s $dnsbot {user} {game} {username}')

def grab_username(irl, game):
    try:
        with conn:
            c.execute("""SELECT username FROM users
                      WHERE irl=? AND game=? 
                      """, (irl.lower(), game.lower()))
        response = c.fetchone()[0]
        await ctx.send('{}\'s username for {} is '.format(args[0], args[1]) + response + '.')
    except:
        await ctx.send('Invalid arguments!')

def start_bot(client, conn, c):
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
        if flag is None or flag[0] != '-':
            await ctx.send('Type "dnsbot -h" for help')
        else:
            arg_num = len(args)

            if flag == '-a' and arg_num == 3:
                add_username(args[0], args[1], args[2])
            elif flag == '-h':
                await ctx.send('`Usage: $dnsbot [-ahg] [args]\n' +
                               'a: add username for specified user and game [-a user game username]\n' +
                               'h: print this help message\n' +
                               'g: get the username for a specified user and game`')
            elif flag == '-g' and arg_num == 2:
                grab_username(args[0], args[1])
            else:
                await ctx.send('Invalid flag or number of arguments')
