from gtts import gTTS
import pyttsx3
from playsound import playsound 
import eyed3
import time

engine = pyttsx3.init()
engine.setProperty('rate',150)

def TTS(answer, voice = 'female'):
    
    if voice == 'male':
        
        engine.say(answer)
        engine.runAndWait()
    
    if voice == 'female':
        
        myobj = gTTS(text=answer, lang='en', slow=False)
        myobj.save("answer.mp3")
        playsound("answer.mp3", block=True)
        duration = eyed3.load('answer.mp3').info.time_secs
