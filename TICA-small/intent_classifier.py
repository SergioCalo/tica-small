# Streamlit
import streamlit as st
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from torchtext.legacy import data
import torch
import random


#Reproducing same results
SEED = 10

#Torch
torch.manual_seed(SEED)

#Cuda algorithms
torch.backends.cudnn.deterministic = True 


TEXT = data.Field(tokenize='spacy',batch_first=True,include_lengths=True, lower=True)
LABEL = data.LabelField(dtype = torch.float,batch_first=True)
fields = [('label', LABEL), ('text',TEXT)]

path = 'intent_data_sent.csv'
training_data=data.TabularDataset(path = path, format = 'csv', fields = fields, skip_header = True)
train_data, valid_data = training_data.split(split_ratio=0.7, random_state = random.seed(SEED))
TEXT.build_vocab(train_data,min_freq=0,vectors = "glove.6B.100d")  
LABEL.build_vocab(train_data)


#Define model
from intent_classifier_model import classifier





#define hyperparameters
size_of_vocab = 227
embedding_dim = 100
num_hidden_nodes = 30
num_output_nodes = 8
num_layers = 1
bidirection = True
dropout = 0
device = torch.device('cpu')  



#instantiate the model
model = classifier(size_of_vocab, embedding_dim, num_hidden_nodes,num_output_nodes, num_layers, 
                   bidirectional = True, dropout = dropout)
model = model.to(device)



#load weights
path='saved_weights_sent.pt'
model.load_state_dict(torch.load(path));
model.eval();

#inference 

nlp = spacy.load("en_core_web_sm")

def sentiment_scores(sentence):
    
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)

    if sentiment_dict['compound'] >= 0.05 :
        return "Positive"

    elif sentiment_dict['compound'] <= - 0.05 :
        return "Negative"

    else :
        return "Neutral"

def predict_intent(sentence):
    sentiment = ''
    tokenized = [tok.text.lower() for tok in nlp.tokenizer(sentence)]  #tokenize the sentence 
    indexed = [TEXT.vocab.stoi[t] for t in tokenized]          #convert to integer sequence
    length = [len(indexed)]                                    #compute no. of words
    tensor = torch.LongTensor(indexed).to(device)              #convert to tensor
    tensor = tensor.unsqueeze(1).T                             #reshape in form of batch,no. of words
    length_tensor = torch.LongTensor(length)                   #convert to tensor
    prediction = model(tensor, length_tensor)                  #prediction 
    intent = list(LABEL.vocab.stoi)[torch.argmax(prediction)]
    if intent == 'ADD_INFO':
        sentiment = sentiment_scores(sentence)
        
    return intent + ' ' + sentiment


