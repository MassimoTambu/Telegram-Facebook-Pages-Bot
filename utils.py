import json, config

import telegram

from third_parties.facebook_scraper.facebook_scraper.fb_types import Post

def dumpPosts(posts: list[Post]):
   if config.DUMP == False: return
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
   post_text = post['post_text'] if post['post_text'] else ''
   if post['shared_post_url'] is not None:
      shared_text = '_' + post['shared_text'][post['shared_text'].find('\n', post['shared_text'].find('\n')+1)+2:] + '_' if post['shared_text'] else ''
      return '[{}]({})\n'.format(pageName, post['post_url']) + telegram.helpers.escape_markdown(
         'Date: {}\nComments: {}\n\n{}\n{}\n\n{}'
         .format(
            str(post['time']),
            post['comments'],
            u'\U0001F501' + post['shared_username'],
            shared_text,
            post_text
         ),
      version=2)

   return '[{}]({})\n'.format(pageName, post['post_url']) + telegram.helpers.escape_markdown(
      'Date: {}\nComments: {}\n\n{}'.format(
         str(post['time']),
         post['comments'],
         post_text
      ),
   version=2)
