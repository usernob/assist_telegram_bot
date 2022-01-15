import pafy
from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton,
                            InlineQueryResultVideo, InlineQueryResultAudio)
from youtubesearchpython.__future__ import VideosSearch



@Client.on_inline_query(filters.regex(r'^(yts)\s+?(.+?\s*?)\s*?$'))
async def ytsearch_handler(bot,msg):
    result = []
    query = msg.matches[0].group(2)
    search = VideosSearch(query, limit = 10)
    videosResult = await search.next()
    for data in videosResult['result']:
        #print('\n\n')
        #print(data)
        shortdesc = f"{data['publishedTime']} - {data['duration']}\n{data['viewCount']['short']}\n{data['descriptionSnippet'][0]['text'] if data['descriptionSnippet'] != None else 'None'}"
        pesan = f"{data['accessibility']['title']}\nlink {data['link']}"
        result.append(
            InlineQueryResultArticle(
                title = data['title'],
                input_message_content = InputTextMessageContent(
                    pesan
                ),
                url = data["link"],
                thumb_url = data["thumbnails"][0]['url'],
                description = shortdesc,
                reply_markup = InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            'download',
                            switch_inline_query_current_chat = f'ytdl {data["link"]}'
                        ),
                        InlineKeyboardButton(
                            'watch on youtube',
                            url = data['link']
                        )
                    ]]
                )
            )
        )
    await msg.answer(results = result)

toLarge = '''
Dikarenakan ukuran file ini melebihi 2 GB,
saya tidak bisa mengirim file dalam 
bentuk {types} karena pembatasan dari telegram, 
sebagai gantinya saya mengirimkan url yg bisa
anda download sendiri silahkan tekan tombol dibawah
'''

@Client.on_inline_query(filters.regex('^(ytdl)\s+?(((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?)$'))
async def ytdownload_handler(bot, msg):
    result = []
    query = msg.matches[0].group(2)
    base = pafy.new(query)
    stream = base.allstreams
    for s in stream:
        print(s)
        message = f'{s.quality} - {s.extension}\n{round(s.get_filesize()/1024/1024, 2)} MB'
        if s.mediatype == 'normal':
            if s.get_filesize() >= 2000000000:
                result.append(
                    InlineQueryResultArticle(
                        title = 'Video',
                        input_message_content = InputTextMessageContent(
                            toLarge.format(types = 'video')             
                        ),
                        description = message,
                        reply_markup = InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton(
                                    'download',
                                    url = s.url
                                )
                            ]]
                        )
                    )
                )
            else:
                result.append(
                    InlineQueryResultVideo(
                        video_url = s.url,
                        title = 'Video',
                        thumb_url = base.thumb,
                        description = message,
                        caption = message
                    )
                )
        elif s.mediatype == 'audio':
            if s.get_filesize() >= 2000000000:
                result.append(
                    InlineQueryResultArticle(
                        title = 'Audio',
                        input_message_content = InputTextMessageContent(
                            toLarge.format(types = 'audio')             
                        ),
                        description = message,
                        reply_markup = InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton(
                                    'download',
                                    url = s.url
                                )
                            ]]
                        )
                    )
                )
            else:
                result.append(
                    InlineQueryResultAudio(
                        audio_url = s.url,
                        title = 'Audio',
                        caption = message
                    )
                )
    await msg.answer(results = result)