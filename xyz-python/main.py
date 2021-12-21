import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix = "+", description = "Bot de xyz#7980")

@bot.event
async def on_ready():
	print("Ready !")
 
def isPair(ctx):
    	return ctx.message.author.id % 2 == 0
 
@bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command()
@commands.check(isPair)
@commands.has_permissions(manage_messages = True)
async def pair(ctx):
	await ctx.send("Vous remplissez toute les conditions !")

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()

@bot.command()
async def bansId(ctx):
	ids = []
	bans = await ctx.guild.bans()
	for i in bans:
		ids.append(str(i.user.id))
	await ctx.send("La liste des id des utilisateurs bannis du serveur est :")
	await ctx.send("\n".join(ids))
 
@bot.command()
async def say(ctx, number, *texte):
	for i in range(int(number)):
		await ctx.send(" ".join(texte))

@bot.command()
async def getInfo(ctx, info):
	server = ctx.guild
	if info == "memberCount":
		await ctx.send(server.member_count)
	elif info == "numberOfChannel":
		await ctx.send(len(server.voice_channels) + len(server.text_channels))
	elif info == "name":
		await ctx.send(server.name)
	else:
		await ctx.send("Etrange... Je ne connais pas cela")
  
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")

  

bot.run("TOKEN")
