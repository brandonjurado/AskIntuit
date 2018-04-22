from flask import Flask, render_template
from flask_restful import Resource, Api as RestfulApi
from flask_ask import Ask, statement

app = Flask(__name__)
restApi =  RestfulApi(app)
ask = Ask(app, '/')

# Load the views
import views

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@ask.intent('HelloIntent')
def hello(firstname):
    text = render_template('hello', firstname=firstname)
    return statement(text).simple_card('Hello', text)

class QueryEngine(Resource):
    def get(self, question):
        from bs4 import BeautifulSoup
        import requests
        import re
        from collections import OrderedDict

        #search_term_string="how to file taxes on a roth ira"
        search_term_string = question
        r = requests.get("https://accountants-community.intuit.com/search?utf8=%E2%9C%93&q="+search_term_string)
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
        return {'questions':question_array, 'answers':answer_array}

restApi.add_resource(QueryEngine, '/query/<string:question>')

if __name__ == '__main__':
    app.run(debug=True)