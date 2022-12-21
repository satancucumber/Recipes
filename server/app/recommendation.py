from playhouse.postgres_ext import *
from server.app.models import BaseModel, StrFavorite, StrFridge
import pandas as pd
import math

def ReadData():
    mentions = dict()
    query = StrFavorite.select()
    str_selected = query.dicts().execute()
    for line in str_selected:
        user_id = line["userid"]
        recipes_id = line["recipesid"]
        if not user_id in mentions:
            mentions[user_id] = dict()
        for i in range(len(recipes_id)):
            mentions[user_id][i+1] = recipes_id[i]
    return mentions


def distCosine(vecA, vecB):
    def dotProduct(vecA, vecB):
        d = 0.0
        for dim in vecA:
            if dim in vecB:
                d += vecA[dim]*vecB[dim]
        return d
    return dotProduct (vecA,vecB) / math.sqrt(dotProduct(vecA,vecA)) / math.sqrt(dotProduct(vecB,vecB))


def makeRecommendation (userID, userRates, nBestUsers, nBestProducts):
    matches = [(u, distCosine(userRates[userID], userRates[u])) for u in userRates if u != userID]
    bestMatches = sorted(matches, key=lambda x, y: (y, x), reverse=True)[:nBestUsers]
    print("Most correlated with '%s' users:" % userID)
    for line in bestMatches:
        print("  UserID: %6s  Coeff: %6.4f" % (line[0], line[1]))
    sim = dict()
    sim_all = sum([x[1] for x in bestMatches])
    bestMatches = dict([x for x in bestMatches if x[1] > 0.0])
    for relatedUser in bestMatches:
        for product in userRates[relatedUser]:
            if not product in userRates[userID]:
                if not product in sim:
                    sim[product] = 0.0
                sim[product] += userRates[relatedUser][product] * bestMatches[relatedUser]
    for product in sim:
        sim[product] /= sim_all
    bestProducts = sorted(sim.iteritems(), key=lambda x, y: (y, x), reverse=True)[:nBestProducts]
    print("Most correlated products:")
    for prodInfo in bestProducts:
        print("  ProductID: %6s  CorrelationCoeff: %6.4f" % (prodInfo[0], prodInfo[1]))
    return [(x[0], x[1]) for x in bestProducts]


rec = makeRecommendation(2, ReadData(), 1, 1)


