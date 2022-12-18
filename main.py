import discord
import json
import random
import asyncio
from discord.ext import commands
import time
from datetime import datetime
words = ['retarded', 'goofy', 'stupid', 'annoying']
intents = discord.Intents.all()
intents.members = True
intents.guild_messages = True
intents.guild_reactions = True
bot = commands.Bot(command_prefix='c!', intents=intents , help_command=None)

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
    embed.add_field(name='Version', value='0.3 BETA', inline=False)
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
    if ctx.message.author.guild_permissions.kick_members:
        await user.kick(reason=reason)
        await ctx.send(f'{user} has been kicked. Reason : `{reason}`')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")

@bot.command()
async def ban(ctx, user: discord.Member, *, reason: str):
    if ctx.message.author.guild_permissions.ban_members:
        await user.ban(reason=reason)
        await ctx.send(f'{user} has been banned. Reason : `{reason}`')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")
            
@bot.command()
async def removewarn(ctx, user: discord.Member):
    if ctx.message.author.guild_permissions.kick_members:
        for i, warn in enumerate(warns):
            if warn['user'] == user:
                del warns[i]
                await ctx.send(f'{user} has been removed from the warns list.')
                return
        await ctx.send(f'{user} was not found in the warns list.')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")
@bot.command()
async def ping(ctx):
    before = time.time()
    await ctx.send("Pong!")
    after = time.time()
    difference = after - before
    await ctx.send(f"Ping: {difference * 1000:.2f}ms")
@bot.command()
async def insult(ctx):
    selected_word = random.choice(words)
    await ctx.send(f'You are {selected_word}')
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, number: int):
    await ctx.channel.purge(limit=number)
@bot.command()
async def poll(ctx, *, question: str):
    # Create the poll message and add the question as the title
    poll_message = discord.Embed(title=question, color=discord.Color.green())
    # Add the reactions for the poll options
    poll_message.add_field(name='\n \u2705 Yes', value='\u200b', inline=True)
    poll_message.add_field(name='\n \u274C No', value='\u200b', inline=True)
    # Send the poll message
    message = await ctx.send(embed=poll_message)
    # Add the reactions to the message
    await message.add_reaction('\u2705')
    await message.add_reaction('\u274C')
@bot.command()
async def mute(ctx, user: discord.Member, *, reason: str):
    # Check if the user has the necessary permissions
    if ctx.message.author.guild_permissions.manage_roles:
        # Create the mute role if it doesn't exist
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if mute_role is None:
            mute_role = await ctx.guild.create_role(name='Muted')
        # Set the permissions of the mute role to restrict sending messages
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)
        # Add the mute role to the user
        await user.add_roles(mute_role)
        # Send a message to confirm that the user has been muted
        await ctx.send(f'`{user}` has been muted. Reason: `{reason}`')
    else:
        await ctx.send("Oops! You don't have permission to use this command.")
@bot.command()
async def unmute(ctx, user: discord.Member):
    # Check if the user has the necessary permissions
    if ctx.message.author.guild_permissions.manage_roles:
        # Get the mute role
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
        # Remove the mute role from the user
        await user.remove_roles(mute_role)
        # Send a message to confirm that the user has been unmuted
        await ctx.send(f'`{user}` has been unmuted.')
    else:
        await ctx.send("Oops! You don't have permission to use this command.")
bot.run('MTA1MTE4NjIxMDM2Nzg3MzEwNA.G4MUCn.ugxj-xTZeAKUlBlrmOmuaLNY_qbBr0NeR5aheo')
