from bs4 import BeautifulSoup
from requests import get

#Get a text version of the website's source code
website = 'http://www.bbc.com/news/world'
source = get(website).text
soup = BeautifulSoup(source, 'lxml')

#get the first featured post, both its title and URL
def get_first_post():
    article = soup.find('div', class_='buzzard-item')
    link = website[0:18] + article.a['href']
    title = article.a.h3.span.text
    return (title,link)

if __name__ == '__main__':
    print(get_first_post())