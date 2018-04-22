from bs4 import BeautifulSoup
import requests
import re
from collections import OrderedDict
from flask_ask import Ask, statement, question, session
from flask import Flask, render_template
from flask_ask import Ask, statement
from twilio.rest import Client
from urllib.request import urlopen
import boto3
import re

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
    cutOffIndex = 0
    for i in final_indexes:
        cutOffIndex += 1
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
        if cutOffIndex == 3:
            return question_array, answer_array

@ask.intent("QueryKnowledgebase")
def getAnswer(query):
    isBroke = False
    triggerWords = ["broken", "not working", "broke", "isn't working"]
    for i in triggerWords:
        x = 0
        if i in query:
            isBroke = True
            account_sid = "AC5250b6f6b34be7f37a0a9c188bdcea1e"
            auth_token = "0a413933672df9a739527e5259d25997"
            client = Client(account_sid, auth_token)
            client.api.account.messages.create(
            to="+12545772767",
            from_="+12548314738",
            body="User has sent message: {} Check application and functionality".format(query))
            with urlopen("https://s3-us-west-2.amazonaws.com/one-int/alerts.txt") as url:
                s = url.read()
            string1 = str(s)
            x = int(re.search(r'\d+', string1).group())
            x += 1
            binary = str(x).encode()
            s3 = boto3.resource('s3')
            object = s3.Object('one-int', 'alerts.txt')
            object.put(Body=binary)
            boto3.resource('s3').ObjectAcl('one-int','alerts.txt').put(ACL='public-read')
        if x > 2:
            account_sid = "ACf4b4c4a21347b9fce0358f0f6ebac107"
            auth_token = "3fba63cfcd3d1f38ef6d7f1f98cbb01e"
            client = Client(account_sid, auth_token)
            client.api.account.messages.create(
            to="+18176532661",
            from_="+14694163460",
            body="An unusually high number of people are experiencing application issues, check the logs")
            x = 0
            binary = str(x).encode()
            s3 = boto3.resource('s3')
            object = s3.Object('one-int', 'alerts.txt')
            object.put(Body=binary)
            boto3.resource('s3').ObjectAcl('one-int','alerts.txt').put(ACL='public-read')
        break
    if isBroke:
        return statement("I noticed that you have reported that something isn't working correctly, we will forward this to our team and be in touch with a solution, thank you.")
        
    session.attributes["noCounter"] = 0
    session.attributes["index"]=0
    index=session.attributes["index"]
    session.attributes["currentQuery"] = query
    session.attributes["questionArr2"], session.attributes["answerArr2"] = searchIntuit(query)
    questionArr2, answerArr2= session.attributes["questionArr2"], session.attributes["answerArr2"]
    return question("I have found..." + questionArr2[index] + "...Does this match your search term?")


@ask.intent('AMAZON.YesIntent')
def yes_intent():
    if session.attributes["noCounter"] == 3:
        return statement("Please let me know more about your issue or question and I will pass it on, thank you.")
    else:
        query = session.attributes["currentQuery"] 
        session.attributes["noCounter"] = 0     
        questionArr2, answerArr2= session.attributes["questionArr2"], session.attributes["answerArr2"]  
        temp=session.attributes["index"]
        session.attributes["index"] = 0
        message = ''
        if len(answerArr2[temp].split()) > 35:
            message = "The message is pretty lengthy, I will text it to you instead"
            account_sid = "AC5250b6f6b34be7f37a0a9c188bdcea1e"
            auth_token = "0a413933672df9a739527e5259d25997"
            client = Client(account_sid, auth_token)
            client.api.account.messages.create(
            to="+12545772767",
            from_="+12548314738",
            body=answerArr2[temp])
        else:
            message = answerArr2[temp]
        return statement(message)

@ask.intent('AMAZON.NoIntent')
def no_intent():
    if session.attributes["noCounter"] == 3:
        return statement("I'm sorry we couldn't match your search. Thank you.")
    else:
        query = session.attributes["currentQuery"]
        questionArr2, answerArr2= session.attributes["questionArr2"], session.attributes["answerArr2"]    
        session.attributes["index"]+=1
        session.attributes["noCounter"]+=1
        index = session.attributes["index"]
        if session.attributes["noCounter"] == 3:
            return question("We don't seem to be finding what you want, I will submit this question to the knowledge base for you.  Would you like to provide more details to your quesiton?")
        else:
            return question("I have found..." + questionArr2[index] + "...Does this match your search term?")

# ALEXA STUFF
@ask.launch
def start_skill():
    welcome_message = "Hello there, I can answer questions using intuit knowledge base. Ask away"
    return question(welcome_message)
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

