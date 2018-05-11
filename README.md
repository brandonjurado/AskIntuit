# AskIntuit
An Alexa skill built to answer questions directed towards Intuit using Intuit Knowledgebase.

## Setup
The environment setup uses the following tutorial: 

https://developer.amazon.com/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/new-alexa-tutorial-deploy-flask-ask-skills-to-aws-lambda-with-zappa
 
### Step 1:
Clone the project and checkout VoiceInterface

<code> git clone https://github.com/brandonjurado/AskIntuit.git

git checkout VoiceInterface

</code>

### Step 2:
Install a virtual environment using virtualenv

<code> 
    pip install virtualenv
</code>

### Step 3: Create a virtual environment

<code>
    virtualenv venv
</code>

Activate the virtual environment 

Windows:

<code>
source venv\Scripts\activate
</code>

Unix

<code>
source venv/bin/activate
</code>

If successful, your virtual environment command line should look like this: 

(venv) hjones:AskIntuit$

### Install dependencies 
Because of a problem with flask-ask, you need to use pip version 9.0.1

Windows:

<code>
python.exe -m pip install --upgrade pip==9.0.1
</code>

Let's install our dependencies from the requirements.txt file. This was created using <code> pip freeze > requirements.txt </code>

<code>
pip install -r requirements.txt
</code>

### Configure AWS
You'll need the following. These credentials were sent to you.  

- Access Key ID
- Secret Access Key

<code> aws configure </code>

Use default region and output format

### Configure Zappa
In order for the zappa configuration to work, we have to fix a bug in zappa. To do tthis, open 'utilities.py' at 

\AskIntuit\venv\Lib\site-packages\zappa\utilities.py

Replace line 142 with

<code>
with open(full, 'r', encoding="utf8") as f:
</code>

Be sure to check indentation errors.

//TODO

I have to figure out how to share this zappa config so we can have multiple branches. 


Create a zappa config file

<code> zappa init </code>

<code>