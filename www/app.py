from curses import echo
from fnmatch import translate
from tkinter import font
from flask import Flask, render_template, request
import config
import aicontent
import json
# import googletrans
from googletrans import Translator
from aicontent import ask
from aicontent import append_interaction_to_chat_log
from texttospeech import text_to_speech

chat_logs = [''];

def page_not_found(e):
    return render_template('404.html'), 404

app = Flask(__name__)
app.config.from_object(config.config['development'])
app.register_error_handler(404, page_not_found)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())

@app.route('/everything', methods=["GET", "POST"])
def everything():
    if request.method == "POST":
        translate = Translator()
        requestEverything = request.form['requestEverything']
        requestEverythingFR = translate.translate(requestEverything, dest='fr').text
        query = "{}".format(requestEverythingFR)
        openAIAnswerUnformatted = aicontent.openAIQuery(query)
        openAIAnswer = openAIAnswerUnformatted.replace('\n', '<br>')
        answerTranslation = translate.translate(openAIAnswer, dest='fr')
        openAIAnswer = answerTranslation.text

    return render_template('everything.html', **locals())

@app.route('/chat-with-ai', methods=["GET", "POST"])
def chat_with_ai():
    if request.method == "POST":
        chat_log = None
        translate=Translator()
        query = request.form['tellStoryForm']
        # query = "{}{}".format(query, chat_logs)
        queryEN = translate.translate(query, dest='en').text
        answer = ask(queryEN, None)
        answer=translate.translate(answer,dest='fr').text
        chat_logs.append("Human: {}".format(query))
        chat_logs.append("AI: {}".format(answer))

    return render_template('chat-with-ai.html', **locals(), chat_logs=chat_logs)

@app.route('/frontend', methods=["GET", "POST"])
def frontend():
    if request.method == 'POST':
        text = request.form['speech']
        gender = request.form['voices']
        text_to_speech(text, gender)
        return render_template('frontend.html')
    else:
        return render_template('frontend.html')

@app.route('/tell-story-ai', methods=["GET", "POST"])
def tellStoryForm():
    f = open('actors_list.json')
    data = json.load(f)
    # actors = [{'name': 'Tom', 'capacities': ['man','fun', 'smart']}, {'name': 'Katty', 'capacities': ['woman','smart','test']}]
    actors = data
    if request.method == 'POST':
        translate=Translator()
        submission = request.form['tellStoryForm']
        submission_who = request.form['tellStoryForm-who']
        submissionEN = translate.translate(submission, dest='en')
        if submission_who == "":
            query = "Tell me a story about: {}".format(submission)
            query2 = "Tell me a story about: {}. The characters are : ".format(submissionEN.text)
            for actor in actors:
                query2 = query2 + "{}, ".format(actor['name'])
                for capacity in actor['capacities']:
                    # query2 = "{} {}".format(query2, capacity)
                    query2 = query2 + "is {} , ".format(capacity)
        else:
            # query = "Tell me a story about: {}. In this story, pepole are named : {}".format(submission, submission_who)
            query = "Tell me a story about: {}. The characters are are named : {}".format(submission, submission_who)
        openAIAnswerUnformatted = aicontent.openAIQuery(query2)
        # openAIAnswer = openAIAnswerUnformatted.replace('\n', '<br>')
        openAIAnswer = openAIAnswerUnformatted.replace('\n', '<br>')
        answerTranslation = translate.translate(openAIAnswer, dest='fr')
        openAIAnswer = answerTranslation.text
        prompt = 'AI Story for {} is:'.format(submission)
    return render_template('tell-story-ai.html', **locals())
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)