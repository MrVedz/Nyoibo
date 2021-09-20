import os
import random
import praw				#install using pip install praw
from dotenv import load_dotenv		#install using pip install python-dotenv
import discord				#install using pip install discord
from discord.ext import commands



#bot variables
load_dotenv()
pref = "n!"
client = commands.Bot(command_prefix=pref)
f = open("rules.txt","r")
rules = f.readlines()
muted_r = os.environ['muted_id']
with open('filtered_words.txt') as filtered:
    filtered = filtered.read().strip().lower().split(', ')	#reads all the words in lower case only 
								#and seperates each word in the list


#Reddit
reddit = praw.Reddit(client_id = os.environ['r_cid'],		#reddit client id
		client_secret = os.environ['r_csecret'],	#reddit website application secret
		username = os.environ['r_uname'],		#username of Reddit account
		password = os.environ['r_pass'],		#password of the Reddit account
		user_agent = os.environ['r_uagent'])		#just name your own agent(anything)



#Bot Events
@client.event
async def on_ready():
  print("Flying Nimbus is ready to strike under Nyoibo#3080")	#On ready message

#Auto Moderation Event
@client.event
async def on_message(msg):
    for word in filtered:
        if word in msg.content.lower():
            await msg.delete()
            await msg.channel.send(f'{msg.author.mention}! Read the rules again!')
            return
    await client.process_commands(msg)

#Error Event
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



#bot commands
@client.command()
async def ping(ctx):
  await ctx.send("I am online!")
  
@client.command(aliases=['r' or 'rules'])
async def rule(ctx,*,number):
  await ctx.send(rules[int(number)])

@client.command()
async def test(ctx):
  await ctx.send(f_words)
  
@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,*,amount=10):
  await ctx.channel.purge(limit=amount)
  await ctx.send("Messages cleared successfully!")
  
@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason = "No reason provided"):
    try:
    	await member.send("You have been kicked from the server. Reason:"+reason)
    except:
    	await ctx.send("The member has their DM's Closed")
    await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason = "No reason provided"):
    try:
    	await member.send("You have been banned from the server. Reason:"+reason)
    except:
    	await ctx.send(member.name +" has been banned from the server. Reason:"+reason)
    await member.ban(reason=reason)

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
  banned_users = await ctx.guild.bans()
  member_name, member_disc = member.split('#')

  for banned_entry in banned_users:
    user = banned_entry.user

    if(user.name, user.discriminator)==(member_name,member_disc):

      await ctx.guild.unban(user)
      await ctx.send(member_name +" has been unbanned!")
      return

  await ctx.send(member+" was not found")
 
@client.command(aliases=['m'])
@commands.has_permissions(kick_members = True)
async def mute(ctx,member : discord.Member):
  muted_role = ctx.guild.get_role(muted_r)

  await member.add_roles(muted_role) 
  await ctx.send(member.mention +" has been muted.") 

@client.command(aliases=['um'])
@commands.has_permissions(kick_members = True)
async def unmute(ctx,member : discord.Member):
  muted_role = ctx.guild.get_role(muted_r) 

  await member.remove_roles(muted_role) 
  await ctx.send(member.mention +" has been unmuted.") 

@client.command(aliases=['user','info'])
@commands.has_permissions(kick_members = True)
async def whois(ctx, member : discord.Member):
	embed = discord.Embed(title = member.name , description = member.mention, color = discord.Color.green())
	embed.add_field(name = 'ID', value = member.id, inline =  True)
	embed.set_thumbnail(url = member.avatar_url)
	embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
	await ctx.send(embed=embed)

@client.command()
async def meme(ctx, sub = "memes"):
	subreddit = reddit.subreddit(sub)
	r_asub = []
	top = subreddit.top(limit = 25)

	for submission in top:
		r_asub.append(submission)

	r_rsub = random.choice(r_asub)
	title = r_rsub.title
	image = r_rsub.url

	embed = discord.Embed(title =  title)
	embed.set_image(url = image)
	await ctx.send(embed = embed)
	
	
	
#Easter Egg :D
@client.command()
async def emoji(ctx):
	await ctx.send("😄")
	await ctx.send("<:PepeChrist:882924532963348480>")  #https://cdn.discordapp.com/emojis/882924532963348480.png
	await ctx.send("")



#Bot Runner
client.run(os.environ['bottok'])
