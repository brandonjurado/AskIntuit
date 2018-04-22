from bs4 import BeautifulSoup
import requests
import re
from collections import OrderedDict
from flask_ask import Ask, statement, question, session
from flask import Flask, render_template
from flask_ask import Ask, statement


app = Flask(__name__)
ask = Ask(app, '/')



# Query intuit
def searchIntuit(query):
    search_term_string = query
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
    return question_array, answer_array

index = 0
temp = 0

@ask.intent("QueryKnowledgebase")
def getAnswer(query):
    session.attributes["index"]=0
    index=session.attributes["index"]
    session.attributes["currentQuery"] = query
    session.attributes["questionArr2"], session.attributes["answerArr2"] = searchIntuit(query)
    questionArr2, answerArr2= session.attributes["questionArr2"], session.attributes["answerArr2"]
    return question("I have found " + questionArr2[index] + "Does this match your search term?")


@ask.intent('AMAZON.YesIntent')
def yes_intent():
    query = session.attributes["currentQuery"]      
    session.attributes["questionArr2"], session.attributes["answerArr2"] = searchIntuit(query) 
    questionArr2, answerArr2= session.attributes["questionArr2"], session.attributes["answerArr2"]  
    temp=session.attributes["index"]
    session.attributes["index"] = 0
    return statement(answerArr2[temp])

@ask.intent('AMAZON.NoIntent')
def no_intent():    
    query = session.attributes["currentQuery"]
    session.attributes["questionArr2"], session.attributes["answerArr2"] = searchIntuit(query) 
    questionArr2, answerArr2= session.attributes["questionArr2"], session.attributes["answerArr2"]    
    session.attributes["index"]+=1
    index = session.attributes["index"]
    return question("I have found " + questionArr2[index] + "Does this match your search term?")

# ALEXA STUFF
@ask.launch
def start_skill():
    welcome_message = "Hello there, I can answer questions using intuit knowledge base. Ask away"
    return statement(welcome_message)
# Tell me hi
@ask.intent("HelloIntent")
def hello():
    message = "Nice job, the hello intent is working"
    return statement(message)
# fileRoth Tester
# how to file Roth
@ask.intent("fileRoth")
def fileRothFunction():
    questionArr1, answerArr1 = searchIntuit("how to file a roth ira")
    return statement("You've activated fileRoth Intent" + answerArr1[0])
# Search Question
# ask intuit search knowledgebase

# can I write down a loss of inventory?
@ask.intent("InventoryLoss")
def demoInventoryLoss():
    message = '''If the inventory was destroyed, that means it isn't on hand at the end of the year.
    If it isn't on hand at the end of the year, you will get your deduction when you adjust inventory to the actual year end balance. '''
    return statement(message)
# non-resident amended tax return
@ask.intent("MileageWriteOff")
def demoMileageWriteOff():
    message = '''

    Business mileage, including driving to acquire supplies is deductible.
    Now, if she does a 3000 mile road trip and stops in to pick up one bottle of shampoo....you'll need to evaluate the reasonableness of her contemporaneous mileage log.
    '''
    return statement(message)

@ask.intent("NonJerseyTaxReturn")
def demoNonJerseyTaxReturn():
    message = "On Paper. Use NJ-1040NR and write AMENDED on the top. FYI-this info is in the NJ-1040NR instructions"
    return statement(message)


if __name__ == '__main__':
    app.run(debug=True)

