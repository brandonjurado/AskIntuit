from bs4 import BeautifulSoup
import requests
import re
from collections import OrderedDict

search_term_string="how to file taxes on a roth ira"
page = requests.get("https://accountants-community.intuit.com/search?utf8=%E2%9C%93&q="+search_term_string)
soup = BeautifulSoup(page.content, 'html.parser')

links = str(soup.find("div", {"id": "search-results"}))
article_indexes = re.findall('"([^"]*)"', links)
li = []
for i in article_indexes:
  if i.startswith("Article"):
    li.append(i)
final_indexes = []
for i in li:
  x = i.split()
  final_indexes.append(x[1])
final_indexes = list(OrderedDict.fromkeys(final_indexes))
answer_array = []
question_array = []
#https://accountants-community.intuit.com/articles/1609578
for i in final_indexes:
  rr = requests.get("https://accountants-community.intuit.com/articles/" + i)
  soup = BeautifulSoup(rr.content, 'html.parser')
  if "Solution Description" in str(soup) and "Question 1:" not in str(soup):
      result = soup.find("div", class_="article-body salesforce")
      question = list(result.children)[0].text
      if (question == "Problem Description"):
          text = list(result.children)[1:]
          for i in text:
              if (i.string != None and i.string.strip()):
                  question = i.string
                  break
      question_array.append(question)
      answer = result.text.replace('\n', ' ')
      answer_array.append(answer)
print(question_array)
print(answer_array)