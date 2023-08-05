import json, config

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
