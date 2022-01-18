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



#@bot.on_message()
#async def allmsg(bot,msg):
#    print(msg)
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