"""Script to gather IMDB keywords from 2018's top grosing movies"""
import sys
import requests
from bs4 import BeautifulSoup
import csv

URL = "http://www.imdb.com/search/title?at=0&sort=boxoffice_gross_us,desc&start=1&year=2018,2018"

def get_top_grossing_movie_links(url):
        """Return a list of tuples of the top grossing movies of 2018 and link o their IMDB pages"""
        response = requests.get(url)
        movies_list = []
        soup = BeautifulSoup(response.text, "html.parser")
        for each_url in soup.select('.lister-item-header a[href*="title"]'):
                movie_title = each_url.text
                if movie_title !='X':
                        movies_list.append((movie_title, each_url['href']))
        return movies_list

def get_keywords_for_movies(url):
        """Return a list of keywords associated with *movie*"""
        keywords = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for each_keyword in soup.select('.sodatext a[href*="keyword"]'):
                keyword = each_keyword.text 
                keywords.append(keyword)
        return keywords

def main():
    """Main entry point for the script"""
movies = get_top_grossing_movie_links(URL)
with open('output.csv', 'w') as output:
        csvwriter = csv.writer(output)
        for title, url in movies:
                if '?' in url:
                        url=url.split('?')[0]
                if '#' in url:
                        url = url.split('#')[0]
                keywords = get_keywords_for_movies('http://www.imdb.com{}keywords/'.format(url))
                csvwriter.writerow([title, keywords])

if __name__ == '__main__':
        sys.exit(main())