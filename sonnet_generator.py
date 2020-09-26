# -*- coding: utf-8 -*-
"""Copy of SONNET_GENERATOR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lgbOk88lV7eCvlg1z8hRSA-gsgYPHmZT

# **IMPORTING LIBRARIES**
"""

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import Regularizer
import tensorflow.keras.utils as ku 
from keras.callbacks import ModelCheckpoint
import numpy as np 
import tensorflow as tf
import sys
from gensim.parsing.preprocessing import remove_stopwords
import re

from google.colab import drive
drive.mount('/content/drive')

"""# **READING, TOKENIZING AND CLEANING DATA**"""

tokenizer = Tokenizer()
#Reading Data
data = open(r'/content/drive/My Drive/dataset.txt').read()

#Making sentences Lower case and spliting it 
sonnet_14 = data.lower().split("<eos>")

#Removing the un wanted terms from the data
for i in range(len(sonnet_14)):
 sonnet_14[i] = sonnet_14[i].replace("\n",'')
 sonnet_14[i] = sonnet_14[i].replace("<eos>",'')
 sonnet_14[i] = re.sub("[`~!@#$+%*:()'?-]", ' ',sonnet_14[i]) 
 sonnet_14[i] = remove_stopwords(sonnet_14[i])

"""# **GENERATE VALUES**"""

#Generating the values for the data
tokenizer.fit_on_texts(sonnet_14)
total_words = len(tokenizer.word_index) + 1
input_sequences = []
for line in sonnet_14:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_sequence = token_list[:i+1]
        input_sequences.append(n_sequence)

max_sequence = max([len(x) for x in input_sequences])#selecting the maximum input sequence length
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence, padding='pre'))#padding prior zeros to the input sequence

predictors, label = input_sequences[:,:-1],input_sequences[:,-1]#splitting the data into predictor and label
                                                                                  
label = ku.to_categorical(label, num_classes=total_words)#making the variables to be either 0 or 1

"""# **CREATING A MODEL AND ITS LAYERS**"""

model = Sequential() #Using sequential model
model.add(Embedding(total_words, 50, input_length=max_sequence-1))  # Your Embedding Layer
model.add(Bidirectional(LSTM(150, return_sequences=True)))  # An LSTM Layer
model.add(Dropout(0.2))  #(# A dropout layer)
model.add(LSTM(100))  #(# Another LSTM Layer)
model.add(Dense(total_words/2, activation='relu'))  # A Dense Layer including regularizers
model.add(Dense(total_words, activation='softmax'))  # A Dense Layer
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])  # Pick a loss function and an optimizer)

"""# **TRAINING THE DATA**"""

train=model.fit(predictors,label,epochs=100,verbose=1)#traing the model on 100 epochs

"""# **SAVING THE TRAINED MODEL**"""

# serialize model to JSON
model_json = model.to_json()
with open("jack1.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

"""# **LOADING TRAINED MODEL AND PREDICTION**"""

#to read the .json and HDF5 file from the drive
from tensorflow.keras.models import model_from_json
json_file = open('/content/drive/My Drive/jack1.json','r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights('/content/drive/My Drive/model.h5')
model = loaded_model
#Feeding the trained model to predict the words
def predict(seed_text , seed = 625):
    for i in range( seed ):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=
        max_sequence , padding='pre')
        predicted = model.predict_classes(token_list, verbose=0 )
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
        if i!=1 and i!=0:
          if i%13==0:
            seed_text+='\n'
    return seed_text


#Giving input and printing the sonnet
sonnet_14 = input()
tk=predict(sonnet_14)
nxt=tk.split("\n")[1:15]
for i in range(len(d)):  
  d[i] = re.sub("[,`~!@#$+%*:()'?-]", '',d[i])
gt=d.pop(0).split(" ")
if(gt[0].lower()=='d' or gt[0].lower()=='s'or gt[0].lower()=='è'):gt[0]="As"
for i in([" ".join(gt).capitalize()]+nxt):
  print(i)

