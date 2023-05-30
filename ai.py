from calendar import EPOCH
import pyttsx3
import speech_recognition as sr

# Sound effects to replace voice
from sounds import play_greeting, play_response, play_response_2, play_command, play_rejection, play_goodbye

class AI():
    __name = ""
    __skill = []

    def __init__(self, name=None):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.m = sr.Microphone()

        if name is not None:
            self.__name = name
        
        print("Listening...")
        
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        sentence = "Hello, my name is" + self.__name
        self.__name = value
        # self.engine.say(sentence)
        print(sentence)
        play_greeting()
        self.engine.runAndWait()
    
    def say(self, sentence):
        # self.engine.say(sentence)
        print(sentence)
        play_response_2()
        self.engine.runAndWait()

    def listen(self):
        print("Say something")
        with self.m as source:
            audio = self.r.listen(source)
        # print("Got it!")
        try:
            phrase = self.r.recognize_google(audio, show_all=False, language="en_US")
            if phrase not in ["good bye", 'bye', 'quit', 'exit', 'goodbye', 'exit', 'stop']:
                sentence = "Got it! You said " + phrase
                # self.engine.say(sentence)
                print(sentence)
                self.engine.runAndWait()
        except:
            print("Sorry, didn't catch that:")
            # self.engine.say("Sorry, didn't catch that")
            self.engine.runAndWait()
            print("You said: ", phrase)
            play_command()
        return phrase
    
    def stop_ai(self):
        self.engine.stop()
        play_goodbye()
        print("Engine stopped")