class Post:
   def __init__(self, dict):
      self.dict = dict
      self.post_id = dict['post_id']
      self.text = dict['text']
      self.post_text = dict['post_text']
      self.shared_text = dict['shared_text']
      self.original_text = dict['original_text']
      self.time = dict['time']
      self.timestamp = dict['timestamp']
      self.image = dict['image']
      self.image_lowquality = dict['image_lowquality']
      self.images = dict['images']
      self.images_description = dict['images_description']
      self.images_lowquality = dict['images_lowquality']
      self.images_lowquality_description = dict['images_lowquality_description']
      self.video = dict['video']
      self.video_duration_seconds = dict['video_duration_seconds']
      self.video_height = dict['video_height']
      self.video_id = dict['video_id']
      self.video_quality = dict['video_quality']
      self.video_size_MB = dict['video_size_MB']
      self.video_thumbnail = dict['video_thumbnail']
      self.video_watches = dict['video_watches']
      self.video_width = dict['video_width']
      self.likes = dict['likes']
      self.comments = dict['comments']
      self.shares = dict['shares']
      self.post_url = dict['post_url']
      self.link = dict['link']
      self.links = dict['links']
      self.user_id = dict['user_id']
      self.username = dict['username']
      self.user_url = dict['user_url']
      self.is_live = dict['is_live']
      self.factcheck = dict['factcheck']
      self.shared_post_id = dict['shared_post_id']
      self.shared_time = dict['shared_time']
      self.shared_user_id = dict['shared_user_id']
      self.shared_username = dict['shared_username']
      self.shared_user_url = dict['shared_user_url']
      self.shared_post_url = dict['shared_post_url']
      self.available = dict['available']
      self.comments_full = dict['comments_full']
      self.reactors = dict['reactors']
      self.w3_fb_url = dict['w3_fb_url']
      self.reactions = dict['reactions']
      self.reaction_count = dict['reaction_count']
      self.withKey = dict['with']
      self.page_id = dict['page_id']
      self.sharers = dict['sharers']
      self.translated_text = dict['translated_text']
      self.image_id = dict['image_id']
      self.image_ids = dict['image_ids']
      self.was_live = dict['was_live']
      self.header = dict['header']

   def printAll():
      print(dict)

   def getPostUrl(self):
      # According to the library author, this field could be None
      if self.post_url is not None:
         return self.post_url
      return 'https://www.facebook.com/' + self.post_id

   # TODO add Telegram bot code
   def toTelegramPost(self):
      return {
         'body': self.post_text,
         'url': self.getPostUrl(),
         'images': self.images,
         'comments_count': self.comments,
         'time': self.time,
         'username': self.username,
      }
