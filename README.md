# Telegram-Facebook-Pages-Bot
Telegram bot which sends posts from a list of Facebook Pages to a Telegram channel.


## Usage
### Automatic setup
Just run `setup.py`

### Manual setup
Insert telegram bot token and the channel tag in the **config.py** file.  
Insert the FB pages you want to get posts from in a **pages.csv** file.  
The first line is needed and must be `page_name,page_tag,last_post_used`.  
The first column is the **page name**, you can set it to whatever you want but it will be the signature of the posts in every comment.  
The second name is the **page tag**, this must me the name of the page you can find in the URL with the broswer, this is what the bot actually needs to get posts from the pages.  
The last column is the **last post used**, that is the timestamp of the last post retrieved by the bot, and will be changed by it at runtime.  
**Be careful** to set it properly the first time, because the bot will try to retrieve all the posts which were published after that time.  
The timestamp format is '%Y-%m-%d %H:%M:%S' (example: 2019-09-07 19:38:29)  

## What's working
Right now the bot retrieves text posts and images (with gallery support), shares don't work.
### TODO
- video support can be implemented

## Module needed
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)  
[facebook-scraper](https://github.com/kevinzg/facebook-scraper)

## Example of pages.csv

```
page_name,page_tag,last_post_used
Facebook Page,facebook,2020-01-11 17:39:56
```
