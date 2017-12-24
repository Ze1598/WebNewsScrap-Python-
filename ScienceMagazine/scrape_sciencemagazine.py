#Scrape Science magazine website: only artciles' titles and links

from bs4 import BeautifulSoup
from requests import get
from datetime import datetime

#Create the name for the file to be created at the end containing the scrapped information
minute, hour, day, month, year = datetime.now().minute, datetime.now().hour, datetime.now().day, datetime.now().month, datetime.now().year
file_name = 'JNews_{}-{}th-{}_{}--{}.txt'.format(month, day, year, hour, minute)

#Website to be scraped
website = 'http://www.sciencemag.org/'
#Then GET a text version of its source code...
source = get(website).text
#For it to be parsed using lxml to create a BeautifulSoup object
soup = BeautifulSoup(source, 'lxml')

def get_first_article():
    article = soup.find('div', class_ = 'hero__content')
    #remove leading spaces from the title
    article_title = article.h2.a.text.strip()
    article_url = website + article.h2.a['href']
    return f'@sciencemagazine \'s featured article is \'{article_title}\', which you can read at {article_url}'

def get_articles():
    articles = soup.find_all('div', class_ = 'hero__content')
    write_string = ''
    for article in articles:
        write_string += f'Title: {article.h2.a.text.strip()}\nURL: {website+article.h2.a["href"]}\n\n'
    return write_string

if __name__ == '__main__':
    print(get_first_article())
    with open(file_name, 'w') as new_file:
        new_file.write(get_articles())