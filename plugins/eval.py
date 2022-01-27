from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import sudo
import utils


@Client.on_message(filters.command('eval') & filters.user(sudo))
def eval_python(bot,msg):
    print(msg.text)
    code = msg.text.replace('/eval', '')
    print(code)
    test = eval(code)
    print(test)