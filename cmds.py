import sys
import json

# Command object used to call commands.
cmds={
    "cmd":lambda midf,message,client: cmd(midf,message,client),
    "serverstat":lambda midf,message,client: serverstat(midf,message,client),
    "template":lambda midf,message,client: template(midf,message,client)
} 

# Description object
desc={
    "cmd":"evaluate command sent by bot admin.",
    "serverstat":"Display server member status.",
    "template":"be copy/pasted."
}

# Read in data.json
data=json.loads(open("data.json","r").read())

# Standard interface to run commands through.
async def run_command(midf,message,client):
    command = message.content.split(' ')[0]
    if message.content.lower() == "?hello there":
        await message.channel.send("General kenobi!")
    else:
        try:
            await cmds[command[1:]](midf,message,client).cmd()
        except:
            e = sys.exc_info()
            errmsg=f"Error: {e}"
            print(errmsg)
        
# -------------------- command classes and their functions --------------------

class cmd(): # Use: evaluate command sent by bot admin.
    def __init__(self,midf,message,client):
        self.name=type(self).__name__
        self.message=message
        self.client=client
        self.midf=midf
        self.command=self.message.content[len(self.midf)+len(self.name):]
        self.args=self.command.split(' ')
    
    async def cmd(self):
        if self.message.author.id == data["ownerid"]:
            await eval(self.command)
        else:
            await self.message.channel.send("Access denied.")

class serverstat(): # Get server members status.
    def __init__(self,midf,message,client):
        self.name=type(self).__name__
        self.message=message
        self.client=client
        self.midf=midf
        self.command=self.message.content[len(self.midf)+len(self.name):]
        self.args=self.command.split(' ')
        
    async def cmd(self):
        online, idle, do_not_disturb, offline = self.community_report(self.message.guild)
        await self.message.channel.send(f"```Online: {online}.\nIdle: {idle}.\nDo not disturb: {do_not_disturb}.\nOffline: {offline}.```")

    def community_report(self,guild):
        online = 0
        idle = 0
        do_not_disturb = 0
        offline = 0
        
        for m in guild.members:
            if m.bot==False:
                if str(m.status) == "idle":
                    idle += 1
                elif str(m.status) == "dnd":
                    do_not_disturb += 1
                elif str(m.status) == "online":
                    online += 1
                else:
                    offline += 1
        return online, idle, do_not_disturb, offline


class template(): # Template class with basic data structure.
    def __init__(self,midf,message,client):
        self.name=type(self).__name__
        self.message=message
        self.client=client
        self.midf=midf
        self.command=self.message.content[len(self.midf)+len(self.name):]
        self.args=self.command.split(' ')
        
    async def cmd(self):
        await self.message.channel.send("An unexpected command for sure, But a welcome one.")