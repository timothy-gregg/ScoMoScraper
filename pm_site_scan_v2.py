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

# connect to database and create cursor
conn = sqlite3.connect('pm_scan.db')
c = conn.cursor()

# open web page and get first media item
url = 'https://pm.gov.au/media'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")
most_recent = soup.find("div", class_="media-item")


# iterate through child elements of media item to get title and date
children = most_recent.descendants
for child in children:
        if child.name == 'div' and child.get('class', '') == ['media-title']:
                latest_title = child.text
        elif child.name == 'div' and child.get('class', '') == ['media-date']:
                latest_date = child.text
                # convert date to datetime 
                format = '%d %b %Y'
                convert = time.strptime(latest_date, format)
                latest_datetime = int(mktime(convert))


# check these details against latest record in database
c.execute('SELECT * FROM articles ORDER BY datetime DESC LIMIT 1')
record = c.fetchone()
if latest_title == record[0] and latest_datetime == record[1]:
        pass # if no match, check next media-item on website
else:
        c.execute("INSERT INTO articles VALUES (?, ?)", (latest_title, latest_datetime))
        conn.commit()





#iterate through results and check published date
# for i in most_recent:
#     date = i['content']
#     print(date)
#     format = '%Y-%m-%dT%H:%M:%S+10:00'
#     convert = time.strptime(input, format)
#     article_date = int(mktime(convert))
#     dates = c.execute('SELECT datetime FROM articles ORDER BY datetime DESC LIMIT 1')
#     latest_saved = int(c.fetchone()[0])
#     if article_date > latest_saved:
        
        
        # c.execute("INSERT INTO articles VALUES('first article', 1537392583)")




  


        

















