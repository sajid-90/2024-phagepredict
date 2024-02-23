# -*- coding: utf-8 -*-
"""KerasTuner.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eGTGLaNtb5iN6NaTj0DMto2oFihEptSy
"""

pip install Bio

# Commented out IPython magic to ensure Python compatibility.
from Bio import SeqIO
from sklearn.metrics import confusion_matrix,classification_report
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
# %matplotlib inline
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Dense, Input, Flatten
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Embedding, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import Sequential

from google.colab import drive
drive.mount('/content/drive')



neg_seq = []
neg_id= []

for seq_record in SeqIO.parse("/content/drive/MyDrive/Colab Notebooks/TRneg250.txt", "fasta"):
    neg_seq.append(str(seq_record.seq))
    neg_id.append(str(seq_record.id))
pos_seq = []
pos_id= []

for seq_record in SeqIO.parse("/content/drive/MyDrive/Colab Notebooks/TRpos250.txt", "fasta"):
    pos_seq.append(str(seq_record.seq))
    pos_id.append(str(seq_record.id))
seqs=pos_seq + neg_seq
dfclass = pd.DataFrame({'class' :  np.repeat((1,0), (250, 250))})
y=dfclass['class']
print(seqs)

Indneg_seq = []
Indneg_id= []

for Indseq_record in SeqIO.parse("/content/drive/MyDrive/Colab Notebooks/TSneg63.txt", "fasta"):
    Indneg_seq.append(str(Indseq_record.seq))
    Indneg_id.append(str(Indseq_record.id))
Indpos_seq = []
Indpos_id= []

for Indseq_record in SeqIO.parse("/content/drive/MyDrive/Colab Notebooks/TSpos63.txt", "fasta"):
    Indpos_seq.append(str(Indseq_record.seq))
    Indpos_id.append(str(Indseq_record.id))

Indseqs=Indpos_seq + Indneg_seq
Inddfclass = pd.DataFrame({'class' :  np.repeat((1,0), (63, 63))})
z=Inddfclass['class']
print(Indseqs)

pip install keras-tuner --upgrade

import keras_tuner as kt

max_words = 5000
max_len = 350
tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(seqs)
sequences = tok.texts_to_sequences(seqs)
sequences_matrix = sequence.pad_sequences(sequences,maxlen=max_len)

#Independent Testing
indtok = Tokenizer(num_words=max_words)
indtok.fit_on_texts(Indseqs)
Indsequences = indtok.texts_to_sequences(Indseqs)
Indsequences_matrix = sequence.pad_sequences(Indsequences,maxlen=max_len)
X_train=sequences_matrix
y_train=y
X_test=Indsequences_matrix
y_test=z

import keras_tuner as kt
from tensorflow import keras

def build_model(hp):
  model = keras.Sequential()
  model.add(keras.layers.Dense(hp.Choice('units', [2, 4, 8, 16, 32, 64, 128]),activation='relu'))
  model.add(keras.layers.Dense(1, activation='sigmoid'))
  model.compile(loss='binary_crossentropy',metrics=['accuracy'])
  return model

tuner1 = kt.RandomSearch(
    build_model,
    overwrite=True,
    objective='val_accuracy',
    max_trials=10,
    directory='./multiclass_classifier/training')

tuner1.search(X_train, y_train, epochs=20, validation_data=(X_test, y_test))
best_model = tuner1.get_best_models()[0]

tuner1.results_summary()

best_model.build(X_train.shape)
best_model.summary()

accr = best_model.evaluate(X_test,y_test)
print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}'.format(accr[0],accr[1]))

pred=best_model.predict(X_test)
pred1 = np.round_(pred)

from sklearn.metrics import matthews_corrcoef as mcc
mc=mcc(y_test, pred1)
print("MCC: ",mc)
from sklearn.metrics import confusion_matrix as cm
cm(y_test, pred1)

from sklearn.metrics import matthews_corrcoef as mcc
mc=mcc(y_test, pred1)
print("MCC: ",mc)
from sklearn.metrics import confusion_matrix as cm
cm(y_test, pred1)
print(classification_report(y_test, pred1))
tp, fn, fp, tn = confusion_matrix(y_test, pred1).ravel()
print("MCC ---> {0}".format(mc))
print("Confusion Matrix. tn, fp, fn, tp ---> ", tp, fn, fp, tn)
print("Precision --->TP/TP+Fp ", tp/(tp+fp))
print("Recall - SN - Sensitivity --->TP/TP+FN ", tp/(tp+fn))
print("Specificity - SP ---> ", tn/(tn+fp))
print("Balanced Accuracy ---> ", ((tp/(tp+fn))+(tn/(tn+fp)))/2)
print("Jaccard Index --->TP/TP+FN+FP ", tp/(tp+fn+fp))