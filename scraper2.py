#!/usr/bin/env python3

from typing import Any
import telegram, threading
from facebook_scraper import get_posts
from datetime import datetime
import csv
from tempfile import NamedTemporaryFile
import shutil
import config
import time
import sys
import traceback
import logging
import config
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ExtBot, Application, CallbackContext, JobQueue

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

fields = ['page_name', 'page_tag', 'last_post_used']

CHAT_ID = config.CHAT_ID
WAIT_SECONDS = 600

async def check(context: ContextTypes.DEFAULT_TYPE):
    with open('pages.csv', mode='r+') as csv_file, NamedTemporaryFile(mode='w', delete=False) as tempfile:
        csv_reader = csv.DictReader(csv_file)
        csv_writer = csv.DictWriter(tempfile, fields)
        csv_writer.writeheader()
        for page in csv_reader:
            try:
                # https://github.com/kevinzg/facebook-scraper/issues/990
                posts = list(get_posts(page['page_tag'], start_url="https://m.facebook.com/profile.php?id="+page['page_tag'], pages=2, cookies='cookies.txt'))
            except OSError as err:
                print("Got an exception while trying to retrieve posts")
                traceback.print_exc()
                if err.errno == 101 or err.errno == 500:
                    print("Network unreachable, waiting 5 minutes")
                    time.sleep(300)
                    break
                else:
                    sys.exit()
            posts.sort(key = lambda x: int(x['post_id']))
            for post in posts:
                if int(post['post_id']) <= int(page['last_post_used']): # post already sent to channel
                    continue
                post_text = telegram.helpers.escape_markdown(post['post_text'], version=2) if post['post_text'] else ''
                if post['shared_post_url'] is not None:
                    shared_text = '_' + telegram.helpers.escape_markdown(post['shared_text'][post['shared_text'].find('\n', post['shared_text'].find('\n')+1)+2:], version=2) + '_' if post['shared_text'] else ''
                    message = u'\U0001F501' + ' ' + post['shared_username'] + '\n' + shared_text + '\n\n' + post_text + '\n[' + page['page_name'] + '](https://www.facebook.com/groups/' + page['page_tag'] + ')'
                else:
                    message = post_text + '\n[' + page['page_name'] + ']'
                if post['images'] is not None and len(post['images']) > 0:
                    images = [telegram.InputMediaPhoto(post['images'][0], caption=message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)]
                    for image in post['images'][1:]:
                        images.append(telegram.InputMediaPhoto(image))
                    print("SEND IMAGE")
                    await application.bot.send_media_group(CHAT_ID, images)
                elif post['video'] is not None:
                    print("SEND VIDEO")
                    await application.bot.send_video(CHAT_ID, post['video'], caption=message)
                elif post['text'] is not None:
                    print("SEND MESSAGE")
                    await application.bot.send_message(CHAT_ID, message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
            if len(posts) != 0: 
                # according to facebook-scraper devs you can get 0 posts if
                # you get temporarily ip banned for too many requests 
                page['last_post_used'] = posts[-1]['post_id']
            row = {'page_name': page['page_name'], 'page_tag': page['page_tag'], 'last_post_used': page['last_post_used']}
            csv_writer.writerow(row)
    shutil.move(tempfile.name, 'pages.csv')

if __name__ == '__main__':
    application: Application[ExtBot, CallbackContext, Any, Any, Any, JobQueue] = ApplicationBuilder().token(config.TOKEN).build()
    if application.job_queue is not None:
        # application.job_queue.run_repeating(callback=check, interval=10)
        application.job_queue.run_once(callback=check, when=1)
    else:
        raise Exception('job_queue is none. Bot will not start without the task scheduler')
    
    application.run_polling()
