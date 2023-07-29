import json

f = open('bot_data.json', 'r')
data = json.loads(f.read())
f.close()
# insert your bot token between quotes
# RaccattaBot token
TOKEN = data['token']
# insert the tag of the channel where you want to send posts after the @
chat_id = data['chat_id']
