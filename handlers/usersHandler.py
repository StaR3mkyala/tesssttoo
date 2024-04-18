import random, os, requests, io
from gtts import gTTS
from pytube import YouTube
from telethon.tl.types import DocumentAttributeAudio
client = None
orders_words = '''
كتم ---> قم بالرد بها علي الرساله
الغاء كتم ---> قم بالرد بها علي الرساله
صوره ---> اكتب صوره + منشن للشخصي اللي عايز صورته
منشن الكل ---> لمنشن جميع الاعضاء معادا البوتات
كشف البوتات ---> يجلب لك جميع يوزرات البوتات في المجموعه
تكرار ---> قم بكتابره تكرار + الكلمه + عدد المرات
قفل الجروب ---> لمسح جميع الرسال اللتي سوف ترسل
فتح الجروب ---> لغلق امر قفل الجروب
------------ اوامر الضحك ------------
1- نسبه الذكاء
2- نسبه الحيونه
3- نسبه الانوثه
'''
handler_per = {}
async def welcome_message(event):
    welcome_list = ['نعم 🙄','عايز اي 😑','يعم بطل زننن 😤','تحت الخدمه 🧏‍♂️']
    choose_word = random.randint(0,len(welcome_list) - 1)
    await event.reply(welcome_list[choose_word])

async def getPhoto(event):
    chat = await event.get_chat()
    user = event.message.message.split(" ")
    photo = await client.download_profile_photo(user[-1])
    await client.send_file(chat, file=photo)
    os.remove(photo)

async def smart(event):
    if event.is_reply:
        # Get the replied-to message object
        replied_message = await event.get_reply_message()
        # Get the user entity of the sender of the replied-to message
        user = await replied_message.get_sender()
        chat = await event.get_chat()
    
        smartDegree = random.randint(0,100)
        await client.send_message(chat, f"نسبه الذكا للشخص : @{user.username}\n ➥{smartDegree}%")
    
async def animal(event):
    if event.is_reply:
        # Get the replied-to message object
        replied_message = await event.get_reply_message()
        # Get the user entity of the sender of the replied-to message
        user = await replied_message.get_sender()
        chat = await event.get_chat()
        animalDegree = random.randint(0,100)
        await client.send_message(chat, f"نسبه الحيونه للشخص : @{user.username}\n ➥{animalDegree}%")

async def woman (event):
    if event.is_reply:
        # Get the replied-to message object
        replied_message = await event.get_reply_message()
        # Get the user entity of the sender of the replied-to message
        user = await replied_message.get_sender()
        chat = await event.get_chat()
        womanDegree = random.randint(0,100)
        await client.send_message(chat, f"نسبه الانوثه للشخص : @{user.username}\n ➥{womanDegree}%")

async def menu(event):
    await event.reply(orders_words)

async def text_to_voice(event):
    if handler_per['text_to_voice']['per']:
        words = event.message.message.split(" ")
        tts = gTTS(text=" ".join(words[1:]), lang='ar')
        # Save the speech as an MP3 file
        path = "text.mp3"
        tts.save(path)
        print("Speech saved as output.mp3")
        await client.send_file(await event.get_chat(), path, thumb="test.jpg", caption=" ".join(words[1:]))

async def get_youtube_audio_bytes(video_url):
    # Create a YouTube object
    yt = YouTube(video_url)
    # Get the highest resolution audio stream
    stream = yt.streams.filter(only_audio=True).first()
    # Open a bytes IO stream to store audio bytes
    bytes_io = io.BytesIO()
    # Stream the audio and write it to the bytes IO stream
    stream.stream_to_buffer(bytes_io)
    # Get the bytes from the bytes IO stream
    audio_bytes = bytes_io.getvalue()
    result = io.BytesIO(audio_bytes)
    result.name = "audio.mp3"
    print(yt.thumbnail_url)
    req = requests.get(yt.thumbnail_url)
    if req.status_code == 200:
        # Get the bytes of the image
        image_bytes = req.content
    else:
        # If the request failed, print an error message
        print(f"Failed to fetch image from URL: {yt.thumbnail_url}")
    return result, yt, image_bytes

async def search_youtube(event):
    query = event.message.message.split(" ")
    getVideoId = requests.get(f'https://www.googleapis.com/youtube/v3/search?key=AIzaSyApdtGzPMGzDDNJRyRNaUMRCHqZ7HiBL2c&q={query[1:]}&type=video&part=snippet')
    video_url = f'https://www.youtube.com/watch?v={getVideoId.json()['items'][0]['id']['videoId']}'
    
    audio_bytes,yt, image_bytes = await get_youtube_audio_bytes(video_url)
    audio_attributes = [
        DocumentAttributeAudio(
            duration=yt.length,  # Fill in the duration of the audio in seconds if known
            title=getVideoId.json()['items'][0]['snippet']['title'],
            performer=getVideoId.json()['items'][0]['snippet']['channelTitle']
        )
    ]
    caption = f'عدد المشاهدات: {yt.views}\nالمطور: @StaR0xf'
    # Send the audio file with streaming
    await client.send_file(await event.get_chat(), file=audio_bytes, thumb=image_bytes, attributes=audio_attributes, caption=caption)
