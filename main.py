from bs4 import BeautifulSoup
import requests

#funcs
def convert(string, breaker):
    li = list(string.split(breaker))
    return li

#get the link to the amazon search page which you want to scrape
f = open('link.txt', 'r')
myLink = f.read()
f.close()

#pull the page
myPage = requests.get(myLink).content

soup = BeautifulSoup(myPage, 'lxml')


f = open('myPage.html', 'w')
f.write(soup.prettify())
f.close()

results = soup.find(id="widepage").find(class_="list-group").find_all(class_="amw-listing-item")

for item in results:
    label = convert(item.text, ' — ')
    book = label[0]
    author = label[1]
    print(f"author: {author}\nbook: {book}\n")


print(results[0].text)