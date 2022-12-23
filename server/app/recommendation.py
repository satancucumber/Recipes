from playhouse.postgres_ext import *
from server.app.models import BaseModel, StrFavorite, StrFridge, StrIngredient, User
import pandas as pd
import math

def ReadDataIngredient():
    mentions = dict()
    query = StrIngredient.select()
    str_selected = query.dicts().execute()
    for line in str_selected:
        recipe_id = line["recipeid"]
        ingredients_id = line["ingredientsid"]
        if not recipe_id in mentions:
            mentions[recipe_id] = dict()
        for i in range(len(ingredients_id)):
            if ingredients_id[i] != 0:
                mentions[recipe_id][i+1] = ingredients_id[i]
    return mentions

def ReadDataFridge():
    mentions = dict()
    query = StrFridge.select()
    str_selected = query.dicts().execute()
    for line in str_selected:
        user_id = line["userid"]
        ingredients_id = line["ingredientsid"]
        if not user_id in mentions:
            mentions[user_id] = dict()
        for i in range(len(ingredients_id)):
            if ingredients_id[i] != 0:
                mentions[user_id][i+1] = ingredients_id[i]
    return mentions

def ReadDataFavorite():
    mentions = dict()
    query = StrFavorite.select()
    str_selected = query.dicts().execute()
    for line in str_selected:
        user_id = line["userid"]
        recipes_id = line["recipesid"]
        if not user_id in mentions:
            mentions[user_id] = dict()
        for i in range(len(recipes_id)):
            if recipes_id[i] != 0:
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
    bestMatches = sorted(matches, key=lambda k:(k[1],k[0]), reverse=True)[:nBestUsers]
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
    bestProducts = sorted(sim.items(), key=lambda k:(k[1],k[0]), reverse=True)[:nBestProducts]
    print("Most correlated products:")
    for prodInfo in bestProducts:
        print("  ProductID: %6s  CorrelationCoeff: %6.4f" % (prodInfo[0], prodInfo[1]))
    return [(x[0], x[1]) for x in bestProducts]

userID = 6
nBestUsers = 10
nBestProducts = 10
#rec = makeRecommendation(userID, ReadDataFavorite(), nBestUsers, nBestProducts)
#print(rec)

def recipes_id(rec):
    out = []
    for record in rec:
        out.append(record[0])
    return out

#print(makeRecommendation(5,ReadDataIngredient(),nBestUsers,nBestProducts))
#print(recipeid(makeRecommendation(5,ReadDataIngredient(),nBestUsers,nBestProducts)))

def rec_recipes_id(id):
    user = User.get(User.id == id)
    if len(user.likes) <= 5:
        return recipes_id(makeRecommendation(id,ReadDataFridge(),nBestUsers,nBestProducts))
    return recipes_id(makeRecommendation(id,ReadDataFavorite(),nBestUsers,nBestProducts))