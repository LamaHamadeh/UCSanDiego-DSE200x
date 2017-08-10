#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 16:20:38 2017

@author: lamahamadeh
"""

#importing libraries
#-------------------
import pandas as pd #pandas
import matplotlib.pyplot as plt #matplotlib
from matplotlib import style #style
style.use("ggplot") #look pretty



#reading the movie dataframe
#----------------------------
Mov = pd.read_csv('/Users/lamahamadeh/Downloads/ml-20m/movies.csv')
print('First DataFrame (movie)')
print('**********************')
print ('Shape', Mov.shape) #(27278, 3)
print (Mov.head(5))
print (Mov.describe())
def num_missing(x):
  return sum(x.isnull())
#Applying per column:
print ("Missing values per column:")
print (Mov.apply(num_missing, axis=0)) #no NANs
print(Mov.columns)
print('---------------')
Mov['year'] = Mov['title'].str.extract('.*\((.*)\).*',expand = True) #Here we have separated the 'year' from the tilte column and put it in a complete new column.
print(Mov.head())
print('-------------------------------------')

#Read the ratings dataframe
#----------------------------
rat = pd.read_csv('/Users/lamahamadeh/Downloads/ml-20m/ratings.csv')
print('Second DataFrame (ratings)')
print('*************************')
print ('Shape',rat.shape) #(20000263, 4)
print (rat.tail(4))
print (rat.describe())
def num_missing(x):
  return sum(x.isnull())
#Applying per column:
print ("Missing values per column:") 
print (rat.apply(num_missing, axis=0)) #no NANs
del rat['timestamp'] 
print(rat.columns)
print('-------------------------------------')


#Add the ratings column to the movie dataframe
#----------------------------------------------
print('Box Office DataFrame') #in this new dataframe I have joined/merged the movies and the ratings dataframes after taking the mean value of ratings for each ID movie 
print('********************')
#Calculate the mean value of the ratings for each movie ID
#---------------------------------------------------------
avg_rat = rat.groupby('movieId', as_index = False).mean()

box_office = Mov.merge(avg_rat, on = 'movieId', how = 'inner')
print ('Shape',box_office.shape)
print(box_office.head(5))
print(box_office.tail(5))
#box_office.hist('rating',color='blue')
print('-------------------------------------')

print('Documentary DataFrame') #this dataframe contains only the documentary movies and the correspondant ratings.
print('********************')
Doc = box_office [(box_office.genres == 'Documentary')]
print(Doc.head(5))
print(Doc.tail(5))
print(Doc.shape)
print (Doc.dtypes) #It can be seen here that 'year' ahs an 'object' type. Therefore, it it bettwe to change it to a numeric type
#Changing the type of year from 'Object' to 'numeric' to be able to plot it
Doc['year'] = pd.to_numeric(Doc['year'], errors='coerce')
print('Year Min:', Doc['year'].min(), 'Year Max:', Doc['year'].max())
print (Doc.dtypes)
print('-------------------------------------')

#Data Visulisation
#-------------------
plt.scatter(x=Doc['year'],y=Doc['rating'],color = 'blue')
plt.title('Documentary Movies Rating From 1894 Until 2015')
plt.xlabel('Year')
plt.ylabel('Rating')
plt.grid(True)
plt.show()
print('-------------------------------------')


