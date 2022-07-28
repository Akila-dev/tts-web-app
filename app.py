from flask import Flask, render_template, request, flash
from time import sleep
import speech_recognition as sr
import pyttsx3
from time import sleep

# from waitress import serve

app = Flask(__name__)
# app.config['DEBUG'] = True
app.secret_key = "manwolfdragon_1234509876"

@app.route("/")
def index():
    flash(objQuestion)
    return render_template("index.html")

@app.route("/start", methods=["POST", "GET"])
def start():
    flash(objQuestion)
    sleep(1)
    objective(objQuestion)
    return render_template("index.html")

    

# @app.route("/app")
# def app():
#     flash(objquestion)
#     return render_template("app.html")

# SPEECH RECOGNITION START
import speech_recognition as sr
import pyttsx3

required=0
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    if "pulse" in name:
        required= index
r = sr.Recognizer()

def listen(response = False):
    print("Listening...")
    with sr.Microphone(device_index=required) as source:
        if response:
            ai_speak(response)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            ai_speak('Sorry, I did not get that')
        except sr.RequestError:
            ai_speak('Sorry, my speech service is down')
        return voice_data
    

def ai_speak(audio_string):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty("rate", 130)#changing index changes voices but ony 0 and 1 are working here
    print(audio_string)
    engine.say(audio_string)
    engine.runAndWait()



def check_response(question, voice_data):
    q = question
    lowercaseQuestion = question.lower()
    answerArray = voice_data.split(' ')
    questionArray = lowercaseQuestion.split(' ')
    print(answerArray)
    print(questionArray)
    if answerArray != questionArray:
        wrongWords = []
        if len(answerArray) <= len(questionArray):
            for x, word in enumerate(answerArray):
                if word != questionArray[x]:
                    wrongWords.append(x)
        else:
            vd = listen(f'Try Pronouncing the words again gently')
            check_response(q, vd)
        print(wrongWords)
        
        if len(wrongWords) > 0 and len(answerArray) == len(questionArray):
            vd = listen(f'Almost there, try pronouncing this word as {questionArray[wrongWords[0]]}')
            check_response(q, vd)
        elif len(wrongWords) > 0 and len(answerArray) < len(questionArray) or len(wrongWords) > 0 and len(answerArray) > len(questionArray):
            vd = listen(f'Try Pronouncing the words again gently')
            check_response(q, vd)
    else:
        ai_speak('Correct. Well done')
    


def objective(question, call=True):
    if call:
        ai_speak("Let's try pronouncing this sentence")
        voice_data = listen()
        check_response(question, voice_data)
    else:
        exit()

objQuestion = "He is the president"

# objective(objQuestion)
# SPEECH RECOGNITION END


if __name__ == "app":
    app.run()
# serve(app, host="0.0.0.0", port=8080, threads=1)