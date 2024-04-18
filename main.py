from telethon import TelegramClient, events
from handlers import adminsHandler, usersHandler
from telethon.tl.types import ChatAdminRights
from telethon.errors import ChatAdminRequiredError
import os, random, dotenv, re, time

dotenv.load_dotenv()
api_id = 23004811
api_hash = '1b1ec5c3c12509541bf99cf381de2bb9'
client = TelegramClient('session', api_id, api_hash)
client.start()
adminsHandler.client = client
usersHandler.client = client
muteMembers = adminsHandler.muteMembers
adminRights = 0
handler_per = {
    'mute': {
        'per': True,
        'close': 'قفل الكتم',
        'open': 'فتح الكتم'
    },
    'again': {
        'per': True,
        'close': 'قفل التكرار',
        'open': 'فتح التكرار'
    },
    'mentionAll': {
        'per': True,
        'close': 'قفل منشن الكل',
        'open': 'فتح منشن الكل'
    },
    'getBots': {
        'per': True,
        'close': 'قفل كشف البوتات',
        'open': 'فتح كشف البوتات'
    },
    'text_to_voice':{
        'per': True,
        'close': 'قفل قل',
        'open': 'فتح قل'
    }
}
adminsHandler.handler_per = handler_per
usersHandler.handler_per = handler_per
async def main(event):
    chat = await event.get_chat()
    admins = await adminsHandler.getAdmins(chat)
    user_id = event.message.from_id.user_id

    if str(user_id) in muteMembers:
        await client.delete_messages(chat, [event.original_update.message.id])
    if 'قفل' in event.message.message:
        if event.from_id.user_id in admins:
            for hanPer in handler_per:
                if handler_per[hanPer]['close'] == event.message.message:
                    handler_per[hanPer]['per'] = False
                    await event.reply(f"تم {event.message.message} 👍🐱‍🏍")
                    break
    elif 'فتح' in event.message.message:
        if event.from_id.user_id in admins:
            for hanPer in handler_per:
                if handler_per[hanPer]['open'] == event.message.message:
                    handler_per[hanPer]['per'] = True
                    
                    await event.reply(f"تم {event.message.message} 👍🐱‍🏍")
                    break
if __name__ == "__main__":
    print("Iam Work")
    client.add_event_handler(main, events.NewMessage())

    #----------------- Admins Controls -----------------#
    client.add_event_handler(adminsHandler.mute, events.NewMessage(pattern=r"^كتم$"))
    client.add_event_handler(adminsHandler.unMute, events.NewMessage(pattern=r"^الغاء كتم$"))
    client.add_event_handler(adminsHandler.again, events.NewMessage(pattern='تكرار'))
    client.add_event_handler(adminsHandler.MentionAll, events.NewMessage(pattern=r'^منشن الكل$'))
    client.add_event_handler(adminsHandler.getBots, events.NewMessage(pattern=r'^كشف البوتات$'))
    client.add_event_handler(adminsHandler.close_group, events.NewMessage(pattern=r'^قفل الجروب$'))
    client.add_event_handler(adminsHandler.open_group, events.NewMessage(pattern=r'^فتح الجروب'))

    #----------------- Users Controls -----------------#
    client.add_event_handler(usersHandler.getPhoto, events.NewMessage(pattern='صوره '))
    client.add_event_handler(usersHandler.smart, events.NewMessage(pattern=r"^نسبه الذكاء$"))
    client.add_event_handler(usersHandler.animal, events.NewMessage(pattern=r"^نسبه الحيونه$"))
    client.add_event_handler(usersHandler.woman, events.NewMessage(pattern=r"^نسبه الانوثه$"))
    client.add_event_handler(usersHandler.welcome_message, events.NewMessage(pattern=r'^ظورو$'))
    client.add_event_handler(usersHandler.menu, events.NewMessage(pattern=r'^اوامر$'))
    client.add_event_handler(usersHandler.text_to_voice, events.NewMessage(pattern=r'قل'))
    client.add_event_handler(usersHandler.search_youtube, events.NewMessage(pattern=r'بحث'))
    
    client.run_until_disconnected()
