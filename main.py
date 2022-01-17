from pyrogram import Client, filters
from config import bot_token,api_id,api_hash,sudo
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
bot = Client(
        "my_bot",
        api_id = api_id,
        api_hash = api_hash,
        bot_token = bot_token,
        plugins = dict(root = "plugins")
    )


@bot.on_message(filters.command('start'))
async def start(bot,msg):
    await msg.reply(
        'hello what can i help you?',
        reply_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                'download',
                switch_inline_query_current_chat = 'yts never gonna give you up'
            )
        ]])
    )
    
#@bot.on_message()
#async def allmsg(bot,msg):
#    if msg.from_user.id == sudo:
#        if msg.reply_to_message:
#            if msg.reply_to_message.forward_from:
#                await msg.copy(
#                    msg.reply_to_message.forward_from.id
#                )
#    else:
#        await msg.forward(sudo)


if __name__ == '__main__':
    print('bot has running')
    bot.run()