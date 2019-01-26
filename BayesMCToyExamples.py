# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 10:52:10 2019

@author: crhuffer
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
        return np.random.choice(range(self.numsides)+1)
    

# %%



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