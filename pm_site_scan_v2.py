# NOTES AND STUFF>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>
# ONLY NEEDED ONCE: 
# c.execute('''CREATE TABLE articles (article_name text, datetime integer)''')
# #insert intitial values into database
# c.execute("INSERT INTO articles VALUES('first article', 1537392583)")
# conn.commit()
# >>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>

import sqlite3
import requests
import re
import time
from time import mktime
from datetime import datetime
from bs4 import BeautifulSoup
    

def get_title(media_item):
    # iterate through child elements of media item to get title
    children = media_item.descendants
    for child in children:
        if child.name == 'div' and child.get('class', '') == ['media-title']:
            latest_title = child.text
            return latest_title

def get_date(media_item):
    # iterate through child elements of media item to get date
    children = media_item.descendants
    for child in children:
        if child.name == 'div' and child.get('class', '') == ['media-date']:
            latest_date = child.text
            # convert date to datetime 
            format = '%d %b %Y'
            convert = time.strptime(latest_date, format)
            latest_datetime = int(mktime(convert))
            return latest_datetime

def check_db(title, datetime):
    c.execute('SELECT * FROM articles ORDER BY datetime DESC LIMIT 1')
    record = c.fetchone()
    if title == record[0] and datetime == record[1]:
        print('no update made')
        print(title + ' // ' + str(datetime))
        return False 
    else:
        c.execute("INSERT INTO articles VALUES (?, ?)", (latest_title, latest_datetime))
        conn.commit()
        # conn.close()
        print('table updated: ' + latest_title + ' @ ' + str(latest_datetime))
        return True        


# connect to database
<<<<<<< HEAD
<<<<<<< HEAD
conn = sqlite3.connect('pm_scan_v5.db')
=======
conn = sqlite3.connect('pm_scan_v12.db')
>>>>>>> parent of ed50ad3... Revert "Attempt to iterate through multiple pages"
=======
conn = sqlite3.connect('pm_scan_v7.db')
>>>>>>> parent of 347a938... Revert "Tweak for loop"
c = conn.cursor()
c.execute('''CREATE TABLE articles (article_name text, datetime integer)''')
# insert intitial values into database
c.execute("INSERT INTO articles VALUES('first article', 1537392583)")
conn.commit()

url = 'https://pm.gov.au/media'
<<<<<<< HEAD
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers)

# parse HTML, get latest article, check against database
soup = BeautifulSoup(response.text, "lxml")
latest = soup.find_all("div", class_="media-item")
article_count = 0

# iterate through the nine articles on the front page, check each against database
for i in range(9):
    latest_title = get_title(latest[article_count])
    latest_datetime = get_date(latest[article_count])
    db = check_db(latest_title, latest_datetime)
    if db:
        article_count += 1
    else:
        break
url_count = 0
while url_count <= 10: # <<< find a more elegant way to do this
    # open web page 
    url = url + '?page=' + str(url_count)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)

    # parse HTML, get latest article, check against database
    soup = BeautifulSoup(response.text, "lxml")
    latest = soup.find_all("div", class_="media-item")
    article_count = 0

    # iterate through the nine articles on the front page, check each against database
    for i in range(9):
        latest_title = get_title(latest[article_count])
        latest_datetime = get_date(latest[article_count])
        db = check_db(latest_title, latest_datetime)
        if db:
            article_count += 1
        # else:
        #     break
    
    url_count += 1
>>>>>>> parent of ed50ad3... Revert "Attempt to iterate through multiple pages"

# for item in next_latest:
#     next_latest_title = get_title(next_latest)
#     next_latest_datetime = get_date(next_latest)
#     print(next_latest_title, next_latest_datetime)

    # check_db(next_latest_title, next_latest_datetime)
    # print('loop ran ' + str(article_count) + ' times')
        





    



        

















