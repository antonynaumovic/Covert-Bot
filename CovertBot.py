import discord, os
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time, json, requests
from discord.voice_client import VoiceClient

bot=discord.Client()
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Ready")
    await bot.change_presence(game=discord.Game(name="Covert eSports", type=3))
    for server in bot.servers:
        for channel in server.channels:
            if "rules" in channel.name:
                global startChannel
                startChannel = channel
            elif "roles" in channel.name:
                global rolesChannel
                rolesChannel = channel
            elif "welcome" in channel.name:
                global welcomeChannel
                welcomeChannel = channel
            elif channel.id == "510644219401076736":
                global totalChannel
                totalChannel = channel
            elif channel.id == "510644235196956712":
                global memberChannel
                memberChannel = channel
            elif channel.id == "510644246169255954":
                global botChannel
                botChannel = channel


    for emoji in bot.get_all_emojis():
        if emoji.name == "R6S":
            global emojiR6S
            emojiR6S = emoji
        elif emoji.name == "CS":
            global emojiCS
            emojiCS = emoji
        elif emoji.name == "Fortnite":
            global emojiFN
            emojiFN = emoji
        elif emoji.name == "BO4":
            global emojiBO4
            emojiBO4 = emoji
   
    for server in bot.servers:
        global roleBO4
        roleBO4 = discord.utils.get(server.roles, name="Black Ops 4")
        global roleCS
        roleCS = discord.utils.get(server.roles, name="CS:GO")
        global roleFN
        roleFN = discord.utils.get(server.roles, name="Fortnite")
        global roleR6S
        roleR6S = discord.utils.get(server.roles, name="Rainbow Six Siege")
        global roleMember
        roleMember = discord.utils.get(server.roles, name="Member")
        global roleNew
        roleNew = discord.utils.get(server.roles, name="New")

    async for message in bot.logs_from(startChannel, limit=10):
            await bot.delete_message(message)
    async for message in bot.logs_from(rolesChannel, limit=10):
        await bot.delete_message(message)

    embed=discord.Embed(title="To Accept Rules Add Tick", color=0xcc0000)
    embed.set_author(name="Covert eSports", icon_url="https://images-ext-2.discordapp.net/external/6cIGd8Nx7_MGsi1Lh9o5-LKkFuzB8GdNTJ1YXP1b0iU/https/media.discordapp.net/attachments/510625016078139403/510627786092838930/image-2.png")
    embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/6cIGd8Nx7_MGsi1Lh9o5-LKkFuzB8GdNTJ1YXP1b0iU/https/media.discordapp.net/attachments/510625016078139403/510627786092838930/image-2.png")
    embed.add_field(name=1, value="Rule 1", inline=False)
    embed.add_field(name=2, value="Rule 2", inline=False)
    embed.add_field(name=3, value="Rule 3", inline=False)
    embed.add_field(name=4, value="Rule 4", inline=False)
    embed.add_field(name=5, value="Rule 5", inline=False)
    embed.set_footer(text="React To Accept Rules")
    welcomeRoles = await bot.send_message(startChannel, embed=embed)


    await bot.add_reaction(welcomeRoles, "✅")

    embed=discord.Embed(title="Choose Game", color=0xcc0000)
    embed.set_author(name="Covert eSports", icon_url='https://media.discordapp.net/attachments/510625016078139403/510627786092838930/image-2.png')
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/510625016078139403/510627786092838930/image-2.png')
    embed.add_field(name=emojiBO4, value="Black Ops 4", inline=True)
    embed.add_field(name=emojiCS, value="CS:GO", inline=True)
    embed.add_field(name=emojiFN, value="Fortnite", inline=True)
    embed.add_field(name=emojiR6S, value="Rainbow Six Siege", inline=True)
    embed.set_footer(text="React To Gain Roles")

    gameRoles = await bot.send_message(rolesChannel, embed=embed)
    await bot.add_reaction(gameRoles, emojiBO4)
    await bot.add_reaction(gameRoles, emojiCS)
    await bot.add_reaction(gameRoles, emojiFN)
    await bot.add_reaction(gameRoles, emojiR6S)

@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    if user.id != "510626176008454145":
        
        if reaction.emoji == emojiBO4 and channel == rolesChannel:
            await bot.add_roles(user, roleBO4)
        elif reaction.emoji == emojiCS and channel == rolesChannel:
            await bot.add_roles(user, roleCS)
        elif reaction.emoji == emojiFN and channel == rolesChannel:
            await bot.add_roles(user, roleFN)
        elif reaction.emoji == emojiR6S and channel == rolesChannel:
            await bot.add_roles(user, roleR6S)
        elif reaction.emoji == "✅" and channel == startChannel:
            await bot.add_roles(user, roleMember)
            await bot.remove_roles(user, roleNew)

@bot.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    if user.id != "510626176008454145":
        
        if reaction.emoji == emojiBO4 and channel == rolesChannel:
            await bot.remove_roles(user, roleBO4)
        elif reaction.emoji == emojiCS and channel == rolesChannel:
            await bot.remove_roles(user, roleCS)
        elif reaction.emoji == emojiFN and channel == rolesChannel:
            await bot.remove_roles(user, roleFN)
        elif reaction.emoji == emojiR6S and channel == rolesChannel:
            await bot.remove_roles(user, roleR6S)
        elif reaction.emoji == "✅" and channel == startChannel:
            await bot.remove_roles(user, roleMember)
            await bot.add_roles(user, roleNew)

@bot.event
async def on_member_join(member):
    h = 0
    print("{} Has Joined".format(member))
    embed=discord.Embed(title=str(member.name), color=0xcc0000)
    embed.set_author(name="Welcome To Covert:", icon_url="https://images-ext-2.discordapp.net/external/6cIGd8Nx7_MGsi1Lh9o5-LKkFuzB8GdNTJ1YXP1b0iU/https/media.discordapp.net/attachments/510625016078139403/510627786092838930/image-2.png")
    embed.set_thumbnail(url=member.avatar_url)
    await bot.send_message(welcomeChannel, embed=embed)
    await bot.add_roles(member, roleNew)
    t = 0
    b = 0
    for i in member.server.members:
        t += 1
        if i.bot == True:
            b +=1
    h = t - b
    await bot.edit_channel(channel = totalChannel, name="╔-total-﹝{}﹞".format(t))
    await bot.edit_channel(channel = memberChannel, name="╠-members-﹝{}﹞".format(h))
    await bot.edit_channel(channel = botChannel, name="╚-bots-﹝{}﹞".format(b))

@bot.command(pass_context=True)
async def total(ctx):
    async for message in bot.logs_from(ctx.message.channel, limit=1):
            await bot.delete_message(message)
    t = 0
    b = 0
    for i in ctx.message.server.members:
        t += 1
        if i.bot == True:
            b +=1
    h = t - b
    await bot.edit_channel(channel = totalChannel, name="╔-total-﹝{}﹞".format(t))
    await bot.edit_channel(channel = memberChannel, name="╠-members-﹝{}﹞".format(h))
    await bot.edit_channel(channel = botChannel, name="╚-bots-﹝{}﹞".format(b))

bot.run(os.getenv('TOKEN'))