from bs4 import BeautifulSoup
from requests import get

def google_results(keyword):
    '''Takes a given word and scrapes information of a google query
    about that word. It then returns a string with the first 
    result's title and URL.
    
    Args:
        keyword (str): The word to be used in the google query.
    
    Returns:
        (str): A formatted string with the first result's title and URL.'''

    #The target URL to be scraped (executes a google query for 'keyword')
    target = "https://www.google.pt/search?q=" + keyword + "&ie=utf-8"
    #Get the source code of the page
    source = get(target).text
    #Create a BeautifulSoup object with the source code, parsing it with lxml
    soup = BeautifulSoup(source, 'lxml')

    #The tag we are looking for in the html
    results = soup.find_all('div', class_='g')
    num = 1

    for result in results:
        try:
            #The result's title will be found in this tag
            result_title = result.h3.a.text
            #Creates a list where each item is a line of the span tag's text (the result's description)
            result_desc = "".join(result.find('span', class_='st').text.splitlines())[:100] + '...'
            #From the link string, remove the part before 'https' and end at '.html'
            result_link = result.h3.a["href"][7:].split('&')[0]
            print(f'The #{num} google result for "{keyword}", is "{result_title}" which you can find at {result_link}')
        except:
            print(f'Something went wrong scraping result #{num}')
        print()
        num += 1

if __name__ == '__main__':
    print(google_results('python'))