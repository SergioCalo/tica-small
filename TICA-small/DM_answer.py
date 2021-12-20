from TTS import TTS
from streamlit_bokeh_events import streamlit_bokeh_events as ASR
import streamlit as st
import pandas as pd
import spacy
from collections import Counter
from templates import add_info_pos_answer
import re

nlp = spacy.load("en_core_web_sm")

def action(intent, user_input, voice, name, items_df, previous_recom):
    answer = "I'm sorry, I don't understand you"
    subaction = False
    keywords = ['museum', 'bar', 'restaurant', 'opera', 'theatre', 'music', 'event', 'art',  'modern',  'painting', 'paint', 'egypt', 'zoo' ,'kid' ,'animal', 'outdoors', 'catalonia', 'theme park', 'rollercoaster', 'mountain', 'activity','tower', 'gaudí', 'gaudí', 'architecture', 'sea', 'exhibition', 'history', 'fish', 'monument', 'art nouveau', 'church', 'temple', 'market', 'archaeology', 'gallery', 'science', 'experiment', 'statue', 'culture', 'chocolate', 'palace', 'sport', 'basketball', 'ice', 'concert', 'stadium', 'cemetery', 'sculpture', 'walk', 'beach', 'square', 'fountain', 'park', 'town hall', 'barça', 'football', 'skyscraper']
    
   
    database = pd.read_csv('/home/sergio/Documents/MIIS/NLI/TICA-app/models/Database.csv')
    database = database.drop(labels=previous_recom, axis=0)

    #items_df

 
    if intent == "GREETING ":
        
        if name:
                answer = f'Hi again {name}!'
        else:               
                answer = "Hi! What's your name?"
                subaction = 'Greeting'

                            
    if intent == "GOODBYE ":
        answer = "Bye! See you soon!"
        
    if intent == "THANKS ":
        answer = "You are welcome!"
        
    if intent == "RECOMMENDATION ":
        items_rec = items_df['Positive'][0]
        recom = recommendations(items_rec, database)
        if len(recom) == 0:
            answer = "I need to know more about you. why don't you try to tell me what you like?"
        else:
            recom = Counter(recom)
            recom = recom.most_common(1)[0][0]
            Name = database["Name"][recom]
            Description = database["Description"][recom]
            answer = f'You would enjoy {Name}, {Description}. Do you think it is a good idea?'
            previous_recom.append(recom)
            subaction = 'recommendation'
        
    if intent == "ADD_INFO Positive":
        item = detect_item(user_input, keywords)
        if item == None:
            answer = 'What else do you like?'
        else:
            
            answer =  add_info_pos_answer(item) + 'What else do you like?'
            lista = items_df['Positive'][0]
            lista.append(str(item))
            items_df['Positive'][0] = lista
            if len(lista) > 1:
                items_rec = items_df['Positive'][0]
                recom = recommendations(items_rec, database)
                recom = Counter(recom)
                recom = recom.most_common(1)[0][0]
                Name = database["Name"][recom]
                Description = database["Description"][recom]
                previous_recom.append(recom)
                if len(previous_recom)<2:
                    answer = f'{ add_info_pos_answer(item)}. Oh wait! I have an idea! I think maybe you would enjoy {Name}, {Description}. Sound good to you?'
                else:
                    answer = f"{ add_info_pos_answer(item)}. Ok I'm going to try again. I think maybe you would enjoy {Name}, {Description}. What do you think about the idea?"
                subaction = 'recommendation'
        
    if intent == "ADD_INFO Negative":
        item = detect_item(user_input, keywords)
        if item == None:
            answer = 'I see! So what do you really like?'
        else:
            answer = f'Sure!, No {item} today'
            lista = items_df['Negative'][0]
            lista.append(str(item))
            items_df['Negative'][0] = lista
            print(items_df)

        
    return answer, subaction, previous_recom

def sub_greeting(user_input, voice):
    name = take_name(user_input)
    if name == None:
        answer = "Sorry, I didn't understand you. Could you repeat your name, please?"
        subaction = 'Greeting'
    else:
        answer = f"Hi {name}, I'm Hermes, how can i help you?"
        subaction = False
    return answer, name, subaction


def sub_timetable(intent, user_input, items_df, voice, previous_recom):
    subaction = 'Timetable'
    weekdays = ['Monday' ,'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = detect_day(user_input, weekdays)
    database = pd.read_csv('/home/sergio/Documents/MIIS/NLI/TICA-app/models/Database.csv')
    database = database.drop(labels=previous_recom[:-1], axis=0)
    items_rec = items_df['Positive'][0]
    recom = recommendations(items_rec, database)
    recom = Counter(recom)
    recom = recom.most_common(1)[0][0]
    time = database["Time"][recom]
    Name = database["Name"][recom]

    if time == "open at all times" or time == "temporarily closed":
        return f"{Name} is {time}", False
    indices = [m.start() for m in re.finditer('\(', time)]
    indices.append(time.index(day))
    indices.sort()
    timetable = indices.index(time.index(day))
    new_time = re.findall("\((.*?)\)", time)[timetable]
    if(new_time == "closed"):
        answer = f"On {day}, {Name} is closed"
    else:
        answer = f"On {day}, {Name} is open {new_time}"
    subaction = False

    return answer, subaction

def sub_ask_timetable(intent):
    subaction = 'Ask_timetable'

    if intent == "CONFIRM ":
     
        answer = f"Which day of the week are you visiting?"
        subaction = 'Timetable'
    
    elif intent == "REJECT ":
        answer = "okay! I see that it is not necessary! Have a great stay!"
        subaction = False
        
    else:
        answer = "Sorry I didn't understand you"
    return answer, subaction


def sub_location(intent, user_input, items_df, voice, previous_recom):
    subaction = 'Location'

    if intent == "CONFIRM ":
        
        database = pd.read_csv('/home/sergio/Documents/MIIS/NLI/TICA-app/models/Database.csv')
        database = database.drop(labels=previous_recom[:-1], axis=0)
        items_rec = items_df['Positive'][0]
        recom = recommendations(items_rec, database)
        recom = Counter(recom)
        recom = recom.most_common(1)[0][0]
        Name = database["Name"][recom]
        Location = database["District"][recom]
        answer = f"Sure! The {Name} is located in {Location}. Would you like to know the timetable?"
        subaction = 'Ask_timetable'

        
    elif intent == "REJECT ":
        answer = "Wow! I see that you already know the city! Would you like to know the timetable?"
        subaction = 'Ask_timetable'
        
    else:
        answer = "Sorry I didn't undertand you"
    return answer, subaction



def sub_recommendation(intent, user_input, items_df, voice, previous_recom):
    subaction = 'recommendation'

    if intent == "CONFIRM ":
        
        database = pd.read_csv('/home/sergio/Documents/MIIS/NLI/TICA-app/models/Database.csv')
        database = database.drop(labels=previous_recom[:-1], axis=0)
        items_rec = items_df['Positive'][0]
        recom = recommendations(items_rec, database)
        recom = Counter(recom)
        recom = recom.most_common(1)[0][0]
        Price = database["Price"][recom]
        answer = f"Great! the fees for visiting is {Price}. Would you like to know the location?"
        subaction = 'Location'
        
    elif intent == "REJECT ":
        answer = "Oh I'm sorry. Maybe you can try to give me more information about what you want to do"
        subaction = False
        
    else:
        answer = "Don't be rude... I'd like to know if it's okay with you"


        
    return answer, subaction

def sub_info_pos(item, voice):
    
    answer = f"Hi {name}, I'm Hermes, how can I help you?"
    subaction = False
    return answer, name, subaction

def sub_info_neg(item, voice):
    
    answer = f"Hi {name}, I'm Hermes, how can I help you?"
    subaction = False
    return answer, name, subaction


def detect_item(inpt, keywords):
    item = None
    doc = nlp(inpt)
    for token in doc:
        if token.lemma_.lower() in keywords:
            item = token.lemma_.lower()        
    return item

def detect_day(inpt, weekday):
    item = None
    doc = nlp(inpt)
    for token in doc:
        if token.lemma_ in weekday:
            item = token.lemma_        
    return item

def recommendations(user_labels, df):
    items = []
    for i in range(len(user_labels)):
        for j in df.index:
            user_label_2 = "[" + user_labels[i] + "]"
            if user_label_2 in df["Labels"][j]:
                items.append(j)
    return items

def take_name(user_input):
    doc = nlp(user_input)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return None
        


