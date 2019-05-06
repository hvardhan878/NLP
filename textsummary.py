#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 20:26:11 2019

@author: harsh
"""

import numpy as np
import matplotlib.pyplot as plt
import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


Path = '/Users/harsh/Desktop/NLP/annualreport.pdf'

file = open(Path, 'rb')

# Create a pdf reader .
annualreport = PyPDF2.PdfFileReader(file)

# Get total pdf page number.
total = annualreport.numPages

currentPage = 1
 
text = ''

# Loop in all the pdf pages.
while(currentPage < total ):

    # Get the specified pdf page object.
    pdfPage = annualreport.getPage(currentPage)

    text = text + pdfPage.extractText()

    currentPage += 1

#cleaning the text
import re
cleantext = re.sub('[^a-zA-Z]',' ',text)
cleantext = re.sub(r'\s+', ' ', cleantext) 
cleantext = cleantext.lower()
sentences = nltk.sent_tokenize(text) 

#remove extra words/stopwords
stopwords = nltk.corpus.stopwords.words('english')
frequencies = {}  
for word in nltk.word_tokenize(cleantext):  
    if word not in stopwords:
        if word not in frequencies.keys():
            frequencies[word] = 1
        else:
            frequencies[word] += 1

maxfreq = max(frequencies.values())


for word in frequencies.keys():  
    frequencies[word] = (frequencies[word]/maxfreq)

sentence_scores = {}  
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in frequencies.keys():
            if len(sentence.split(' ')) < 30:
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = frequencies[word]
                else:
                    sentence_scores[sentence] += frequencies[word]


import heapq  
summary_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)  
print(summary) 







