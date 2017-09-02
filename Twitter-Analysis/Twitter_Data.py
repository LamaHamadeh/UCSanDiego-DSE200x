#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 10:12:23 2017

@author: lamahamadeh
"""

'''
Twitter API Access
------------------
Twitter offers a Web Application Programming Interfact (API) to access all 
tweets on their website.
Send queries via web to twitter's servers for tweets based on: users, locations,
trends, search terms and hashtags.
It requires authentication.

Twitter implements OAuth 1.0A as its standard authentication mechanism, and in 
order to use it to make requests to Twitter's API, you'll need to go to 
https://dev.twitter.com/apps and create a sample application. This app 
identifies all the request that are sent ot the platform.
Choose any name for your application, write a description and use 
http://google.com for the website.
Under Key and Access Tokens, there are four primary identifiers you'll need to 
note for an OAuth 1.0A workflow:
    
consumer key,
consumer secret,
access token, and
access token secret (Click on Create Access Token to create those).

Note that you will need an ordinary Twitter account in order to login, create 
an app, and get these credentials.
'''

#Creating a Twitter application
import pickle
import os

if not os.path.exists('secret_twitter_credentials.pkl'):
    Twitter = {}
    Twitter['Consumer Key'] = ''
    Twitter['Consumer Secret'] = ''
    Twitter['Access Token'] = ''
    Twitter['Access Token Secret'] = ''
    with open ('secret_twitter_credentials.pkl', 'wb') as f:
        pickle.dump(Twitter, f)
else:
        Twitter = pickle.load(open('secret_twitter_credentials.pkl','rb'))
        
#Twitter Python Package (should be installed in using the command window
#before preoceeding: pip install twitter)
        
#create a API object: Authorising an application to access Twitter account data

import twitter

auth = twitter.oauth.OAuth(Twitter['Access Token'],
                           Twitter['Access Token Secret'],
                           Twitter['Consumer Key'],
                           Twitter['Consumer Secret'])

twitter_api = twitter.Twitter(auth = auth)

print(twitter_api)

#-----------------------------

#Retrieving Trends

'''
Twitter identifies locations using the Yahoo! Where On Earth ID.
The Yahoo! Where On Earth ID for the entire world is 1. 
See https://dev.twitter.com/docs/api/1.1/get/trends/place and 
http://developer.yahoo.com/geo/geoplanet/
look at the BOSS placefinder here: 
https://developer.yahoo.com/boss/placefinder/
'''
WORLD_WOE_ID = 1 #the WOEID for the word is always 1
UK_WOE_ID = 23424975 #WOEID for UK
LOCAL_WOE_ID=30720 #WOEID for Nottingham City
#I have obtained the above ids form: http://woeid.rosselliot.co.nz/

# Prefix ID with the underscore for query string parameterization.
# Without the underscore, the twitter package appends the ID value
# to the URL itself as a special case keyword argument.
world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID) #this gives us the top 50 trends
uk_trends = twitter_api.trends.place(_id=UK_WOE_ID)
local_trends = twitter_api.trends.place(_id=LOCAL_WOE_ID)

print(local_trends[:2]) #the first two records

trends = local_trends
print(type(trends),'\n') #twitter list
print('********************************')
print(list(trends[0].keys()),'\n')
print('********************************')
print(trends[0]['trends'],'\n') #trends for the first object
print('********************************')

#Displaying API responses as pretty-printed JSON
import json
print((json.dumps(local_trends[:2], indent = 1)))#dumps function creates a 
#better verison of the output

#Computing the intersection of two sets of trends
trends_set = {}
trends_set['world'] = set([trend['name']
                        for trend in world_trends[0]['trends']])

trends_set['uk'] = set([trend['name']
                        for trend in uk_trends[0]['trends']])
    
trends_set['nottingham'] = set([trend['name']
                        for trend in local_trends[0]['trends']])
    
    
for loc in ['world', 'uk', 'nottingham']:
    print(('-'*10, loc))
    print((','.join(trends_set[loc])))
    
print(('='*10, 'intersection of world and uk'))
print((trends_set['world'].intersection(trends_set['uk'])))

print(('='*10, 'intersection of uk and nottingham'))
print((trends_set['uk'].intersection(trends_set['nottingham'])),'\n','\n')

#-----------------------------

#Collecting search results
q = '#PrincessDiana'

number = 100

search_results = twitter_api.search.tweets(q = q, count = number)

statuses = search_results['statuses']

print(len(statuses))
print(statuses)

all_text = []
filtered_statuses =[]
for s in statuses:
    if not s['text']in all_text:
        filtered_statuses.append(s)
        all_text.append(s['text'])
statuses = filtered_statuses

print(len(statuses))

[s['text'] for s in search_results['statuses']]

print(json.dumps(statuses[0], indent = 1))

t = statuses[0]

print(t['retweet_count'])
print(t['retweeted'])

#-----------------------------

#Extracting text, screen names and hastags

status_texts = [status['text']
                for status in statuses]

screen_names = [user_mention['screen_name']
                for status in statuses
                    for user_mention in status['entities']['user_mentions']]
    
hashtags = [hashtag['text']
            for status in statuses
                for hashtag in status['entities']['hashtags']]

words = [w
        for t in status_texts
            for w in t.split()]

print(json.dumps(status_texts[0:5], indent = 1))
print(json.dumps(screen_names[0:5], indent = 1))
print(json.dumps(hashtags[0:5], indent = 1))
#print(json.dumps(words[0:5], indent = 1))

#-----------------------------

#Creating a basic frequency distribution from the words in tweets

from collections import Counter

for item in [words, screen_names, hashtags]:
    c = Counter(item)
    print(c.most_common()[:10])
    print()

#-----------------------------
    
#Create a prettyprint function to display tuples in a nice tabluar format

def prettyprint_counts(label, list_of_tuples):
    print('\n{:^20} | {:^6}'.format(label, 'Count'))
    print('*'*40)
    for k,v in list_of_tuples:
        print('{:20} | {:>6}'.format(k,v))


for label, data in (('Word', words),('Screen Name',screen_names),
                    ('Hashtags', hashtags)):
    c = Counter(data)
    prettyprint_counts(label, c.most_common()[:10])

#-----------------------------

#Finding the most popular retweets

retweets = [(status['retweet_count'], status['retweet_status']['user']
            ['screen_name'], status['text'].replace('\n', '\\'))
            for status in statuses
                if 'retweet_status' in status
            ]

row_template = '{:^7} | {:^15} | {:50}'

def prettyprint_tweets(list_of_tuples):
    print()
    print(row_template.format('Count', 'Screen Name', 'Text'))
    print('*'*60)
    for count, screen_name, text in list_of_tuples:
        print(row_template.format(count, screen_name, text[:50]))
        if len(text) > 50:
            print(row_template.format('', '', text[50:100]))
            if len(text) > 100:
                print(row_template.format('', '', text[100:]))
                
prettyprint_tweets(sorted(retweets, reverse = True)[:10])

#-----------------------------    
