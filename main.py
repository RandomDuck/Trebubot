import discord
import logging
import datetime
import json
import cmds

# mått felix 12 11 10
# setup logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=f'./logs/discord_{datetime.datetime.now().date()}.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Read token, botversion and midf from a json "data" file
data=json.loads(open("data.json","r").read())
botversion = data["botversion"]
token = data["token"]  
midf = data["cmdMod"]

# starts the discord client.
client = discord.Client()  

@client.event  # event decorator/wrapper. More on decorators here: https://pythonprogramming.net/decorators-intermediate-python-tutorial/
async def on_ready():  # method expected by client. This runs once when connected
    
    # notification of login.
    print(f'''
    Connected: logged in as {client.user}
    Running discord.py version: {discord.__version__}
    Running Trebubot version: {botversion}
    ''')  

@client.event
async def on_message(message):  # event that happens per any message.

    # get and format date and time and then output to log.
    dt=datetime.datetime.now() 
    date=dt.date()
    time=dt.time().strftime("%H:%M:%S")
    v=message.attachments[0]
    print(v.url)
    print(str(v.filename))
    # print(f"""
    #     Title: {message.embeds[0].title}
    #     Desc: {message.embeds[0].description}
    #     Author: {message.embeds[0].author.name}
    #     url: {message.embeds[0].url}
    #     color hex: {message.embeds[0].color}
    #     footer: {message.embeds[0].footer.text}
    #     image url: {message.embeds[0].image.url}
    #     Fields: {message.embeds[0].fields}
    #     """)

    

    open(f"./logs/{message.guild.name}.log","a").write(f"{message.guild.name} [{message.channel}]: {date}[{time}]: {message.author}({message.author.name}): {message.content}\n")
    
    # check if a command was called then run it.
    if message.content[0:len(midf)]==midf:
       await cmds.run_command(midf,message,client) 

# Initiate loop. (placed att absolute bottom)
client.run(token)