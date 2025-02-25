import discord
from discord.ext import commands
import subprocess
from dotenv import load_dotenv
import os

# Remplacez 'os.getenv("TOKEN_API_DISCORD")' par le token de votre bot
TOKEN_API_DISCORD = os.getenv("TOKEN_API_DISCORD")
trusted_users = [os.getenv("TRUSTED_USER")]

# Créez une instance de bot avec un préfixe de commande
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

client = discord.Client(intents=intents)
#bot = commands.Bot(command_prefix='', intents=intents)

# Événement lorsque le bot est prêt
@client.event
async def on_ready():
    print(f'Bot connecté en tant que {client.user}')

# Commande simple pour répondre "pong" à "ping"
#@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong \n')
    await ctx.send("the user is '" + str(ctx.author) + "'")


# Open the link with firefox
@client.event
async def on_message(message):
    if(message.content.lower().replace(" ", "").startswith("http")):
        if (str(message.author) in trusted_users):
            if(message.content.lower().replace(" ", "").startswith("https")):
                await message.channel.send("Link accepted, it will be opened on your computer")
                command = "firefox " + message.content
                subprocess.check_output(command, shell=True, text=True)
            else:
                await message.channel.send("Link refused")

        else:
            await message.channel.send("The bot doesn't trust you...")
    elif(message.content.lower() == "test"):
        await message.channel.send("You are '" + str(message.author) + "'")
        await message.channel.send("the trusted user(s) are " + str(trusted_users) )



# Lancez le bot avec le token
client.run(TOKEN_API_DISCORD)
