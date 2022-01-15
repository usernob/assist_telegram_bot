import pafy,re
from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from youtubesearchpython.__future__ import VideosSearch



@Client.on_inline_query(filters.regex(r'^(yts)\s+?(.+?\s*?)\s*?$'))
async def ytsearch_handler(bot,msg):
    result = []
    query = msg.matches[0].group(2)
    search = VideosSearch(query, limit = 10)
    videosResult = await search.next()
    for data in videosResult['result']:
        print('\n\n')
        print(data)
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
                            switch_inline_query = 'yts never gonna give you up'
                        ),
                        InlineKeyboardButton(
                            'watch on youtube',
                            url = data['link']
                        )
                    ]]
                )
            )
        )
    await msg.answer(results = result, cache_time = 10)