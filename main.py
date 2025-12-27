import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

rol_peruano = "Holasi"

@bot.event
async def on_ready():
    print("UP")

@bot.event
async def on_member_join(member):
    await member.send(f"holasi bienvenido {member.name}") #mensaje al dm

@bot.event
async def on_message(message): # este es para leer 24/7 cada mensaje que se envia (mod)
    if message.author == bot.user:
        return

    if "mierda" in message.content.lower(): #palabra clave
        await message.delete()
        await message.channel.send(f"{message.author.mention} - tu mamá.")

    await bot.process_commands(message) #este es para q el bot pueda ejecutar otras cosas y no solo estar concentrado en los menmsajes que se envian todo el tiempo

@bot.command()
async def hola(ctx):
    await ctx.send(f"hola {ctx.author.mention}") #cmd1

@bot.command()
async def assign(ctx): #cmd2 ddar un rol
    role = discord.utils.get(ctx.guild.roles, name=rol_peruano)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} tiene el papu rol {rol_peruano}")
    else:
        await ctx.send("no existe ese rol pe")

@bot.command()
async def remove(ctx): #cmd3 te saca ese
    role = discord.utils.get(ctx.guild.roles, name=rol_peruano)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} teni el papu rol de {rol_peruano} y ay no lo tiene mas")
    else:
        await ctx.send("no existe perri")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f":{msg}") #dm de lo que agg al cmd

@bot.command()
async def reply(ctx): #uso de respuestas al mensaje
    await ctx.reply("holasi qpaso")

@bot.command()
async def poll(ctx, *, question): #poll
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(rol_peruano) #cmd con necesidad de rol
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!") ###

bot.run(token, log_handler=handler, log_level=logging.DEBUG)