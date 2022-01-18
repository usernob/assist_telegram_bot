from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton


@Client.on_message(filters.regex('^(\/start)(\@.+?)?$'))
async def start(bot,msg):
    print(msg)
    await msg.reply(
        'hello what can i help you?',
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    'try inline',
                    switch_inline_query_current_chat = ''
                )
            ]
        ])
    )
    