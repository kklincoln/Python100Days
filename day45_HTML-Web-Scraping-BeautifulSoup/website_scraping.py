#LIVE PAGE: news.ycombinator.com/news
#Static page: https://appbrewery.github.io/news.ycombinator.com

from bs4 import BeautifulSoup #beautifulSoup version 4
import requests

response = requests.get(url="https://news.ycombinator.com/news")
yc_web_page =response.text
#-----------WE WANT THE TITLE, SCORE, AND LINKS FOR EACH ITEM IN THE PAGE; BY DEAULT TOP 30 ITEMS---------------------#
soup =BeautifulSoup(yc_web_page,"html.parser")
articles = soup.find_all(class_="titleline")
article_texts = []
article_links = []

#for all article_tag in the articles object, find the article text and the article link
for article_tag in articles:
    text = article_tag.getText()
    article_texts.append(text)
    link = article_tag.select_one(selector ="a").get("href")
    article_links.append(link)

#same as the approach above, but with list comprehension method of generating a list
#the split is removing the " point" segment from the upvote text and just storing it as n int
article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

print(article_texts)
print(article_links)
print(article_upvotes)
#------------------FOR THE HIGHEST SCORING ITEM IN THE LIST, GET INDEX --------------------------#
largest_number = max(article_upvotes)
high_score_index = article_upvotes.index(largest_number)
print(high_score_index)
#-------------------PRINT THE TITLE, LINK, AND SCORE FOR THE HIGHEST SCORING ITEM IN THE PAGE-------------------------#
print(article_texts[high_score_index])
print(article_links[high_score_index])
print(article_upvotes[high_score_index])

#--------------------------------------------#




















#------------------------LESSON ------------------------------#

# with open("website.html") as file:
#     contents = file.read()
#     # print(contents)
#
# soup = BeautifulSoup(contents, 'html.parser') #contents refers to the 'markup' in 'html'
# print(soup.title) #calls the element in html including the title tags,
# print(soup.title.string) # calls the string contained in the element without the tags

# all_anchor_tags = soup.find_all(name="a")
# for tag in all_anchor_tags:
#     # print(tag.getText()) #prints all of the text associated with the anchor tags
#     print(tag.get("href")) # print all of the tags that are associated to each of the ahref elements
#
# heading = soup.find(name="h1",id="name")
# # print(heading)
#
# section_heading =soup.find(name="h3", class_="heading")
# print(section_heading.getText())

# company_url = soup.select_one(selector="p a")
# print(company_url)
#
# name = soup.select_one("#name") #ID selector
# print(name)
#
# heading= soup.select(".heading") #class selector
# print(heading)