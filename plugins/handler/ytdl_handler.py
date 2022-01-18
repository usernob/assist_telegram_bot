from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from config import bot_token
from hashids import Hashids
from db import get_db_connection
import pafy
import utils
import sqlite3


hashid = Hashids(min_length=4, salt=bot_token)

MAX_SIZE = 2000000000

REGEX = '^(((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?)$'
apikey = 'AIzaSyBNj-YkGFByB0vmOQcMGPEtuFv2Ef0RTNk'

@Client.on_message(filters.regex(REGEX) | filters.regex(f'^\/start\s*?(\w+)?$'))
async def ytdl_handler(bot, msg):
    m1 = await msg.reply('Processing...')
    link = msg.matches[0].group(1)
    pafy.set_api_key(apikey)
    base = pafy.new(link)
    print(base)
    audio = base.audiostreams
    video = base.streams
    keyboard = []
    con = get_db_connection()
    for s in video:
        print(s.get_filesize())
        text = f'{s.resolution} - {utils.humansized(s.get_filesize())} - {s.extension}'
        if s.get_filesize() >= MAX_SIZE:
            keyboard.append([
                InlineKeyboardButton(
                    text,
                    url = s.url
                )
            ])
        else:
            url = s.url
            cursor = con.execute('INSERT INTO links (original_url,mime_type) VALUES (?,?)',(url,'video'))
            con.commit()
            row = cursor.lastrowid
            en = hashid.encode(row)
            print(en)
            keyboard.append([
                InlineKeyboardButton(
                    text,
                    callback_data = f'link = {en}'
                )
            ])
    for s in audio:
        text = f'{s.bitrate} - {utils.humansized(s.get_filesize())} - {s.extension}'
        if s.get_filesize() >= MAX_SIZE:
            keyboard.append([
                InlineKeyboardButton(
                    text,
                    url = s.url
                )
            ])
        else:
            url = s.url
            cursor = con.execute('INSERT INTO links (original_url,mime_type) VALUES (?,?)',(url,'audio'))
            con.commit()
            row = cursor.lastrowid
            en = hashid.encode(row)
            print(en)
            keyboard.append([
                InlineKeyboardButton(
                    text,
                    callback_data = f'link = {en}'
                )
            ])
    
    con.close()
    
    message = f'''
**{base.title}**

by {base.author}
at {base.published}
{base.viewcount:,} views
duration: {base.duration}
'''
    thumb = base.bigthumbhd or base.bigthumb or base.thumb
    print(thumb)
    await m1.edit_media(
        InputMediaPhoto(
            thumb,
            caption = message,
            parse_mode = 'markdown'
        ),
        reply_markup = InlineKeyboardMarkup(keyboard)
    )

@Client.on_callback_query(filters.regex('^link \= (.+?)$'))
async def test(bot,msg):
    con = get_db_connection()
    cur = con.cursor()
    cb = msg.matches[0].group(1)
    ori_id = hashid.decode(cb)[0]
    url = cur.execute('SELECT * FROM links WHERE id = (?)',(ori_id,)).fetchone()
    #print(tuple(url))
    file = url['original_url']
    mime_type = url['mime_type']
    con.close()
    if mime_type == 'video':
        await bot.send_video(msg.message.chat.id,file)
    elif mime_type == 'audio':
        await bot.send_audio(msg.message.chat.id,file)
    else:
        await bot.send_message(msg.message.chat.id,'something went worng i can fell it')