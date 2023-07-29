# https://pypi.org/project/facebook-scraper/
#! If you scrape too much, Facebook might temporarily ban your IP.
from facebook_scraper import get_posts

#! USE https://github.com/VariabileAleatoria/Telegram-Facebook-Pages-Bot

from post import Post

FREE_YOUR_STUFF_CPH_FB_ID = '166464040076758'
# Is the description of the Facebook group
POST_GROUP_DESC_ID = '1851802798209532'

options = {
   "posts_per_page": 10,
   "comments": False,
   "progress": False
}

for postDict in get_posts(FREE_YOUR_STUFF_CPH_FB_ID, start_url="https://m.facebook.com/profile.php?id="+FREE_YOUR_STUFF_CPH_FB_ID, pages=10, cookies="cookies.txt", options=options):
   post = Post(postDict)
   # Skip group description
   if post.post_id == POST_GROUP_DESC_ID:
      continue

   
   if post.comments is not None:
      print('comments ' + str(post.comments))
