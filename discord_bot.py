from datetime import date
from jinja2 import Undefined
import paramiko
import requests
import discord
import asyncio
import os
import json
from discord.ext.commands import Bot


intents = discord.Intents.default()
intents.members = True

bot = Bot(command_prefix = "!", intents=intents)


# ENV Variables
MAIN_CHANNEL_ID = int(os.getenv("DIS_MC_MAIN_CHANNEL_ID"))
HOSTNAME = os.getenv("DIS_MC_HOSTNAME")
USERNAME = os.getenv("DIS_MC_USERNAME")
PASSWORD = os.getenv("DIS_MC_PASSWORD")
TOKEN = os.getenv("DIS_MC_TOKEN")
SERVER_INFO_MESSAGE_ID = int(os.getenv("DIS_MC_SERVER_INFO_MESSAGE_ID"))

def isValidUsername(username):
    headers = {
        'Accept': 'application/json'
    }

    endpoint = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        req = requests.get(url=endpoint, headers=headers)
        data = req.json()
        # print(data)
        return True
    except:
        return False


def executeServerCommand(minecraftUsername):
    # initialize the SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=HOSTNAME, username=USERNAME, password=PASSWORD)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()

    # execute the command
    getContainerCommand = 'docker ps -qf "name=^k8s_vanillaminecraft_vanillaminecraft"'
    stdin, stdout, stderr = client.exec_command(getContainerCommand)
    container_id = stdout.read().decode()
    err = stderr.read().decode()
    if err:
        print(err)
    cmdCommand = f'docker exec -i {container_id.strip()} rcon-cli "whitelist add {minecraftUsername.strip()}"'
    stdin, stdout, stderr = client.exec_command(cmdCommand)
    output = stdout.read().decode()
    print(output)
    # print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print(err)

    # whitelist player command
    # cmdCommand = f'docker exec -i {container_id.strip()} rcon-cli "whitelist {playerName}"


@bot.event
async def on_ready():
    print("Guess who is ready!")


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    channel = bot.get_channel(MAIN_CHANNEL_ID)
    message = await channel.fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji)
    emoji = '✅'
    if message.id == SERVER_INFO_MESSAGE_ID:
        if (int(payload.user_id) == int(bot.user.id)):
                return
        else:
            if str(payload.emoji) == emoji:
                Role = discord.utils.get(payload.member.guild.roles, name="verified")
                if Role not in payload.member.roles:
                    try:
                        await payload.member.send(content="To get whitelisted, please reply in this chat with your Minecraft username.")
                    except:
                        print("Error sending message")
            await message.clear_reactions()
            await message.add_reaction('✅')

        

@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    main_channel = bot.get_channel(MAIN_CHANNEL_ID)
    if message.author == bot.user:
        return
    Role = discord.utils.get(main_channel.guild.roles, name="verified")
    server = bot.get_guild(main_channel.guild.id)
    member = server.get_member_named(message.author.name)
    if Role not in member.roles:
        isValid = isValidUsername(user_message)
        if not message.guild:
            if isValid == True:
                try:
                    Role = discord.utils.get(main_channel.guild.roles, name="verified")
                    server = bot.get_guild(main_channel.guild.id)
                    member = server.get_member_named(message.author.name)
                    executeServerCommand((str(user_message)))
                    await member.add_roles(Role)
                    await message.channel.send('Your username is valid and you have been whitelisted. Welcome to the server!')
                except:
                    print("Error")
            else:
                await message.channel.send('Not a valid username. Please respond with a valid username')


# Run the app in Discord.
bot.run(TOKEN)