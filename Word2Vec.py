import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import re
from collections import Counter
import sys
import math
from random import randint
import pickle
import os

# This Word2Vec implementation is largely based on this paper
# https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf
# It's a bit old, but Word2Vec is still SOTA and relatively simple, so I'm going with it

# Check out Tensorflow's documentation which is pretty good for Word2Vec
# https://www.tensorflow.org/tutorials/word2vec

wordVecDimensions = 100
batchSize = 128
numNegativeSample = 64
windowSize = 5
numIterations = 100000

# This function just takes in the conversation data and makes it
# into one huge string, and then uses a Counter to identify words
# and the number of occurences
def processDataset(filename):
    openedFile = open(filename, 'r', encoding='UTF8')
    allLines = openedFile.readlines()
    print(allLines)
    myStr = ""
    for line in allLines:
        myStr += line
    finalDict = Counter(myStr.split())
    return myStr, finalDict

def createTrainingMatrices(dictionary, corpus):
    allUniqueWords = list(dictionary.keys())
    allWords = corpus.split()
    numTotalWords = len(allWords)
    xTrain=[]
    yTrain=[]
    for i in range(numTotalWords):
        if i % 100000 == 0:
            print ('Finished %d/%d total words' % (i, numTotalWords))
        wordsAfter = allWords[i + 1:i + windowSize + 1]
        wordsBefore = allWords[max(0, i - windowSize):i]
        wordsAdded = wordsAfter + wordsBefore
        for word in wordsAdded:
            xTrain.append(allUniqueWords.index(allWords[i]))
            yTrain.append(allUniqueWords.index(word))
    return xTrain, yTrain

def getTrainingBatch():
    num = randint(0,numTrainingExamples - batchSize - 1)
    arr = xTrain[num:num + batchSize]
    labels = yTrain[num:num + batchSize]
    return arr, labels[:,np.newaxis]

continueWord2Vec = True
# Loading the data structures if they are present in the directory
if (os.path.isfile('Word2VecXTrain.npy') and os.path.isfile('Word2VecYTrain.npy') and os.path.isfile('wordList.txt')):
    xTrain = np.load('Word2VecXTrain.npy')
    yTrain = np.load('Word2VecYTrain.npy')
    print ('Finished loading training matrices')
    with open("wordList.txt", "rb") as fp:
        wordList = pickle.load(fp)
    print ('Finished loading word list')

else:
    fullCorpus, datasetDictionary = processDataset(r'C:\Users\dlgpd\Desktop\20-1\oss\term-project\Learn_for_yourself\chat_system\conversationData.txt')
    print ('Finished parsing and cleaning dataset')
    wordList = list(datasetDictionary.keys())
    createOwnVectors = input('Do you want to create your own vectors through Word2Vec (y/n)?')
    if (createOwnVectors == 'y'):
        xTrain, yTrain  = createTrainingMatrices(datasetDictionary, fullCorpus)
        print ('Finished creating training matrices')
        np.save('Word2VecXTrain.npy', xTrain)
        np.save('Word2VecYTrain.npy', yTrain)
    else:
        continueWord2Vec = False
    with open("wordList.txt", "wb") as fp:
        pickle.dump(wordList, fp)
