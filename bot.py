import discord
from discord.ext import commands
import subprocess
from dotenv import load_dotenv
import os
import time 


TOKEN_API_DISCORD = os.getenv("TOKEN_API_DISCORD") # Replace 'os.getenv("TOKEN_API_DISCORD")' by the token of your bot
trusted_users = [os.getenv("TRUSTED_USER")] # Remplacez 'os.getenv("TRUSTED_USER")' by the tag of your discord account


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True

#client = discord.Client(intents=intents, command_prefix = '!')
client = commands.Bot(command_prefix='!', intents=intents)

# Executed when the bot launches and is ready
@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')

# first command to test
#@bot.command(name='ping')
#async def ping(ctx):
#    await ctx.send('pong \n')
#    await ctx.send("the user is '" + str(ctx.author) + "'")


############# for debuging
#import logging

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
#################


@client.event
async def on_message(message):
    #logger.info(f"Message reçu: {message.content}") ####### TODO for debuging

   
    if(not message.author.bot):
        if(isCommandCalledFromMessage(message,"test")):
            await message.channel.send("You are '" + str(message.author) + "'")
            await message.channel.send("the trusted user(s) are " + str(trusted_users) )


            
        elif (str(message.author) in trusted_users):
            # Open the link with firefox
            if(isCommandCalledFromMessage(message,"http")):
            
                if(message.content.lower().replace(" ", "").startswith("https")):
                    #try:
                    await message.channel.send("Link accepted, it will be opened on your computer")
                    command = "firefox " + message.content
                    subprocess.Popen(command, shell=True)
                        #result = subprocess.run(command, shell=True, text=True, capture_output=True)
                        #logger.info(f"Command output: {result.stdout}")
                        #if result.stderr:
                        #    logger.error(f"Command error: {result.stderr}")
                    #except subprocess.CalledProcessError as e:
                    #    await message.channel.send(f"Error by opening the link : {e}")
                    await message.channel.send("Link Opened !")
                    
                else:
                    await message.channel.send("Link refused")
            
            # Copy txt, everything after ".c ", from discord to the clipboard (and send a notification on the PC )
            elif(isCommandCalledFromMessage(message,".c ")):
            
                txt = message.content[len(".c "):]
                print("Try to copy on the computer the txt is '"+ txt + "'")

                commandForCopying = 'echo "' + txt + '" | xsel --clipboard --trim' #--trim removes the '\n' at the end of the new txt on the clipboard, which is by default
                commandForSendingNotification = 'notify-send --urgency=normal --app-name="Tranfer bot" "You just received a new text in your Clipboard !"'
                subprocess.Popen(commandForCopying, shell=True)
                subprocess.Popen(commandForSendingNotification, shell=True)
            
            # receive the content from the clipboard
            elif(isCommandCalledFromMessage(message,".v")):
                command = "xsel --clipboard --output"
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output = process.stdout.readline()
                await message.channel.send( "```INFO : Nothing is in the clipboard```" if output.replace(" ","") == "" else output) #TODO solve the case when outputs overflows the 2000 characters limit from discord




        else:
            await message.channel.send("The bot doesn't trust you...")

        


# @client.command(name="sendtxt")
# async def text_phoneToPC(ctx):
#     text = ctx.message[]

def isCommandCalledFromMessage(message, prefix):
    while message[0] == ' ':
        message = message[1:]
    return message.content.lower().startswith(prefix)

# Start the bot with the token
if __name__ == "__main__":
    #time.sleep(10)
    client.run(TOKEN_API_DISCORD)
