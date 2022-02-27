from bs4 import BeautifulSoup
import requests

myLink = 'https://theanarchistlibrary.org/category/topic'

#pull the page
myPage = requests.get(myLink).content
soup = BeautifulSoup(myPage, 'lxml')

#save pulled data to an html file
f = open('myPage.html', 'w')
f.write(soup.prettify())
f.close()