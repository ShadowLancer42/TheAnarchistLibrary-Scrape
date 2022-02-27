from bs4 import BeautifulSoup
import requests
import json

#funcs
#region

#general purpose
def convert(string, breaker):
    li = list(string.split(breaker))
    return li

#makes a dict from the structure (the keys) and a label var (the values)
# both should be lists. the label will have info like author name, book title, etc.
def dictMaker(label, structure):
    output = {}
    for i in range(len(label)):
        try:
            output.update({structure[i] : label[i]})
        # in case of the label having more data than the structure can account
        # for, just use "other" as the key
        except:
            output.update({"other" : label[i]})
    return output


# takes a list of results (use find_all()) and iterates through, and seperates
# results into a list: [Book Title, Author name, (whatever else may be tagged on at the end)]
def fetchResults(results, breaker, structure):
    output = []
    for item in results:
        # splits the item into a list, ['Book Title', 'Author']
        label = convert(item.text, ' — ')
        #                    remove newline characters
        book = label[0].replace('\n', '')
        # split 'author + pages' into list (use 6 spaces as split) 
        secondHalf = convert(label[1].replace('  ', ''), breaker)
        #author is the first half of that list
        author = secondHalf[0]

        #takes book title, author, and all list items formed after that, and puts
        # them into a single, non-nested, list.
        # ex: [book title, author name, date posted, pp number]
        thisLabel = [book]
        for i in secondHalf:
            if (i != ''):
                thisLabel.append(i)
        # add a nested dict of this specific label to the list, which we will output once
        # we have iterated through all labels.
        output.append(dictMaker(thisLabel, structure))
    return output

        

def popTexts(soup):
    results = soup.find(id="widepage").find(class_="list-group").find_all(class_="amw-listing-item")
    structure = ["Book Title", "Author Name", "Downloads"]
    data = fetchResults(results, '      ', structure)
    return data

def topicPage(soup):
    results = soup.find(id="widepage").find(class_="amw-post-listing-container").div.div.find_all(class_="amw-listing-item")

    structure = ["Book Title", "Author Name", "Date Published", "Pages"]
    #feed fetchResults your find_all() list of items, it will give you the data on it
    # in the form of a list containing several dicts (so a python version of a json)
    data = fetchResults(results, '\n', structure)
    return data

#endregion

#the page to scrape
myLink = "https://theanarchistlibrary.org/category/topic/black-flag"


#pull the page
myPage = requests.get(myLink).content

soup = BeautifulSoup(myPage, 'lxml')

#
print(topicPage(soup))

myData = json.dumps(topicPage(soup), indent=4)

# save it on a json file
f = open('myData.json', 'w')
f.write(myData)
f.close()