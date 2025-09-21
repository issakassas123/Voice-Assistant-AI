import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound as ps

'''
Playing Sound
Now that we have these modules installed we can start writing the code to play sound from our computers 
speakers. We will use the gTTS(google text to speech) module to do this.
'''

def speak(text):
    tts = gTTS(text = text , lang = 'en')
    filename = 'voice.mp3'
    tts.save(filename)
    ps.playsound(filename)

'''
Getting User Input
In the last tutorial we learned how to output sound from our python script using the gTTS module. 
In this video we will do the opposite, we will get user input and turn it into text data that we can 
process.

Let's get started by creating a function called get_audio.
'''

def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        audio = recognizer.listen(mic)
        said = ""

        try:
            said = recognizer.recognize_google(audio)
            print(said)
        
        except Exception as e:
            print(f"Exception: {str(e)}")
            
    return said

speak('Hello World')

text = get_audio()

if 'hello' in text:
    speak('hello ok')