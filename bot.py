import discord
import json
import random
import asyncio
from discord.ext import commands
import datetime
import os
import time
import urlextract
import requests
import subprocess
import interactions
import yt_dlp
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='c!', intents=intents , help_command=None)
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
@bot.command()
async def warn(ctx, user: discord.Member, *, reason: str):
    if ctx.message.author.guild_permissions.kick_members:
        await ctx.send(f'`{user}` has been warned. Reason : `{reason}`')
        await user.send(f'You have been warned in {ctx.guild.name} for the following reason: {reason}')
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
    embed.add_field(name='Version', value='0.9.1-alpha', inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def help(ctx, *, message: str = ""):
    embed = discord.Embed(
        title='Help Page of ChromaBot',
        description=message,
        color=discord.Color.red()
    )
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1053394784900894851/1053394892371537970/helplogo.png')
    embed.add_field(name='c!about', value='Shows the about page of ChromaBot', inline=False)
    embed.add_field(name='c!kick', value='Kicks an user in your server. `Usage: c!kick [@someone] [reason]`', inline=False)
    embed.add_field(name='c!ban', value='Bans someone in your server. `Usage: c!ban [@someone] [reason]`', inline=False)
    embed.add_field(name='c!warn', value='Warns someone in your server. `Usage: c!warn [@someone] [reason]`', inline=False)
    embed.add_field(name='c!removewarn', value='Removes a specific warn for someone in your server. `Usage: c!removewarn [@someone] [warns]`', inline=False)
    embed.add_field(name='c!check', value='Checks if the bot is working.', inline=False)
    embed.add_field(name='c!poll', value='Makes a poll. `Usage : c!poll [something]`', inline=False)
    embed.add_field(name='c!clear', value='Clears messages in your server. `Usage: c!purge [number of how many messages you want to remove]`', inline=False)  
    embed.add_field(name='c!mute', value='Mutes a person in your server. `Usage : c!mute [@someone]`', inline=False)
    embed.add_field(name='c!unmute', value='Unmutes a person in your server. `Usage : c!unmute [@someone]`', inline=False)
    embed.add_field(name='c!rps', value='Plays a game of rock, paper, scissors. `Usage : c!rps [rock,paper,scissors]`', inline=False)
    embed.add_field(name='c!getpfp', value='Gets a profile picture from someone in your server `Usage : c!getpfp [@someone]`', inline=False)
    embed.add_field(name='c!unban', value='Unbans someone in your server. `Usage: c!unban [@someone]`', inline=False)
    embed.add_field(name='c!changelog', value='Shows the changelogs of ChromaBot. ', inline=False)
    embed.add_field(name='c!ping', value='Checks the ping of ChromaBot. ', inline=False)
    embed.add_field(name='c!birthday', value='Wishes someone happy birthday. `Usage : c!birthday [@someone]`', inline=False)
    embed.add_field(name='c!userdex', value='Starts a new userdex game', inline=False)
    embed.add_field(name='c!tts', value='Make the bot say some text to speech stuff in a voice channel. `Usage: c!tts [some random text]`', inline=False)
    embed.add_field(name='c!play', value='Plays youtube videos in a voice channel. `Usage: c!play [some youtube video url]`', inline=False)
    embed.add_field(name='c!stop', value='Disconnects the bot from the voice channel (works with tts and play)', inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def kick(ctx, user: discord.Member, *, reason: str):
    if ctx.message.author.guild_permissions.kick_members:
        await user.kick(reason=reason)
        await user.send(f'You have been kicked in {ctx.guild.name} for the following reason: {reason}')
        await ctx.send(f'{user} has been kicked. Reason : `{reason}`')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")
@bot.command()
async def ban(ctx, user: discord.Member, *, reason: str):
    if ctx.message.author.guild_permissions.ban_members:
        await user.ban(reason=reason)
        await user.send(f'You have been banned in {ctx.guild.name} for the following reason: {reason}')
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
async def check(ctx):
    before = time.time()
    await ctx.send("Everything is working fine :white_check_mark:")
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, number: int):
        await ctx.channel.purge(limit=number)
        await ctx.send(f'Cleared {number} message')
@bot.command()
async def poll(ctx, *, question: str):
    poll_message = discord.Embed(title=question, color=discord.Color.green())
    poll_message.add_field(name='\n \u2705 Yes', value='\u200b', inline=True)
    poll_message.add_field(name='\n \u274C No', value='\u200b', inline=True)
    message = await ctx.send(embed=poll_message)
    await message.add_reaction('\u2705')
    await message.add_reaction('\u274C')
@bot.command()
async def mute(ctx, member: discord.Member, time: int, *, reason: str):
    if not discord.utils.get(ctx.guild.roles, name="Muted"):
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)
    else:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(muted_role)
    await ctx.send(f"{member.mention} has been muted for {time} minutes for {reason}")
    await asyncio.sleep(time*60)
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} has been unmuted.")
@bot.command()
async def unmute(ctx, user: discord.Member):
    if ctx.message.author.guild_permissions.manage_roles:
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
        await user.remove_roles(mute_role)
        await ctx.send(f'`{user}` has been unmuted.')
    else:
        await ctx.send("Oops! You don't have permission to use this command.")
@bot.command()
async def rps(ctx, choice: str):
    choices = {"rock": ":rock:", "paper": ":page_facing_up:", "scissors": ":scissors:"}
    result_messages = {
        "rock": {
            "rock": "It's a tie!",
            "paper": "You lose! Paper beats rock.",
            "scissors": "You win! Rock beats scissors.",
        },
        "paper": {
            "rock": "You win! Paper beats rock.",
            "paper": "It's a tie!",
            "scissors": "You lose! Scissors beats paper.",
        },
        "scissors": {
            "rock": "You lose! Rock beats scissors.",
            "paper": "You win! Scissors beats paper.",
            "scissors": "It's a tie!",
        },
    }
    
    if choice.lower() not in choices:
        await ctx.send("Please choose rock, paper, or scissors.")
        return
    
    computer_choice = random.choice(list(choices.keys()))
    await ctx.send(choices[computer_choice])
    await ctx.send(result_messages[choice][computer_choice])

@bot.command()
async def getpfp(ctx, user: discord.User):
    embed = discord.Embed(title=f"{user.name}'s profile picture")
    embed.set_image(url=user.avatar)
    await ctx.send(embed=embed)

@bot.command()
async def unban(ctx, *, user: discord.User):
    if ctx.message.author.guild_permissions.ban_members:
        try:
            await ctx.guild.unban(user)
            await ctx.send(f'{user} has been unbanned.')
        except Exception as e:
            await ctx.send(f'Error: {e}')
    else:
        await ctx.send("Oops ! You don't have permission to use this command :pensive: !")

@bot.command()
async def changelog(ctx):
    embed = discord.Embed(title='ChromaBot Changelog')
    embed.add_field(name='0.1.1-alpha', value='-added moderation commands \n -bugs and issues fixed \n -added discord.ext submodule', inline=False)
    embed.add_field(name='0.2.1-alpha', value='-added check command \n -added clear command', inline=False)
    embed.add_field(name='0.3.1-alpha', value='-added mute command \n -added unmute command', inline=False)
    embed.add_field(name='0.4.1-alpha', value='-added poll command \n -added rps (Rock Paper Scissors) command', inline=False)
    embed.add_field(name='0.5.1-alpha', value='-added getpfp (getting profile pictures) command', inline=False)
    embed.add_field(name='0.6.1-alpha', value='-added changelog command \n -added unban command', inline=False)
    embed.add_field(name='0.7.1-alpha', value='-added ping command', inline=False)
    embed.add_field(name='0.8.1-alpha', value='-added birthday command \n -added userdex game', inline=False)
    embed.add_field(name='0.9.1-alpha', value='-added tts command \n -added play command \n -added stop command', inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Pong ! :ping_pong:")
    embed.add_field(name=f"Latency: {round(bot.latency * 1000)}ms", value="⁣", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def birthday(ctx, user: discord.User):
    await ctx.send(f'Happy Birthday {user.name} ! :birthday: :partying_face:    ')
@bot.command()
async def whois(ctx, member: discord.Member):
    roles = [f"<@&{role.id}>" for role in member.roles]
    embed = discord.Embed(title=f"{member.name}'s Information ({member.id})", description="", color=0x00308F)
    embed.add_field(name="Name", value=member.mention, inline=True)
    embed.add_field(name="Roles", value=' '.join(roles), inline=True)
    embed.add_field(name="Registered", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=True)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=True)
    embed.set_thumbnail(url=member.avatar)
    await ctx.send(embed=embed)
@whois.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.UserInputError):
        await ctx.send("Please provide a valid member to get information about.")
@bot.command()
async def userdex(ctx):
    members = ctx.guild.members
    human_members = [member for member in members if not member.bot]
    member = random.choice(human_members)
    embed = discord.Embed(title=f"A wild user appeared!", description=" ", color=0xffffff)
    embed.set_image(url=member.avatar)
    await ctx.send(embed=embed)
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    try:
        guess = await bot.wait_for('message', check=check, timeout=120.0)
        if guess.content == member.name:
            user = guess.author
            embed = discord.Embed(title=f"You caught {member.name} @{guess.author}!", color=0xffffff)
            embed.add_field(name="Attack :crossed_swords:", value=(random.randint(750, 1500)), inline=False)
            embed.add_field(name="Health :heart:", value=(random.randint(1250   , 3000)), inline=False)
            embed.set_image(url=member.avatar)
            await user.send(embed=embed)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Incorrect! The correct answer was {member.name}")  
    except asyncio.TimeoutError:
        await ctx.send("You took too long to guess! Better luck next time.")
@bot.command()
async def tts(ctx, *, message: str):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    subprocess.run(["espeak", "-p mb-us2", "-w output.wav", message])    
    vc.play(discord.FFmpegPCMAudio("output.wav"))
    while vc.is_playing():
        await asyncio.sleep(2)
        await vc.disconnect()
    subprocess.run(["rm", "-rf", "output.wav", message]) 
@bot.command()
async def play(ctx, *, audiolink: str):
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    
    try:
        process = await asyncio.create_subprocess_shell(
            "yt-dlp --extract-audio --audio-format mp3 -o yt.mp3 {}".format(audiolink),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await process.wait()
        if process.returncode != 0:
            raise Exception("yt-dlp command failed")
        vc.play(discord.FFmpegPCMAudio("yt.mp3"))
        while vc.is_playing():
            await asyncio.sleep(1)
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while playing the audio.")
@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    if vc is not None:
        vc.stop()
        await vc.disconnect()
    else:
        await ctx.send("You are not in a voice channel.")
    subprocess.run(["rm", "-rf", "yt.mp3"]) 
bot.run('YOUR BOT TOKEN HERE')
