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

        search_term_string = question
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
        return {'questions':question_array, 'answers':answer_array}

restApi.add_resource(QueryEngine, '/query/<string:question>')

if __name__ == '__main__':
    app.run(debug=True)