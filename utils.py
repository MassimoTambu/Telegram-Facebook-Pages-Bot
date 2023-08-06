import json, config

import telegram

from third_parties.facebook_scraper.facebook_scraper.fb_types import Post

def dumpPosts(posts: list[Post]):
   if config.DUMP: return
   fileName = "dump.json"
   # Clear file
   open(fileName, 'w').close()
   file = open(fileName, "a")
   file.write("[")
   for i, post in enumerate(posts):
      dump = json.dumps(post, indent=3, sort_keys=True, default=str)
      file.write(dump if len(posts) != i + 1 else dump + ",")
   file.write("]")
   file.close()

def createTelegramMessage(post: Post, pageName: str):
   post_text = telegram.helpers.escape_markdown(post['post_text'], version=2) if post['post_text'] else ''
   if post['shared_post_url'] is not None:
      shared_text = '_' + telegram.helpers.escape_markdown(post['shared_text'][post['shared_text'].find('\n', post['shared_text'].find('\n')+1)+2:], version=2) + '_' if post['shared_text'] else ''
      return '[{}]({})\nDate: {}\nComments: {}\n\n{}\n{}\n\n{}'.format(
         pageName,
         post['link'],
         str(post['time']),
         post['comments'],
         u'\U0001F501' + post['shared_username'],
         shared_text,
         post_text
      )

   return '[{}]({})\nDate: {}\nComments: {}\n\n{}'.format(
      pageName,
      post['link'],
      str(post['time']),
      post['comments'],
      post_text
   )
