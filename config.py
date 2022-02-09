import os

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
sudo = [int(i) for i in os.environ['SUDO'].split(',')]
api_key = os.environ['API_KEY']
getme = []
print(sudo)

HELP = {}
