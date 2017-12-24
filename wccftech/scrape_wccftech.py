#Script to scrape wccftech's featured articles' title and URL

#imports
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime

#target website
website = 'https://wccftech.com/'
#make a GET request for the source code
source = get(website).text
#then parse it using lxml
soup = BeautifulSoup(source, 'lxml')

#create the name for the file to be created
minute, hour, day, month, year = datetime.now().minute, datetime.now().hour, datetime.now().day, datetime.now().month, datetime.now().year
file_name = 'wccftech_{}-{}th-{}_{}--{}.txt'.format(month, day, year, hour, minute)

#this function will return a list, where the first item is the title of the first featured article's title, \
#and the second item is the article's URL
def get_first_article():
    article = soup.find('a', class_ = 'featured featured-1')
    #return [article's title, article's URL]
    return (article.h2.text, article['href'])

#this function will return a string, containing all 6 featured articles, both its titles and its URLs
def get_articles():
    write_string = ''
    #because the name of the classes in the source code is 'featured featured-'+ a number between 1 and 6, I used a for loop within that \
    #range to get the articles, because I wasn't able to loop through the parent class for some reason
    for i in range(1,7):
        article = soup.find('a', class_ = 'featured featured-'+str(i))
        write_string += f'{article.h2.text}: {article["href"]}\n\n'
    return write_string

if __name__ == '__main__':
    print(get_first_article())
    #then what is returned from 'get_articles()' is written to a file in the directory chosen in the beginning
    with open(file_name, 'w') as file:
        file.write(get_articles())