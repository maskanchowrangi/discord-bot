import discord
from discord.ext import commands
import json

with open('config.json') as f:
    config = json.load(f)

# making the bot
 
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Bot ready
@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')
    print(f'Connected to {len(bot.guilds)} servers')

# Welcome message
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f'Welcome {member.mention} to {member.guild.name}!')

# Warning
warnings = {} # storing temporarily

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason):
    if member.id not in warnings:
        warnings[member.id] = []

    warnings[member.id].append(reason)
    await ctx.send(f'{member.mention} has been warned for: {reason}')
    await ctx.send(f'Total warning: {len(warnings[member.id])}')

@bot.command()
async def warnings(ctx, member: discord.Member):
    if member.id in warnings:
        warning_list = '\n'.join(warnings[member.id])
        await ctx.send(f'Warnings for {member.mention}:\n{warning_list}')
    else:
        await ctx.send(f'{member.mention} has no warnings!')

# Server info

@bot.command()
async def serverinfo(ctx):
    guild = ctx.build

    embed = discord.Embed(title=f"{guild.name} Info", color=discord.Color.blue())
    embed.add_field(name="Owner", value=guild.owner.mention)
    embed.add_field(name="Member", value=guild.member.count)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))

    await ctx.send(embed=embed)

# Command (ping)
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# Command (hello)
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

# Command (kick)
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f'({member.mention} has been kicked! Reason: {reason})')

# Command (ban)
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f'({member.mention} has been banned! Reason: {reason})')

# Command (clear)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount +1)
    await ctx.send(f'Cleared {amount} messages!', delete_after=3)

# Error handeling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission for this command!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("I couldn't find that memeber")
    else:
        await ctx.send("An error occurred: ")

# Run bot (with token)
bot.run(config['token'])