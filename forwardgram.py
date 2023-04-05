from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import yaml
import discord
import asyncio






message = []
message2 = []

with open('config.yml', 'rb') as f:
    config = yaml.safe_load(f)



"""
TELEGRAM CLIENT STUFF
"""
client = TelegramClient("forwardgram", config["api_id"], config["api_hash"])
client.start()

#Find input telegram channels
input_channels_entities = []
input_channels_entities2 = []

for d in client.iter_dialogs():
    if d.name in config["input_channel_names"]: #or d.entity.id in config["input_channel_id"]:
        input_channels_entities.append( InputChannel(d.entity.id, d.entity.access_hash) )

for d2 in client.iter_dialogs():
    if d2.name in config["input_channel_names2"]: #or d.entity.id in config["input_channel_id"]:
        input_channels_entities2.append( InputChannel(d2.entity.id, d2.entity.access_hash) )

if input_channels_entities == [] or input_channels_entities2 == []:
    print("No input channels found, exiting")
    exit()


#TELEGRAM NEW MESSAGE
@client.on(events.NewMessage(chats=input_channels_entities))
async def handler(event):
    # If the message contains a URL, parse and send Message + URL
    try:
        parsed_response = (event.message.message + '\n' + event.message.entities[0].url )
        parsed_response = ''.join(parsed_response)
    # Or we only send Message    
    except:
        parsed_response = event.message.message

    globals()['message'].append(parsed_response)

@client.on(events.NewMessage(chats=input_channels_entities2))
async def handler(event):
    # If the message contains a URL, parse and send Message + URL
    try:
        parsed_response2 = (event.message.message + '\n' + event.message.entities[0].url )
        parsed_response2 = ''.join(parsed_response2)
    # Or we only send Message    
    except:
        parsed_response2 = event.message.message

    globals()['message2'].append(parsed_response2)



"""
DISCORD CLIENT STUFF
"""
discord_client = discord.Client()

async def background_task():
    global message
    global message2
    await discord_client.wait_until_ready()
    discord_channel = discord_client.get_channel(config["discord_channel"])
    discord_channel2 = discord_client.get_channel(config["discord_channel2"])
    
    while True:
        if message != [] and message != [''] and message[0] != "" and message2 == []:
            
            
            print(message)
            await discord_channel.send(message[0])
            message.pop(0)
            
        
        elif  message2 != [] and message2 != [''] and message2[0] != "" and message == []:
            print(message2)
            await discord_channel2.send(message2[0])
            message2.pop(0)

        else:
            
            message = []
            message2 = []    
        await asyncio.sleep(0.1)

discord_client.loop.create_task(background_task())



"""
RUN EVERYTHING ASYNCHRONOUSLY
"""

print("Listening now")
asyncio.run( discord_client.run(config["discord_bot_token"]) )
asyncio.run( client.run_until_disconnected() )
