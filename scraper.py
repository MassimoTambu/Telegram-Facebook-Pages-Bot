#!/usr/bin/env python3

import telegram, csv, shutil, time, sys, traceback, logging

from config import IS_DEBUG, CHAT_ID, TOKEN
from utils import createTelegramMessage, dumpPosts
from third_parties.facebook_scraper.facebook_scraper import get_posts
from third_parties.facebook_scraper.facebook_scraper.exceptions import TemporarilyBanned

from typing import Any
from tempfile import NamedTemporaryFile
from telegram.ext import ApplicationBuilder, ContextTypes, ExtBot, Application, CallbackContext, JobQueue

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if IS_DEBUG else logging.INFO
)

fields = ['page_name', 'page_tag', 'last_post_used']

async def check(_: ContextTypes.DEFAULT_TYPE):
    with open('pages.csv', mode='r+') as csv_file, NamedTemporaryFile(mode='w', delete=False) as tempfile:
        csv_reader = csv.DictReader(csv_file)
        csv_writer = csv.DictWriter(tempfile, fields)
        csv_writer.writeheader()
        for page in csv_reader:
            try:
                # https://github.com/kevinzg/facebook-scraper/issues/990
                posts = list(get_posts(
                        group=page['page_tag'],
                        start_url="https://m.facebook.com/profile.php?id="+page['page_tag'],
                        pages=1,
                        timeout=10,
                        cookies='cookies/cookies.txt',
                        options={"allow_extra_requests": True}
                    )
                )
                logging.info("number of posts: " + str(len(posts)))
            except TemporarilyBanned:
                logging.warning("We have been temporarily banned. Changing cookie..")
                #TODO
                sys.exit()
            except OSError as err:
                logging.warning("Got an exception while trying to retrieve posts")
                traceback.print_exc()
                if err.errno == 101 or err.errno == 500:
                    logging.warning("Network unreachable, waiting 5 minutes")
                    time.sleep(300)
                    break
                else:
                    sys.exit()
            posts.sort(key = lambda x: int(x['post_id']))

            dumpPosts(posts)
            #! https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this (no more than 20 message per minute on the same group)
            for post in posts:
                if int(post['post_id']) <= int(page['last_post_used']): # post already sent to channel
                    logging.info('No new posts!')
                    continue
                message = createTelegramMessage(post, page['page_name'])
                if post['images'] is not None and len(post['images']) > 0:
                    images = [telegram.InputMediaPhoto(post['images'][0], caption=message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)]
                    for image in post['images'][1:]:
                        images.append(telegram.InputMediaPhoto(image))
                    logging.debug("SEND IMAGE")
                    try:
                        await application.bot.send_media_group(
                            CHAT_ID,
                            images,
                            read_timeout = 5,
                            write_timeout = 20, # Default is already 20
                            connect_timeout = 5,
                            pool_timeout = 5
                        )
                    except Exception as err:
                        logging.warning(err)
                elif post['images_lowquality'] is not None and len(post['images_lowquality']) > 0:
                    images = [telegram.InputMediaPhoto(post['images_lowquality'][0], caption=message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)]
                    for image in post['images_lowquality'][1:]:
                        images.append(telegram.InputMediaPhoto(image))
                    logging.debug("SEND LOW QUALITY IMAGE")
                    try:
                        await application.bot.send_media_group(
                            CHAT_ID,
                            images,
                            read_timeout = 5,
                            write_timeout = 20, # Default is already 20
                            connect_timeout = 5,
                            pool_timeout = 5
                        )
                    except Exception as err:
                        logging.warning(err)
                elif post['video'] is not None:
                    try:
                        logging.debug("SEND VIDEO")
                        await application.bot.send_video(CHAT_ID, post['video'], caption=message)
                    except Exception as err:
                        logging.warning(err)
                elif post['text'] is not None:
                    logging.debug("SEND MESSAGE")
                    try:
                        await application.bot.send_message(CHAT_ID, message, parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
                    except Exception as err:
                        logging.warning(err)
            if len(posts) != 0: 
                # according to facebook-scraper devs you can get 0 posts if
                # you get temporarily ip banned for too many requests 
                page['last_post_used'] = posts[-1]['post_id']
            row = {'page_name': page['page_name'], 'page_tag': page['page_tag'], 'last_post_used': page['last_post_used']}
            csv_writer.writerow(row)
    shutil.move(tempfile.name, 'pages.csv')

if __name__ == '__main__':
    application: Application[ExtBot, CallbackContext, Any, Any, Any, JobQueue] = ApplicationBuilder().token(TOKEN).build()
    if application.job_queue is not None:
        application.job_queue.run_repeating(callback=check, interval=60, first=1)
    else:
        raise Exception('job_queue is none. Bot will not start without the task scheduler')
    
    application.run_polling()
