import os
import random
import praw
from dotenv import load_dotenv
import discord
from discord.ext import commands



load_dotenv()
pref = "n!"
client = commands.Bot(command_prefix=pref)
f = open("rules.txt","r")
rules = f.readlines()
muted_r = 880859101247197234
with open('filtered_words.txt') as filtered:
    filtered = filtered.read().strip().lower().split(', ')


#bot events 
@client.event
async def on_ready():
  print("Flying Nimbus is ready to strike under Nyoibo#3080")

@client.event
async def on_message(message):
    for word in filtered:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f'{message.author.mention}! Read the rules again!')
            return
        else:
        	await client.process_commands(message) 

@client.event
async def on_command_error(ctx,error):
	if isinstance(error,commands.MissingPermissions):
		await ctx.send("You don't have Permission to use this command!")
		await ctx.message.delete()
	elif isinstance(error,commands.MissingRequiredArgument):
		await ctx.send("You are missing required arguments to use this command!")
		await ctx.message.delete()
	else:
		raise error 



#Meme
reddit = praw.Reddit(client_id = os.environ['r_cid'],
					client_secret = os.environ['r_csecret'],
					username = os.environ['r_uname'],
					password = os.environ['r_pass'],
					user_agent = os.environ['r_uagent'])



#Bot Commands 
@client.command()
async def meme(ctx):
	subreddit = reddit.subreddit("memes")
	top = subreddit.top(limit = 25)
	for submission in top:
		r_asub = append(submission)
		r_rsub = random.choice(r_asub)
		title = r_rsub.title
		image = r_rsubs.url

		embed = discord.Embed(title =  title)
		embed.set_image(url = image)
		await ctx.send(embed = embed)



#Bot Runner
client.run(os.environ['bottok'])