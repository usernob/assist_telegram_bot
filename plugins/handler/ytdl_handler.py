from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot_token
from hashids import Hashids
import pafy
import utils
import sqlite3

def make_table():
    connection = sqlite3.connect('db_ytdl.db')
    
    connection.executescript('CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY AUTOINCREMENT,original_url TEXT NOT NULL)')
    
    connection.commit()
    connection.close()

def get_db_connection():
    conn = sqlite3.connect('db_ytdl.db')
    conn.row_factory = sqlite3.Row
    return conn

make_table()

hashid = Hashids(min_length=4, salt=bot_token)

MAX_SIZE = 2000000000

@Client.on_message(filters.regex('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'))
async def ytdl_handler(bot, msg):
    link = msg.text
    base = pafy.new(link)
    print(base)
    audio = base.audiostreams
    video = base.streams
    keyboard = []
    con = get_db_connection()
    for s in video:
        print(s)
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
            cursor = con.execute('INSERT INTO links (original_url) VALUES (?)',(url,))
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
        print(s)
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
            cursor = con.execute('INSERT INTO links (original_url) VALUES (?)',(url,))
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
{base.viewcount:,} views
duration: {base.duration}
'''
    await msg.reply_photo(
        photo = base.thumb,
        caption = message,
        parse_mode = 'markdown',
        reply_markup = InlineKeyboardMarkup(keyboard)
    )

@Client.on_callback_query()
async def test(bot,msg):
    print(msg)