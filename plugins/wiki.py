import wikipedia as wiki
from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)
import utils
from config import sudo, getme, HELP

@Client.on_inline_query(filters.regex(r'^(wiki)\s+?(.+?\s*?)\s*?(-y)?$') & filters.user(sudo))
async def wiki_handler(bot,msg):
    result = []
    query = msg.matches[0].group(2)
    wiki.set_lang('id')
    wikilist = wiki.search(query,results = 5)
    for key in wikilist:
        url = 'https://id.wikipedia.org/wiki/' + key.replace(' ','_')
        result.append(
            InlineQueryResultArticle(
                title = key,
                input_message_content = InputTextMessageContent(
                    url
                ),
                description = url,
                reply_markup = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            'Summary',
                            callback_data = f'wiki {key.replace(" ", "_")}'
                        )
                    ]
                ])
            )
        )
    if result == []:
        info = 'sorry no results'
    else:
        info = ''
    await msg.answer(
        results = result,
        switch_pm_text = info,
        switch_pm_parameter = 'start',
    )
    
@Client.on_callback_query(filters.regex("(wiki)\s(.+?)$"))
async def wiki_btn(bot, msg):
    query = msg.matches[0].group(2)
    page = wiki.page(query)
    message = f'**{page.title}**\n\n{wiki.summary(query)}\n[link]({utils.encode_url(page.url)})'
    await msg.edit_message_text(message, parse_mode = 'markdown')


HELP[utils.filename(__file__)] = '''
Search wikipedia 

usage:
    `/wiki <query>`

inline:
    `@{username} wiki <query>`


'''
