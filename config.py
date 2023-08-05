import json

f = open('bot_data.json', 'r')
data = json.loads(f.read())
f.close()

TOKEN: str = data['token']
CHAT_ID: str = data['chat_id']
IS_DEBUG: bool = data['debug']
DUMP: bool = data['dump']
