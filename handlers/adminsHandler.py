from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events
import asyncio, time
client = None
muteMembers = set()
handler_per = {}

async def getAdmins(chat):
    global admins
    admins = []
    async for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        admins.append(user.id)
    return admins

# async def startbot(event):
#     global startedBot
#     chat = await event.get_chat()
#     admins = await getAdmins(chat)
#     if event.from_id.user_id in admins:
#         await event.reply("╰┈➤\tتم التفعيل ✔👍⃤ \n Dev:@StaR0xf")
#         print(startedBot)
#         startedBot = 1
#         return startedBot
#     else:
#         await event.reply("مين انت ( ≖‿  ≖ )\nلازم ادمن 📢")
    
async def mute(event):  
    if handler_per["mute"]['per']:
        Reply = await event.get_reply_message()
        if Reply:
            if event.from_id.user_id in admins:
                if str(Reply.from_id.user_id) in muteMembers:
                    await event.reply("مهو مكتوم اساسا 🤦‍♂️")
                else:
                    muteMembers.add(str(Reply.from_id.user_id))
                    await event.reply("كتمتهولك يمعلم 😉")
            elif Reply.from_id.user_id in admins:
                await event.reply("متقدرش تكتم ادمن 😑🤐")
            else:
                await event.reply("مين انت ( ≖‿  ≖ )\nلازم ادمن 📢")

async def unMute(event):
    Reply = await event.get_reply_message()
    if Reply:
        if event.from_id.user_id in admins:
            try:
                muteMembers.remove(str(Reply.from_id.user_id))
                await event.reply("لغيت الكتم 👍")
            except:
                await event.reply("مش مكتوم اساسا")
        else:
            await event.reply("مين انت ( ≖‿  ≖ )\nلازم ادمن 📢")
       
async def again(event):
    if handler_per['again']['per']:
        if event.from_id.user_id in admins:
            chat = await event.get_chat()
            words = event.message.message.split(" ")
            for _ in range(int(words[-1])):
                await client.send_message(chat," ".join(words[1:-1]))
        else:
            await event.reply("مين انت ( ≖‿  ≖ )\nلازم ادمن 📢")
  
async def MentionAll(event):
    if handler_per['mentionAll']['per']:
        
        if event.from_id.user_id in admins:
            tes = ""
            group_entity = await event.get_chat()
            # Get all members from the group 
            async for member in client.iter_participants(group_entity):
                if(member.username != None):
                    tes += "@"+str(member.username)+'\n'
                    await client.send_message(group_entity, f"@{member.username}")
        else:
            await event.reply("مين انت ( ≖‿  ≖ )\nلازم ادمن 📢")
  
async def getBots(event):
    if handler_per['getBots']['per']:
        if event.from_id.user_id in admins:
            group_entity = await event.get_chat()
            bots = ""
            async for bot in client.iter_participants(group_entity):
                if bot.bot == 1:
                    bots +=  "@"+str(bot.username)+'\n'
            await client.send_message(group_entity, f"{str(bots)}")
        else:
            await event.reply("مين انت ( ≖‿  ≖ )\nلازم ادمن 📢")

async def delete_any_message(event):
    chat = await event.get_chat()
    await client.delete_messages(chat, [event.original_update.message.id])

async def close_group(event):
    global close_handler
    if event.from_id.user_id in admins:
        chat = await event.get_chat()
        await event.reply("تــم وقف الصداع عن هذا الجروب اللعين 🤞")
        close_handler = client.add_event_handler(delete_any_message, events.NewMessage(chats=chat))
    else:
        await event.reply("مين انت ( ≖‿  ≖ )\nلازم ادمن 📢")

async def open_group(event):
    if event.from_id.user_id in admins:
        client.remove_event_handler(delete_any_message)
        await event.reply("اهو فتحنا الجروب ورجعنا للزن😒")
    else:
        await event.reply("مين انت ( ≖‿  ≖ )\nلازم ادمن 📢")
