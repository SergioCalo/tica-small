import streamlit as st
import pandas as pd
import numpy as np
import credits
from intent_classifier import predict_intent
import time
import speech_recognition as sr
!pipwin install pyaudio

#STT
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events as ASR

#TTS
from TTS import TTS
voice_ = 'female'


from DM_answer import action, sub_greeting, sub_recommendation, sub_location, sub_ask_timetable, sub_timetable

# Creating a demo app with multiple pages
def main():
    # Adding logo to sidebar
    st.sidebar.image("images/Tica.png", width=200)
    # st.sidebar.image("images/eve-logo.png", width=200)

    selected = st.sidebar.radio(
        "Navigate pages", options=["Home", "Credits"]
    )
    
    name = None

    if selected == "Home":
        home()
        
    if selected == "Credits":

        def run_credits_train():
            credits.main()

        run_credits_train()



def home():
    st.title("Welcome to TICA, your Tourist Information Conversational Agent")
    user_input = None
    def takecomand():
        r=sr.Recognizer()
        with sr.Microphone() as source:
            audio=r.listen(source)
            try:
                text = r.recognize_google(audio)
            except:
                TTS("Please say something, I'm bored!", voice = st.session_state.voice)
                return
            return text

    if st.button("Click here so I can hear you :)"):
        user_input = takecomand()
    
    st.write("Select voice: ")
    col1, col2, col3 = st.columns([1,1,1])

   # with col1:
    #    male_voice_button = st.button('Male (powered by pyttsx3)')
    #with col2:
    #    female_voice_button = st.button('Female (powered by gTTS)')
    
    if "subaction" not in st.session_state:
         st.session_state.subaction = False
            
    if "name" not in st.session_state:
         st.session_state.name = None
            
    if "previous_recom" not in st.session_state:
         st.session_state.previous_recom = []
            
    if "items" not in st.session_state:
        st.session_state.items = pd.DataFrame({'Positive': [[]],
                                              'Negative': [[]]}).astype('object')
        st.session_state['items'].to_csv('items.csv')
            
    if "voice" not in st.session_state:
         st.session_state.voice = 'female'
    if st.button('Male (powered by pyttsx3)'):
         st.session_state.voice = 'male'

    if st.button('Female (powered by gTTS)'):
         st.session_state.voice = 'female'

    if user_input:
            st.write(user_input)
            intent = predict_intent(user_input)
            st.write(intent)
            
            
            if st.session_state.subaction == 'recommendation':
                answer, st.session_state.subaction = sub_recommendation(intent, user_input, st.session_state['items'], st.session_state.voice,  st.session_state['previous_recom'])   
                st.write(answer)
                TTS(answer, voice = st.session_state.voice)
                return
            
            if st.session_state.subaction == 'Location':
                answer, st.session_state.subaction = sub_location(intent, user_input, st.session_state['items'], st.session_state.voice,  st.session_state['previous_recom'])    
                st.write(answer)
                TTS(answer, voice = st.session_state.voice)
                return
            
            if st.session_state.subaction == 'Timetable':
                answer, st.session_state.subaction = sub_timetable(intent, user_input, st.session_state['items'], st.session_state.voice,  st.session_state['previous_recom'])    
                st.write(answer)
                TTS(answer, voice = st.session_state.voice)
                return
            
            if st.session_state.subaction == 'Ask_timetable':
                answer, st.session_state.subaction = sub_ask_timetable(intent)
                TTS(answer, voice = st.session_state.voice)
                return
            
            if st.session_state.subaction == 'Greeting':
                answer, st.session_state.name, st.session_state.subaction = sub_greeting(user_input, st.session_state.voice)
                st.write(answer)
                TTS(answer, voice = st.session_state.voice)
                return
            
            if st.session_state.subaction == False:
                answer, st.session_state.subaction, st.session_state['previous_recom'] = action(intent,  user_input,  st.session_state.voice, st.session_state.name, st.session_state['items'], st.session_state['previous_recom'] )
                st.write(answer)
                TTS(answer, voice = st.session_state.voice)
                return
                                     


if __name__ == "__main__":
    main()
