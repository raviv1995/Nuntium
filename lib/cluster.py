import math
import asyncio
import nltk
import time
from nltk.corpus import stopwords
from feed import feedReader
from constants import *

class Cluster:

    def __init__(self):
        sites = ['http://feeds.bbci.co.uk/news/rss.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'http://feeds.reuters.com/reuters/INtopNews']
        feed = feedReader(sites)
        self.feeds = feed.main()
        self.stopwords = set(stopwords.words('english'))
        self.flatList = self.flattenList()
        # print(self.flatList)
        self.clusterArticles()
    
    def flattenList(self):
        flatList = []
        for feed in self.feeds:
            for article in feed:
                flatList.append(article)
        return flatList

    def clusterArticles(self):
        clearFile()
        clusterNumber = 0
        for feedA in self.flatList:
            clusterNumber += 1
            try:
                if not feedA['cluster']<clusterNumber:
                    feedA['cluster'] = clusterNumber
            except KeyError:
                feedA['cluster'] = clusterNumber
            for feedB in self.flatList:
                if feedA == feedB:
                    continue
                else:
                    articleMatrix = self.makeMatrix(feedA, feedB)
                    AND = 0
                    A = 0
                    B = 0
                    for word in articleMatrix.keys():
                        value = articleMatrix.get(word)
                        if value == [1,1]:
                            A += 1
                            B += 1
                            AND += 1
                        elif value == [1,0]:
                            A += 1
                        elif value == [0,1]:
                            B += 1
                    cosine = self.calculateCosine(A,B,AND)
                    dice = self.calculateDice(A,B,AND)
                    if cosine >= COSINE_THRESHOLD and dice >= DICE_THRESHOLD:
                        feedB['cluster'] = clusterNumber
                    # putInFile(feedA,feedB,articleMatrix,cosine,dice)
        writeToFile(sorted(self.flatList, key = lambda i: i['cluster']))    

    def calculateCosine(self, A, B, AND):
        return (AND)/math.sqrt(A*B)
    
    def calculateDice(self, A, B, AND):
        return (AND*2)/(A+B)
    
    def makeMatrix(self, articleA, articleB):
        matrix = {}
        articleStringA = articleA.get('title') + ' ' + articleA.get('summary')
        articleArrayA = articleStringA.split()
        articleStringB = articleB.get('title') + ' ' + articleB.get('summary')
        articleArrayB = articleStringB.split()
        words = articleArrayA + articleArrayB
        for word in words:
            if word in self.stopwords:
                continue
            if word in matrix.keys():
                pass
            if word in articleArrayA and word in articleArrayB:
                matrix[word] = [1,1]
            elif word in articleArrayA:
                matrix[word] = [1,0]
            elif word in articleArrayB:
                matrix[word] = [0,1]
        return matrix

s = time.perf_counter()
cluster = Cluster()
elapsed = time.perf_counter() - s
print(f"Executed in {elapsed:0.2f} seconds.")