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


def popTexts(soup):
    results = soup.find(id="widepage").find(class_="list-group").find_all(class_="amw-listing-item")
    print(results)

    for item in results:
        # splits the item into a list, ['Book Title', 'Author']
        label = convert(item.text, ' — ')
        #                    remove newline characters
        book = label[0].replace('\n', '')
        # split 'author + pages' into list (use 6 spaces as split) 
        secondHalf = convert(label[1], '      ')
        #author is the first half of that list
        author = secondHalf[0]
        print(f"Book Title: {book}\nAuthor Name: {author}\n")

