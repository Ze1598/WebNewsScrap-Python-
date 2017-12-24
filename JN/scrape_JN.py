#A script to scrape Jornal de Notícias (https://www.jn.pt') front page news and its URLs

#Import the necessary modules
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime

#get a text version of the requested website source code
website = 'https://www.jn.pt'
source = get(website).text
#then parse it using lxml
soup = BeautifulSoup(source, 'lxml')

#Get only the first article's title and URL
def get_first_article():
    article = soup.find('article', class_ = 't-g1-l1-am1')
    title = 'Notícia:', article.header.h2.text
    link = 'Link: ' + website + str(article.header.h2.a['href'])
    return f'The first featured news at JN\'s website is "{title}" which you can read at {link}'

# Get all the front page articles' titles and URLs
def get_articles():
    write_string = ''
    for articles in soup.find_all('article', class_ = 't-g1-l1-am1'):
        title = articles.header.h2.text
        link = website + str(articles.header.h2.a['href'])
        write_string += 'News: "{}" which you can read at {}\n\n'.format(title, link)
    return write_string

minute, hour, day, month, year = datetime.now().minute, datetime.now().hour, datetime.now().day, datetime.now().month, datetime.now().year
#The new .txt to be created will have this name
file_name = f'JNews_{month}-{day}th-{year}_{hour}--{minute}.txt'

if __name__ == '__main__':
    print(get_first_article())
    with open(file_name, 'w') as new_file:
        new_file.write('Current featured news at www.jn.pt:\n' + get_articles())