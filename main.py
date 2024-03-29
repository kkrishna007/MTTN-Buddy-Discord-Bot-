import discord
from discord.ext import commands
import json
import pandas as pd
import tabulate
from dotenv import load_dotenv
import os
from correctbranch import CorrectedBranch
from models import *
import random

databaseFile = open('database.json',)
data = json.load(databaseFile)
load_dotenv('.env')
# TODOs:
# Return the table when mentioned
# Category command
# Add Random facts about Manipal


bot = commands.Bot(command_prefix='.', help_command=None,
                   description="This bot returns the cutoffs")
# df = pd.DataFrame.from_dict(data['branches'])
# print(df)



def GetCutoff(branch):
    print(type(branch))
    # print(data['branches'])
    print(len(data['branches']))
    cutoffSearch = 0
    roundName = ''
    for i in data['branches']:
        # print("Current i is", i)

        if(i['name'].lower() == str(branch).lower()):
            # print("if wala i is", i)
            cutoffSearch = i
            roundName = i['1st_round']
        # else:
        #     print("asdasdasd i is", i)

    if(cutoffSearch != 0):
        branchString = f"Cutoffs for the branch **{branch.upper()}**: \n\n2022 Counselling: \n3rd Round: **{str(cutoffSearch['3rd_round'])}.** \n2nd Round: **{str(cutoffSearch['2nd_round'])}.** \n1st Round: **{str(cutoffSearch['1st_round'])}.** \n\nPrevious Year Cutoffs : \n2021  : **{str(cutoffSearch['cutoff_2021'])}.** \n2020:  **{str(cutoffSearch['cutoff_2020'])}.** \n2019: **{str(cutoffSearch['cutoff_2019'])}.**\n"
        print(f"<{cutoffSearch['link']}>")
        linkString = f"The course outline for **{branch.upper()}** can be found at: <{cutoffSearch['link']}>"
        zeroString = f"0 -->  indicates that the no. of seats were not filled for the particular branch and anyone was eligible for them"
        branchMessage = branchString + "\n" + zeroString + "\n\n" + linkString
        return branchMessage, linkString

    else:
        return "Sorry! You have entered an invalid command. Try .help to get the list of commands"


@bot.event
async def on_ready():
    print("I am alive on the MTTN Server")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='https://bit.ly/MTTNMOVIE (link is all caps)'))


@bot.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** {round(bot.latency * 1000)}ms')
    print("found")


@bot.command()
async def something(ctx):
    await ctx.send('pong')


@bot.command(name="cutoff")
async def cutoff(ctx, *, arg):
    correctedBranch = CorrectedBranch(arg)
    cutoff, courseString = GetCutoff(correctedBranch)
    await ctx.channel.send("Hey! " + ctx.author.mention + "\n")
    await ctx.channel.send(cutoff)


@bot.command(name="course")
async def cutoff(ctx, *, arg):
    correctedBranch = CorrectedBranch(arg)
    cutoff, courseString = GetCutoff(correctedBranch)
    await ctx.channel.send("Hey! " + ctx.author.mention + "\n")
    await ctx.channel.send(courseString)


@bot.command()
async def fact(ctx):
    facts=[
        "With 800+ Rooms in MIT Block 10, it's one of Asia's largest single hostel buildings.",
        "Padubidri Beach is one of the 8 beaches in India that were awarded the blue flag recognition",
        "Most popularly known as the 'Campus Town' because the entire town is brimming with students from all over the world!",
        "Manipal Museum of Anatomy & Pathology is one of the largest of its kind in Asia",
        "Manipal gets its name from the famous Manipal Lake"
        ]
    await ctx.send("**Fact: ** "+random.choice(facts))


@bot.command()
async def help(ctx):
    helpString = f'```(1) Mention me @MTTN Bot to get the branch wise cutoff table \n\n(2) Use ".cutoff branch" -> Get the cutoff and course structure \nEg: .cutoff EE --> Returns the information about Electrical and Electronics \n\n(3) Use ".guide" -> Freshers guide to Manipal \n\n(4) Use ".laptop" -> Laptop Guide for freshers\n\n(5) Use ".course branch" -> Returns the syllabus of that branch ```'
    await ctx.channel.send("Here is a list of commands that you can use:" + helpString)


@bot.command()
async def laptop(ctx):
    await ctx.channel.send("Hey! Here is the MTTN's recommended laptop guide: <https://www.manipalthetalk.org/manipal/freshers-guide/mttns-laptop-buying-guide-for-college/>")
    await ctx.channel.send("Also check out our freshers portal which contains all the information that you might need: <https://freshers.manipalthetalk.org/> ")


@bot.command()
async def guide(ctx):
    await ctx.channel.send("Hey! " + ctx.author.mention + "\n")
    await ctx.channel.send("We have compiled a list of all the resources that you might need as a fresher at Manipal: <https://freshers.manipalthetalk.org/> ")


@bot.listen()
async def on_message(message):
    for x in message.mentions:
        if (x == bot.user):
            await message.channel.send("Hey! " + message.author.mention + "\nI am your friendly neightbourhood bot. Here is the cutoffs table for the last year for each branch")
            df = pd.DataFrame.from_dict(data['branches'])
            df = df.drop(['link', 'cutoff_2019', '3rd_round'], axis=1)
            df.columns = ["Branch Name",
                          "Latest (2022 2nd Round)", "2021 Cutoff"]
            df.reset_index(drop=True, inplace=True)
            print(df)
            await message.channel.send(f"```{df}``` \n\n 0 -->  indicates that the no. of seats quota wasn't filled for the particular branch and anyone was eligible for them")
            await message.channel.send("**NOTE:** The data is not 100\% accurate")
            await message.channel.send('\nYou can also use the command **".cutoff branchname"** to get the information of a particular branch \nOr use the ".help" command to get help ')

        # df = pd.json_normalize(data['branches'])
        # print(df)

        # print table
        # await message.channel.send(message.author.mention)


bot.run(os.getenv('TOKEN'))
# @bot.event
# async def on_message(message):
#     if bot.user.mentioned_in(message):
#         await message.channel.send("hogaysa mention")
#         await message.channel.send(message.author.mention)


# @bot.command(name="ping")
# async def ping(ctx):
#     await ctx.channel.send("Yo")

# def createMessage(branch):
#     for key
