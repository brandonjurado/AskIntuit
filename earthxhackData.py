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
  result_data = rr.text
  soup = BeautifulSoup(result_data, 'html.parser')
  if "Solution Description" in str(soup) and "Question 1:" not in str(soup):
    for row in soup.find_all('div',attrs={"class" : "article row"}):
      start1 = 'modified'
      start2 = 'Solution Description'
      end1 = 'Solution'
      end2 = 'Was this article helpful?'
      s = row.text
      questions = s[s.find(start1) + len(start1):s.rfind(end1)]
      questions = questions.replace('\n', '')
      answers = s[s.find(start2) + len(start2):s.rfind(end2)]
      answers = answers.replace('\n', '')
      question_array.append(questions)
      answer_array.append(answers)
print(question_array)
print(answer_array)
