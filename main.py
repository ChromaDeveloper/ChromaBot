import discord
import json
import random
import asyncio
import sqlite3
from discord.ext import commands
import time
from datetime import datetime
words = ['retarded', 'goofy', 'stupid', 'annoying']
intents = discord.Intents.all()
intents.members = True
intents.guild_messages = True
intents.guild_reactions = True
bot = commands.Bot(command_prefix='c!', intents=intents , help_command=None)
conn = sqlite3.connect('warnings.db')
# Create a table to store the warnings
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS warnings (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    reason TEXT
                )''')

warns = []
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
@bot.command()
async def warn(ctx, user: discord.Member, *, reason: str):
    if ctx.message.author.guild_permissions.kick_members:
        # Add the warn to the list
        warns.append({'user': user, 'reason': reason})
        await ctx.send(f'`{user}` has been warned. Reason : `{reason}`')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")

@bot.command()
async def about(ctx, *, message: str = ""):
    embed = discord.Embed(
        title='About Page of ChromaBot',
        description=message,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1053394784900894851/1053394843990229123/aboutlogo.png')
    embed.add_field(name='Written in', value='VS-Code', inline=False)
    embed.add_field(name='Made with', value='Python 3.10.8', inline=False)
    embed.add_field(name='Author', value='Chroma#2444', inline=False)
    embed.add_field(name='Version', value='0.2 BETA', inline=False)
    await ctx.send(embed=embed)
    
@bot.command()
async def àpropos(ctx, *, message: str = ""):
    embed = discord.Embed(
        title='À propos de ChromaBot :flag_fr:',
        description=message,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1053394784900894851/1053651991764664370/frenchaboutlogo.png')
    embed.add_field(name='Écrit en', value='VS-Code', inline=False)
    embed.add_field(name='Fait avec', value='Python 3.10.8', inline=False)
    embed.add_field(name='Auteur', value='Chroma#2444', inline=False)
    embed.add_field(name='Version', value='0.2 BETA', inline=False)
    await ctx.send(embed=embed)
    
@bot.command()
async def help(ctx, *, message: str = ""):
    embed = discord.Embed(
        title='Help Page of ChromaBot',
        description=message,
        color=discord.Color.yellow()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1053394784900894851/1053394892371537970/helplogo.png')
    embed.add_field(name='c!about', value='Shows the about page of ChromaBot', inline=False)
    embed.add_field(name='c!kick', value='Kicks an user in your server. `Usage: c!kick [@someone] [reason]`', inline=False)
    embed.add_field(name='c!ban', value='Bans someone in your server. `Usage: c!ban [@someone] [reason]`', inline=False)
    embed.add_field(name='c!warn', value='Warns someone in your server. `Usage: c!warn [@someone] [reason]`', inline=False)
    embed.add_field(name='c!removewarn', value='Removes a specific warn for someone in your server. `Usage: c!removewarn [@someone] [warns]`', inline=False)
    embed.add_field(name='c!ping', value='Shows the ping.', inline=False)
    embed.add_field(name='c!insult', value='Literally insults you.', inline=False)
    embed.add_field(name='c!purge', value='Purges messages in your server. `Usage: c!purge [number of how many messages you want to remove]`', inline=False)  
    await ctx.send(embed=embed)
    
@bot.command()
async def kick(ctx, user: discord.Member, *, reason: str):
    # Check if the user has the necessary permissions to use this command
    if ctx.message.author.guild_permissions.kick_members:
        # Kick the specified user
        await user.kick(reason=reason)
        await ctx.send(f'{user} has been kicked. Reason : `{reason}`')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")

@bot.command()
async def ban(ctx, user: discord.Member, *, reason: str):
    # Check if the user has the necessary permissions to use this command
    if ctx.message.author.guild_permissions.ban_members:
        # Kick the specified user
        await user.ban(reason=reason)
        await ctx.send(f'{user} has been banned. Reason : `{reason}`')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")
            
@bot.command()
async def removewarn(ctx, user: discord.Member):
    # Check if the user has the necessary permissions to use this command
    if ctx.message.author.guild_permissions.kick_members:
        # Find the warn for the specified user
        for i, warn in enumerate(warns):
            if warn['user'] == user:
                # Remove the warn from the list
                del warns[i]
                await ctx.send(f'{user} has been removed from the warns list.')
                return
        await ctx.send(f'{user} was not found in the warns list.')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")

@bot.command()
async def ping(ctx):
    # Get the current time
    before = time.time()

    # Send a message
    await ctx.send("Pong!")

    # Get the time after sending the message
    after = time.time()

    # Calculate the difference in time
    difference = after - before

    # Send the ping time in milliseconds
    await ctx.send(f"Ping: {difference * 1000:.2f}ms")

@bot.command()
async def insult(ctx):
    selected_word = random.choice(words)
    await ctx.send(f'You are {selected_word}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, number: int):
    await ctx.channel.purge(limit=number)

bot.run('MTA1MTE4NjIxMDM2Nzg3MzEwNA.G8vUnv.JFqt4Wd-_Q-INDHBRtFlzh1LWfTRvT24dE_MJw')
