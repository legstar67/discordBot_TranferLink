import discord
from discord.ext import commands
import subprocess
from dotenv import load_dotenv
import os
import time 
from datetime import datetime
import requests


TOKEN_API_DISCORD = os.getenv("TOKEN_API_DISCORD") # Replace 'os.getenv("TOKEN_API_DISCORD")' by the token of your bot
trusted_users = [os.getenv("TRUSTED_USER")] # Remplacez 'os.getenv("TRUSTED_USER")' by the tag of your discord account
Starting_Link_Attachments = ["https://cdn.discordapp.com"]

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
        #  #DEBUG ---------
        # if (str(message.author) in trusted_users):
        #     await message.channel.send("DEBUG : '"+str(message.attachments[0])+"'")
        #     test = download_image(message.attachments[0],"testimage.jpg")
        #     imageFlow = open("black.jpg","rb")
        #     image = discord.File(fp=imageFlow,description="ceci est un test",filename="TestImage.jpg")

        #     await message.channel.send("My image is : ", file=image)
        #  #END DEBUG ---------

        
        if(isCommandCalledFromMessage(message,"test")):
            await message.channel.send("You are '" + str(message.author) + "'")
            await message.channel.send("the trusted user(s) are " + str(trusted_users) )


            
        elif (str(message.author) in trusted_users):
            # Open the link with firefox
            if(isCommandCalledFromMessageWithExceptions(message,"http",Starting_Link_Attachments)):
            
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


            elif(isCommandCalledFromMessage(message,Starting_Link_Attachments[0])):
                webLinkImage = message.attachments[0]
                today = datetime.today()
                fileName = f"botTranfer_{today.year}_{today.month}_{today.day}"
                sucess = download_image(webLinkImage,fileName)



        else:
            await message.channel.send("The bot doesn't trust you...")
    
    #debugging
        

        


# @client.command(name="sendtxt")
# async def text_phoneToPC(ctx):
#     text = ctx.message[]

def isCommandCalledFromMessage(message, prefix):
    if(len(message.attachments) > 0):
        msgContent = message.attachments[0]
    else:
        msgContent = message.content
        while msgContent[0] == ' ':
            msgContent = msgContent[1:]
    return str(msgContent).lower().startswith(prefix)

def isCommandCalledFromMessageWithExceptions(message, prefix, exceptions):
    for exception in exceptions:
        if(isCommandCalledFromMessage(message,exception)):
            return False
    else:
        return isCommandCalledFromMessage(message,prefix)

def download_image(url, file_name):
    # Send GET request to the URL
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        # Open file in binary write mode
        with open(file_name, 'wb') as file:
            # Write content to file
            file.write(response.content)
        return True
    return False

# # Example usage
# image_url = "https://example.com/image.jpg"
# file_name = "downloaded_image.jpg"
# success = download_image(image_url, file_name)

# Start the bot with the token
if __name__ == "__main__":
    #time.sleep(10)
    client.run(TOKEN_API_DISCORD)
