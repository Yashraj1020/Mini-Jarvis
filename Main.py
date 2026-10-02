import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from random import sample
from confidentials import api_key, News_api
# import wikipedia
from google import genai
# import setuptools
# import pyaudio

recogniser = sr.Recognizer()
News_api = News_api
client = genai.Client(api_key=api_key)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def process_command(c):
    if "google" in c.lower():
        webbrowser.open("https://google.com")
        speak("Opening google...")
    elif "youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        speak("Opening youtube...")
    elif "linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        speak("Opening linkedin...")
    elif "facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        speak("Opening facebook...")
    elif "instagram" in c.lower():
        webbrowser.open("https://instagram.com")
        speak("Opening instagram...")
    elif "play" in c.lower():
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={News_api}")
        data = r.json()
        articles = data.get('articles', [])
        random_article = sample(articles, min(3, len(articles)))
        speak("Here are some news")
        for article in random_article:
            speak(article['title'])

#     elif "what" in c.lower():
#         try:
#             topic = " ".join(c.lower().split(" ")[2:])

#             if topic:
#                 info = wikipedia.summary(topic, sentences=2)
#                 speak(info)
#             else:
#                 speak("Please say a topic")

#         except Exception as e:
#             print(e)
#             speak("Something went wrong")

    else:
        #Let gemini handle it!  
        response = client.models.generate_content(
            model="models/gemini-flash-lite-latest",
            contents= f"Answer briefly in 1-2 lines: {c}"
        )

        speak(response.text)

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from microphone
        print("recognising...")
        try: 
            with sr.Microphone() as Mic:
                print("Listening...")
                audio = recogniser.listen(Mic, timeout= 3, phrase_time_limit= 4)
            word = recogniser.recognize_google(audio)
            if "jarvis" in word.lower():
                speak("What's up?")
                #Listen for command
                with sr.Microphone() as Mic:
                    print("Jarvis Active...")
                    audio = recogniser.listen(Mic, timeout= 4, phrase_time_limit=2.5)
                command = recogniser.recognize_google(audio)
                process_command(command)
            elif "stop" in word.lower():
                speak("Shutting down")
                exit()
        except Exception as e:
            print(f"Error; {e}")