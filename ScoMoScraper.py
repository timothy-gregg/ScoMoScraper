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


def get_url(media_item):
    children = media_item.descendants
    for child in children:
        if child.name == 'div' and child.get('class', '') == ['media-title']:
            for a in child:
                latest_url = a.get('href') 
                return latest_url



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

def check_db(title, datetime, content):
    c.execute('SELECT * FROM articles ORDER BY datetime DESC LIMIT 1')
    record = c.fetchone()
    if title == record[0] and datetime == record[1]:
        print('no update made')
        print(title + ' // ' + str(datetime))
        return False 
    else:
        c.execute("INSERT INTO articles VALUES (?, ?, ?)", (title, datetime, content))
        conn.commit()
        # conn.close()
        print('table updated: ' + latest_title + ' @ ' + str(latest_datetime))
        return True        


def read_page(href):
    url = 'https://pm.gov.au' + href
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    article = soup.find('article')
    return article.text




# TEMP ONLY: timestamp for database files
timeNow = time.time()

#create new database
conn = sqlite3.connect('ScoMoScraper_v1.db')
c = conn.cursor()
# TO DO: conditional logic, create table if no table else pass
c.execute('''CREATE TABLE articles (article_name text, datetime integer, article_content text)''')
# #insert intitial values into database
c.execute("INSERT INTO articles VALUES('first article', 1537392583, 'lorem ipsum dolor sit amet')")
conn.commit()


# open web page 
url = 'https://pm.gov.au/media'
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
    latest_content = read_page(get_url(latest[article_count]))

    db = check_db(latest_title, latest_datetime, latest_content)
    if db:
        article_count += 1
    else:
        break

