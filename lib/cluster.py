import math
import asyncio
import nltk
import time
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from feed import feedReader
from constants import *

class Cluster:

    def __init__(self):
        sites = readCsv()
        feed = feedReader(sites)
        self.clusters = []
        self.feeds = feed.main()
        self.stopwords = set(stopwords.words('english'))
        self.flatList = self.flattenList()
        # print(self.flatList)
        self.clusterArticles()
        self.clusterClusters()
        writeClustersToFile(self.clusters)
    
    def flattenList(self):
        flatList = []
        for feed in self.feeds:
            for article in feed:
                flatList.append(article)
        return flatList

    def clusterArticles(self):
        clearFile()
        clusterNumber = -1
        for feedA in self.flatList:
            try:
                if feedA['cluster'] > clusterNumber:
                    clusterNumber = feedA['cluster'] 
            except KeyError:
                clusterNumber += 1
                feedA['cluster'] = clusterNumber
                try:
                    self.clusters.insert(clusterNumber, self.clusters[clusterNumber].append(feedA))
                except IndexError:
                    self.clusters.insert(clusterNumber, [feedA])
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
                        self.clusters[clusterNumber].append(feedB)
                    # putInFile(feedA,feedB,articleMatrix,cosine,dice)
        # writeToFile(sorted(self.flatList, key = lambda i: i['cluster']))
        # writeClustersToFile(self.clusters)

    def clusterClusters(self):
        for clusterA in self.clusters:
            indexA = self.clusters.index(clusterA)
            feedA = self.articlefy(clusterA)
            for clusterB in self.clusters:
                if clusterA ==  clusterB:
                    continue
                feedB = self.articlefy(clusterB)
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
                if cosine >= COSINE_RE_THRESHOLD and dice >= DICE_RE_THRESHOLD:
                    clusterC = clusterA + clusterB
                    self.clusters[indexA] = clusterC
                    feedA = self.articlefy(clusterC)
                    self.clusters.remove(clusterB)

    def articlefy(self, cluster):
        retDict = {'title':'','summary':''}
        for feed in cluster:
            retDict['title'] = retDict['title'] + ' ' + feed.get('title')
            retDict['summary'] = retDict['summary'] + ' ' + feed.get('summary')
        return retDict

    def calculateCosine(self, A, B, AND):
        return (AND)/math.sqrt(A*B)
    
    def calculateDice(self, A, B, AND):
        return (AND*2)/(A+B)
    
    def makeMatrix(self, articleA, articleB):
        matrix = {}
        stemmer = PorterStemmer()
        articleStringA = articleA.get('title') + ' ' + articleA.get('summary')
        articleArrayA = articleStringA.split()
        stemmedArticleArrayA = []
        for item in articleArrayA:
            stemmedArticleArrayA.append(stemmer.stem(item))
        articleStringB = articleB.get('title') + ' ' + articleB.get('summary')
        articleArrayB = articleStringB.split()
        stemmedArticleArrayB = []
        for item in articleArrayB:
            stemmedArticleArrayB.append(stemmer.stem(item))
        words = stemmedArticleArrayA + stemmedArticleArrayB
        for word in words:
            if word in self.stopwords:
                continue
            if word in matrix.keys():
                pass
            if word in stemmedArticleArrayA and word in stemmedArticleArrayB:
                matrix[word] = [1,1]
            elif word in stemmedArticleArrayA:
                matrix[word] = [1,0]
            elif word in stemmedArticleArrayB:
                matrix[word] = [0,1]
        return matrix

s = time.perf_counter()
cluster = Cluster()
elapsed = time.perf_counter() - s
print(f"Executed in {elapsed:0.2f} seconds.")
