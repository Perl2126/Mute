# Libs
from typing import Optional
import discord
import datetime, asyncio, random
from pathlib import Path
from Cybernator import Paginator
import json
import contextlib
import io
import textwrap

from discord import Member
from discord.ext import commands
from discord.ext.commands.errors import BadUnionArgument
from discord.ext.commands import has_permissions, MissingPermissions

# Setup
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}")

# Things
secret_file = json.load(open(cwd + '/secrets.json'))
bot = commands.Bot(command_prefix='p!', intents=discord.Intents.all(), case_insensitive=True)
bot.config_token = secret_file['token']
bot.remove_command('help')


# Status & Start
@bot.event
async def on_ready():
    print(f"Loggined in as: {bot.user.name}")

# Команда mute
@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, time: int, reason=None):
    mute_role = discord.utils.get(ctx.message.guild.roles, name='Muted')
    if not mute_role:
        mute_role = await ctx.guild.create_role(name='Muted',
                                                permissions=discord.Permissions(send_messages=False),
                                                color=discord.Color.red())
        for i in ctx.guild.channels:
            await i.set_permissions(mute_role, send_messages=False)
        mute_role = discord.utils.get(ctx.message.guild.roles, name='Parrot Muted')
    if mute_role:
        emb = discord.Embed(title='Мут', timestamp=ctx.message.created_at,
                            colour=discord.Colour.from_rgb(207, 215, 255))
        emb.add_field(name='Выдал мут', value=ctx.message.author.mention, inline=True)
        emb.add_field(name='Нарушитель', value=member.mention)
        emb.add_field(name='Причина', value=reason, inline=True)
        emb.add_field(name='Время', value=time, inline=True)
        emb.set_footer(text=f'Запросил: {ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        await member.add_roles(mute_role)
        await ctx.send(embed=emb)
        await asyncio.sleep(time * 60)
        await member.remove_roles(mute_role)
    else:
        await ctx.send("Неверный аргумент!")

# Start bot
bot.run(bot.config_token)