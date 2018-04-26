from bs4 import BeautifulSoup
import requests
import re
from collections import OrderedDict

search_term_string = "how do I amend a tax return"
page = requests.get(
  "https://accountants-community.intuit.com/search?filters%5Bcountry%5D=US&filters%5Bdocument_type%5D=Question&filters%5Bstate%5D=Recommended&q=" + search_term_string)
soup = BeautifulSoup(page.content, 'html.parser')
links = str(soup.find("div", {"id": "search-results"}))
article_indexes = re.findall('"([^"]*)"', links)
li = []
for i in article_indexes:
  if i.startswith("Question"):
    li.append(i)
final_indexes = []
for i in li:
  x = i.split()
  final_indexes.append(x[1])
final_indexes = list(OrderedDict.fromkeys(final_indexes))
answer_array = []
question_array = []
for i in final_indexes:
  rr = requests.get("https://accountants-community.intuit.com/questions/" + i)
  soup = BeautifulSoup(rr.content, 'html.parser')
  result = soup.find("h1")
  question_array.append(result.text)
  table = soup.findAll('div', attrs={"class": "my-1"})
  for x in table:
      text = list(x.children)
      answer = []
      for ans in text:
          if (ans.string != None and ans.string.strip()):
              answer.append(ans.string)
      answer_array.append(' '.join(answer))
print(question_array)
print(answer_array)
