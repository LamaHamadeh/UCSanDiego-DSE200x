#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 21:06:25 2017

@author: lamahamadeh
"""

# NLP on movies reviews


#--------------------Natural Language Processing with nltk---------------------

#nltk is the most popular Python package for Natural Language processing, 
#it provides algorithms for importing, cleaning, pre-processing text data in 
#human language and then apply computational linguistics algorithms like 
#sentiment analysis.

#Importing nltk
import nltk 
#--------------------

#Inspect the movie reviews dataset
nltk.download('movie_reviews') #It also includes many easy-to-use datasets in 
#the nltk.corpus package
from nltk.corpus import movie_reviews
#--------------------

#Look at the data
print(len(movie_reviews.fileids()))
print(movie_reviews.fileids()[:5])
print(movie_reviews.fileids()[-5:])

negative_fileids = movie_reviews.fileids('neg') #negative reviews
positive_fileids = movie_reviews.fileids('pos') #positive reviews

print(len(negative_fileids),len(positive_fileids))

#We can inspect one of the reviews using the raw method of movie_reviews, 
#each file is split into sentences, the curators of this dataset also removed 
#from each review from any direct mention of the rating of the movie.
print(movie_reviews.raw(fileids = positive_fileids[0]))
#--------------------

#Tokenise text in words

#Suppose we have the following text:
romeo_text = """Why then, O brawling love! O loving hate!
O any thing, of nothing first create!
O heavy lightness, serious vanity,
Misshapen chaos of well-seeming forms,
Feather of lead, bright smoke, cold fire, sick health,
Still-waking sleep, that is not what it is!
This love feel I, that feel no love in this."""

print(romeo_text.split()) #Here we can see that the split funtion doesn't work
#for separating words from punctuations. To solve this, we use the tokenisation 
#method.

nltk.download('punkt')
romeo_words = nltk.word_tokenize(romeo_text)
print(romeo_words) #W can see here that each punctuation is separated from the 
#word.

#--------------------

#Bag of words

#The simplest model for analyzing text is just to think about text as an 
#unordered collection of words (bag-of-words).
#From the bag-of-words model we can build features to be used by a classifier, 
#here we assume that each word is a feature that can either be True or False. 
print({word:True for word in romeo_words})

#another way to generalise what we are doing is to define a python function 
#def build_bag_of_words_features(words):
#    return {word:True for word in romeo_words}

#print(build_bag_of_words_features(romeo_words))

#punctuations are still showing up and they are usless for classification 
#urposes, as well as for stopwords. therefore, we can first download the 
#stopwords and then define the words that we don't want

nltk.download('stopwords')
import string
string.punctuation
#Using the Python string.punctuation list and the English stopwords we can 
#build better features by filtering out those words that would not help in the 
#classification:
useless_words = nltk.corpus.stopwords.words('english')+list(string.punctuation)
print('Uselss words for our analysis are: ',useless_words)

#Now we can filter the words between useful and useless using the following
#python function

def build_bag_of_words_features_filtered(words):
    return{word:True for word in words #here we can put either True or 1
           if not word in useless_words}
    
print(build_bag_of_words_features_filtered(romeo_words))

#--------------------

#Plotting the frequencies of words

all_words = movie_reviews.words()
print(len(all_words)/1e6)

filtered_words = [word for word in movie_reviews.words() 
                    if not word in useless_words]

print(len(filtered_words)/1e6)


from collections import Counter
word_counter = Counter(filtered_words)
most_common_words = word_counter.most_common()[:10] #this method accesses the 
#words with the highest count.
print(most_common_words)
#A Counter is a dict subclass for counting hashable objects. It is an unordered
# collection where elements are stored as dictionary keys and their counts are 
#stored as dictionary values.
#Example of counter:
#cnt = Counter()
#for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
#    cnt[word] += 1
#print(cnt)
#Counter({'blue': 3, 'red': 2, 'green': 1})
#print(cnt.most_common)
#[('blue', 3), ('red', 2), ('green', 1)]
#most_common method returns a list of the n most common elements and their 
#counts from the most common to the least.


import matplotlib.pyplot as plt

sorted_word_counts = sorted(list(word_counter.values()), reverse = True)

#loglog plot
plt.figure()
plt.loglog(sorted_word_counts)
plt.ylabel('Frequency')
plt.xlabel('Word Rank');

#Another related plot is the histogram of sorted_word_counts, which displays 
#how many words have a count in a specific range.

#histogram
plt.figure()
plt.hist(sorted_word_counts, bins=50);
plt.title('Normal Histogram')

#Of course the distribution is highly peaked at low counts, i.e. most of the 
#words appear which a low count, so we better display it on semilogarithmic 
#axes to inspect the tail of the distribution.
plt.figure()
plt.hist(sorted_word_counts, bins=50, log=True)
plt.title('Semilogarithmic Histogram')
#--------------------

#Naive Bayes Classifier(sentiment analysis)

#One of the simplest supervised machine learning classifiers is the Naive Bayes
# Classifier

#Using our build_bag_of_words_features function we can build separately the 
#negative and positive features. Basically for each of the 1000 negative and 
#for the 1000 positive review, we create one dictionary of the words and we 
#associate the label "neg" and "pos" to it.

negative_features = [(build_bag_of_words_features_filtered(movie_reviews.words(fileids = [f])),'neg')
    for f in negative_fileids]
print(negative_features)#1000 records

positive_features = [(build_bag_of_words_features_filtered(movie_reviews.words(fileids = [f])), 'pos')
    for f in positive_fileids]
print(positive_features)#1000 records

from nltk.classify import NaiveBayesClassifier

#Train the model
split = 800 #we take 80% of the data for training
sentiment_classifier = NaiveBayesClassifier.train(positive_features[:split]+
                                                  negative_features[:split])

#check the accuracy of the model
print(nltk.classify.util.accuracy(sentiment_classifier, positive_features[:split]+
                            negative_features[:split])*100)
#98.06

#predicting the labels for the rest of 20% of the data and check the accuracy 
#of the testing on the remaining data
print(nltk.classify.util.accuracy(sentiment_classifier, positive_features[split:]+
                            negative_features[split:])*100)
#71.75

#We can finally print the most informative features, i.e. the words that mostly
# identify a positive or a negative review
print(sentiment_classifier.show_most_informative_features())

#--------------------
