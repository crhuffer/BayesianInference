# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 10:52:10 2019

@author: crhuffer
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

class Jar:
    '''A base object for sampling from'''
    
    def __init__(self, itemDict, name):
        self.itemDict = itemDict
        self.name = name
        self.items = np.array([])
        for itemType in itemDict.keys():
            self.items = np.append(self.items, [itemType]*itemDict[itemType])
    
    def SampleWithReplace(self):
        return np.random.choice(self.items)
    
class FairDie:
    
    def __init__(self, numsides, name):
        self.numsides = numsides
        self.name = name
    
    def roll(self):
        return np.random.choice(range(self.numsides))+1

class UnfairDie:
    
    def __init__(self, probabilities, name):
        # probabilities should add to 1, let us correct for that
        probabilities = pd.Series(probabilities)
        currentsum = probabilities.sum()
        probabilities = probabilities.apply(lambda x: math.floor(x*100.0/currentsum))
        self.probabilities = probabilities
        
        # We are going to approximate the solution to the 1% level
        # we will sample from 1 to 100 and assign each side some fraction
        # of those values. Then we will map from the percentile to the side
        self.dictMapping = {}
        counter = 0
        for side in range(len(self.probabilities)):
            for probability in range(self.probabilities[side]):
                self.dictMapping[counter] = side
                counter += 1
                
        self.name = name
    
    def roll(self):
        return self.dictMapping[np.random.randint(0, 100)]+1
    

# %% Test a fair die

Die1 = FairDie(6, 'A')
Die1.roll()

# %% Test a unfair die

Die2 = UnfairDie([10, 10, 10, 10, 10, 50], 'B')
Die2.roll()

# %% Test a second unfair die

Die3 = UnfairDie([0, 0, 0, 0, 0, 100], 'C')
Die3.roll()

# %% Run the dice experiment

# There are 5 fair die and 1 unfair die in a bag
Dies = [FairDie(6, 'A'), FairDie(6, 'B'), FairDie(6, 'C'), FairDie(6, 'D'),
        FairDie(6, 'E'), UnfairDie([0, 0, 0, 0, 0, 100], 'F')]


listDieName = []
listDieSideTry1 = []
listDieSideTry2 = []
# try many times
for index in range(1000000):
    # for each try sample a random die
    currentDie = np.random.choice(Dies)
    currentDieName = currentDie.name
    listDieName.append(currentDieName)
    # roll that die twice
    listDieSideTry1.append(currentDie.roll())
    listDieSideTry2.append(currentDie.roll())

# %% Setup the data in a dataframe
    
df = pd.DataFrame(listDieSideTry1, columns=['SideTry1'])
df['SideTry2'] = listDieSideTry2
df['Die'] = listDieName

# %% Print the probabilities for each die

indexer = ((df['SideTry1'] == 6 ) & (df['SideTry2'] == 6))
currentsum = df.loc[indexer, 'Die'].value_counts().sum()
df.loc[indexer, 'Die'].value_counts()/currentsum

# %% Jar of cookies example
# %% Setup the jars
        
Jar1 = Jar({'Vanilla': 10, 'Chocolate': 30}, 'A')
Jar2 = Jar({'Vanilla': 20, 'Chocolate': 20}, 'B')

# %% Inspect the list of items in Jar1

Jar1.items

# %% Example of sampling from the Jar

print(Jar1.SampleWithReplace())

# %% For some number of attempts pick a Jar and sample a cookie
# record what jar was picked and what cookie to use later 

Jars = np.array([Jar1, Jar2])
listJars = []
listCookies = []
for attempt in range(100000):
    currentJar = np.random.choice(Jars)
    listJars.append(currentJar.name)
    currentCookie = currentJar.SampleWithReplace()
    listCookies.append(currentCookie)
    
# %% Put the results into a dataframe
    
df = pd.DataFrame(listCookies, columns=['Cookie'])
df['Jar'] = listJars

# %% Count the number of cases of Vanilla for each jar
# Use to calculate the probability of it being Jar A if Vanilla is pulled.

# Select Vanilla pulls from Jar B
indexer = ((df['Cookie'] == 'Vanilla') & (df['Jar'] == 'B'))
Pb = df.loc[indexer, :].count()
# Select Vanilla pulls from Jar A
indexer = ((df['Cookie'] == 'Vanilla') & (df['Jar'] == 'A'))
Pa = df.loc[indexer, :].count()

print('ProbA:', Pa/(Pa+Pb))