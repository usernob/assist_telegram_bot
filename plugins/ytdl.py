from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from youtubesearchpython.__future__ import VideosSearch
from config import getme, sudo, bot_token, api_key
from hashids import Hashids
from db import get_db_connection
import utils
import pafy
import utils
import os

@Client.on_inline_query(filters.regex(r'^(yt)\s+?(.+?\s*?)\s*?$') & filters.user(sudo))
async def ytsearch_handler(bot,msg):
    result = []
    me = getme[0]
    query = msg.matches[0].group(2)
    search = VideosSearch(query, limit = 10)
    videosResult = await search.next()
    for data in videosResult['result']:
        #print('\n\n')
        #print(data)
        shortdesc = f"{data['publishedTime']} - {data['duration']}\n{data['viewCount']['short']}\n{data['descriptionSnippet'][0]['text'] if data['descriptionSnippet'] != None else 'None'}"
        pesan = f"{data['accessibility']['title']}\n[link]({data['link']})"
        result.append(
            InlineQueryResultArticle(
                title = data['title'],
                input_message_content = InputTextMessageContent(
                    pesan,
                    parse_mode = 'markdown'
                ),
                url = data["link"],
                thumb_url = data["thumbnails"][0]['url'],
                description = shortdesc,
                reply_markup = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            'watch on youtube',
                            url = data['link']
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            'download',
                            url = f'https://t.me/{me.username}?start={data["id"]}'
                        )
                    ]
                ])
            )
        )
        #print(f'https://t.me/{me.username}?start={data["id"]}')
    await msg.answer(results = result)

hashid = Hashids(min_length=4, salt=bot_token)

MAX_SIZE = 2000000000

REGEX = '^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)(?P<videoid>([\w\-]+)(\S+)?)$'
cached = {}

def get_stream(link):
    if link in cached:
        base = cached[link]
    else:
        base = pafy.new(link)
        cached[link] = base
        base = cached[link]
        if len(cached) == 4:
            enum = enumerate(cached)
            n = enum[0][1]
            cached.pop(n)
        else:
            pass
    return base
    
@Client.on_message(filters.regex(REGEX) | filters.regex(f'^\/start\s*?(?P<videoid>.+?)?$'))
async def ytdl_handler(bot, msg):
    m1 = await msg.reply('Processing...')
    link = msg.matches[0].group('videoid')
    pafy.set_api_key(api_key)
    base = get_stream(link)
    keyboard = []
    con = get_db_connection()
    print(cached)
    audio = base.audiostreams
    video = base.streams
    n = 0
    for s in video:
        print(s.get_filesize())
        url = s.url_https
        text = f'{s.resolution} - {utils.humansized(s.get_filesize())} - {s.extension}'
        if s.get_filesize() >= MAX_SIZE:
            keyboard.append([
                InlineKeyboardButton(
                    text,
                    url = url
                )
            ])
        else:
            cursor = con.execute('INSERT INTO links (download_url,youtube_id,mime_type) VALUES (?,?,?)',(url,link,'video'))
            con.commit()
            row = cursor.lastrowid
            en = hashid.encode(row)
            print(en)
            keyboard.append([
                InlineKeyboardButton(
                    text,
                    callback_data = f'link = {en} {n}'
                )
            ])
        n += 1
    n = 0
    for s in audio:
        url = s.url_https
        text = f'{s.bitrate} - {utils.humansized(s.get_filesize())} - {s.extension}'
        if s.get_filesize() >= MAX_SIZE:
            keyboard.append([
                InlineKeyboardButton(
                    text,
                    url = url
                )
            ])
        else:
            cursor = con.execute('INSERT INTO links (download_url,youtube_id,mime_type) VALUES (?,?,?)',(url,link,'audio'))
            con.commit()
            row = cursor.lastrowid
            en = hashid.encode(row)
            print(en)
            keyboard.append([
                InlineKeyboardButton(
                    text,
                    callback_data = f'link = {en} {n}'
                )
            ])
        n += 1
    con.close()
    
    message = f'''
**{base.title}**

by {base.author}
at {base.published}
{base.viewcount:,} | {utils.humandigit(base.viewcount)} views
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

def progress(current, total, msg):
    m = f"\ruploading {current * 100 / total:.1f}%"
    print(m)
    msg.edit_text(m)
    
class downprogres():
    def __init__(self,msg):
        self.msg = msg
    def __call__(self, total, recvd, ratio, rate, eta):
        m = f'{recvd * 100 / total:.1f} eta = {eta:.1f}'
        print(m, end = '\r')
        #msg.edit_text(m)
        

@Client.on_callback_query(filters.regex('^link \= (.+?) (\d)$'))
async def test(bot,msg):
    con = get_db_connection()
    cur = con.cursor()
    cb = msg.matches[0].group(1)
    n = int(msg.matches[0].group(2))
    ori_id = hashid.decode(cb)[0]
    url = cur.execute('SELECT * FROM links WHERE id = (?)',(ori_id,)).fetchone()
    file = url['download_url']
    print(file)
    yt_id = url['youtube_id']
    base = get_stream(yt_id)
    print(cached)
    #print(file)
    mime_type = url['mime_type']
    con.close()
    up = await bot.send_message(msg.message.chat.id,'uploading....')
    if mime_type == 'video':
        path = f'temp/{base.title}-{base.streams[n].resolution}.{base.streams[n].extension}'
        base.streams[n].download(
            filepath = path,
            quiet = True,
            progress = 'KB',
            callback = downprogres(up))
        await bot.send_video(msg.message.chat.id,file, progress=progress,progress_args = (up,))
        os.remove(path)
    elif mime_type == 'audio':
        path = f'temp/{base.title}-{base.streams[n].bitrate}.{base.streams[n].extension}'
        base.streams[n].download(
            filepath = path,
            quiet = True,
            callback = downprogres(up))
        await bot.send_audio(msg.message.chat.id,file, progress=progress,progress_args = (up,))
        os.remove(path)
    else:
        await bot.send_message(msg.message.chat.id,'something went worng i can fell it')
