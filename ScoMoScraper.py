import sqlite3 # for saving data in an SQLite database
import requests # for making http requests to the PM's website
import time # for converting dates and times to a standardised format
from time import mktime
from datetime import datetime
from bs4 import BeautifulSoup # for parsing HTML and extracting data


# the following functions extract important data from a new post on the PM's website...

# extract the title 
def get_title(media_item):
    children = media_item.descendants
    for child in children:
        if child.name == 'div' and child.get('class', '') == ['media-title']:
            latest_title = child.text
            return latest_title

# extract the URL   
def get_url(media_item):
    children = media_item.descendants
    for child in children:
        if child.name == 'div' and child.get('class', '') == ['media-title']:
            for a in child:
                latest_url = a.get('href') 
                return latest_url

# extract the date, convert it to datetime   
def get_date(media_item):
    children = media_item.descendants
    for child in children:
        if child.name == 'div' and child.get('class', '') == ['media-date']:
            latest_date = child.text
            format = '%d %b %Y'
            convert = time.strptime(latest_date, format)
            latest_datetime = int(mktime(convert))
            return latest_datetime

# check the database to see if latest article is already saved; if not, save it
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

# open the page of the latest artice, parse its contents
def read_page(href):
    url = 'https://pm.gov.au' + href
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find('article')
    return article.text

#create new database
conn = sqlite3.connect('ScoMoScraper.db')
c = conn.cursor()

# check if database table has already been created; if not, create it
try:
    c.execute('''CREATE TABLE articles (article_name text, datetime integer, article_content text)''')
except:
    pass

#insert intitial values into database table
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

