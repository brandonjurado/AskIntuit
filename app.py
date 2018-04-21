from bs4 import BeautifulSoup
import requests
import re
from collections import OrderedDict
from flask_ask import Ask, statement, question, session
from flask import Flask, render_template
from flask_ask import Ask, statement


app = Flask(__name__)
ask = Ask(app, '/')


# Example to demonstrate reutning two ints and assigning to function
# def returnInt():
#     a=1
#     b=2
#     return a,b

# x,y=returnInt()

# Query intuit 
def searchIntuit(query):
    search_term_string = query
    search_term_string = "how to file taxes on a roth ira"
    r = requests.get(
        "https://accountants-community.intuit.com/search?utf8=%E2%9C%93&q="+search_term_string)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    links = str(soup.find("div", {"id": "search-results"}))
    article_indexs = re.findall('"([^"]*)"', links)
    li = []
    for i in article_indexs:
        if i.startswith("Article"):
            li.append(i)
    final_indexs = []
    for i in li:
        x = i.split()
        final_indexs.append(x[1])
    final_indexs = list(OrderedDict.fromkeys(final_indexs))
    answer_array = []
    question_array = []
    #https://accountants-community.intuit.com/articles/1609578

    for i in final_indexs:
        rr = requests.get("https://accountants-community.intuit.com/articles/" + i)
        result_data = rr.text
        soup = BeautifulSoup(result_data, 'html.parser')
        if "Solution Description" in str(soup) and "Question 1:" not in str(soup):
            for row in soup.find_all('div', attrs={"class": "article row"}):
                print(i)
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
    return question_array, answer_array


    # ALEXA STUFF


@ask.launch
def start_skill():
    welcome_message = "Hello there, I can answer questions using intuit knowledge base. Ask away"
    return question(welcome_message)

@ask.intent("HelloIntent")
def hello():
    message = "Nice job, the hello intent is working"
    return statement(message)

@ask.intent("fileRoth")
def fileRothFunction():
    questionArr, answerArr = searchIntuit("how to file a roth IRA")
    return statement(answerArr[0])

if __name__ == '__main__':
    app.run(debug=True)