from pyrogram import Client, filters
from config import bot_token,api_id,api_hash,sudo, getme, HELP
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import utils

bot = Client(
        "my_bot",
        api_id = api_id,
        api_hash = api_hash,
        bot_token = bot_token,
        plugins = dict(root = "plugins")
    )

with bot:
        me = bot.get_me()
        getme.append(me)

@bot.on_message(filters.regex('^(\/start)(\@.+?)?$'))
async def start(bot,msg):
    print(msg)
    await msg.reply(
        '\U0001f600 hello what can i help you?',
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    'try inline',
                    switch_inline_query_current_chat = ''
                )
            ]
        ])
    )



@bot.on_message(filters.regex('^(\/help)\s?(?P<args>.+?)?$'))
async def help_plugins(bot,msg):
    query = msg.matches[0].group('args')
    noargs = '''
Informasi tentang plugins yg tersedia
ketik `/plugins` untuk list plugins yg tersedia

usage:
    `/help <nama plugins>`

'''
    if query == None:
        await msg.reply(noargs, quote = True, parse_mode = 'markdown')
    else:
        try:
            pesan = HELP[query].format(username = getme[0].username)
        except:
            pesan = 'Tidak ada plugins dg nama tersebut'
        await msg.reply(pesan, quote = True, parse_mode = 'markdown')


@bot.on_message(filters.command('plugins'))
async def list_plugins(bot, msg):
    file = utils.get_plugins()
    pesan = f'''
Lokasi plugins : `{file.path}`
Total plugins : `{file.count}`
List plugins : \n
'''
    for i in file.namefile:
        pesan += f'`{i}` | '
    await msg.reply(pesan, quote = True, parse_mode = 'markdown')


    

if __name__ == '__main__':
    print('bot was running')
    bot.run()
