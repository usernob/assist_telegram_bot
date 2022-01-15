import wikipedia as wiki
from pyrogram import Client, filters
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)


@Client.on_inline_query(filters.regex(r'^(wiki)\s+?(.+?\s*?)\s*?(-y)?$'))
async def wiki_handler(bot,msg):
    result = []
    query = msg.matches[0].group(2)
    wiki.set_lang('id')
    print(query)
    if msg.matches[0].group(3) != None:
        page = wiki.page(query)
        pesan = f'{page.title}\n\n{wiki.summary(query, auto_suggest = True)}\n\n{page.url}'
        result.append(
            InlineQueryResultArticle(
                title = query,
                input_message_content = InputTextMessageContent(
                    pesan
                ),
                url = page.url,
                description = page.content
            )
        )
    else:
        wikilist = wiki.search(query,results = 5)
        for key in wikilist:
            url = 'https://id.wikipedia.org/wiki/' + key.replace(' ','_')
            result.append(
                InlineQueryResultArticle(
                    title = key,
                    input_message_content = InputTextMessageContent(
                        url
                    ),
                    description = url
                )
            )
    await msg.answer(
        results = result,
        cache_time = 10
    )
    
