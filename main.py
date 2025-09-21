from neuralintents import GenericAssistant as GA
from speech_recognition import Recognizer , Microphone , UnknownValueError
import pyttsx3 as tts
import sys

recognizer = Recognizer()
speaker = tts.init()
speaker.setProperty('rate' , 150)

todo_list = [
    'Go Shopping',
    'Clean Room',
    'Record Video'
]

def adjust(mic : Microphone , duration : float):
    recognizer.adjust_for_ambient_noise(mic , duration)

def listen(mic):
    audio = recognizer.listen(mic)
    return audio

def recognize_google(audio):
    note  = recognizer.recognize_google(audio)
    note = note.lower()
    return note
    
def say(text : str):
    speaker.say(text)
    
def run_wait():
    speaker.runAndWait()

def say_wait(text: str):
    say(text)
    run_wait()

def create_note():
    global recognizer
    say_wait("What do you want to write on your note?")
    
    done = False
    while not done:
        try: 
            with Microphone() as mic:
                adjust(mic , 0.5)
                 
                audio = listen(mic)
                text = recognize_google(audio)
                
                say_wait('Choose a filename:')
                
                adjust(mic , 0.5)
                
                audio = listen(mic)
                filename = recognize_google(audio)
            
            with open(f'{filename}.txt') as file:
                file.write(text)
                say_wait(f'I successfuly created the note {filename}')
    
        except UnknownValueError:
            recognizer = Recognizer()
            say_wait('I did not understand you, please try again!!!')

def add_todo():
    global speaker
    say_wait("What do you want to add?")
    
    done = False
    
    while not done:
        try:
            with Microphone() as mic:
                adjust(mic , 0.3)
                
                audio = listen(mic)
                item = recognize_google(audio)
                todo_list.append(item)
                
                say_wait(f"I added {item} to do list")
        
        except UnknownValueError:
            recognizer = Recognizer()
            say_wait('I did not understand you, please try again!!!')
    
def show_todos():
    say("the item on your to do list are the following")
       
    for item in todo_list:
        say(item)
    
    speaker.runAndWait()
    
def hello():
    say_wait("Hello. What can I do for you?")
    
def quit():
    say_wait("Bye")
    sys.exit(0)

if __name__ == '__main__':
    mappings = {
        'greeting': hello,
        "create_note" : create_note,
        "add_todo" : add_todo,
        "show_todos": show_todos,
        "exit" : quit
    }

    assistant = GA('intents.json' , intent_methods = mappings)
    assistant.train_model()

    while True:
        try:
            with Microphone() as mic:
                adjust(mic , 0.3)
                audio = listen(mic)
                message = recognize_google(audio)
            
            assistant.request(message)
            
        except UnknownValueError:
            recognizer = Recognizer()