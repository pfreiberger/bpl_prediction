#creating training sets
from collections import OrderedDict
import pandas as pd
import pymongo

client = pymongo.MongoClient()
db = client['team_results']


path = "./trainsets/"

team_names = ['man united']
#words = ["arsen", "win", "lose", "draw","jack", "ramesy", "word", "watch", "big", "good", "legend", "love"]

def inc(word_dict, words):
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
    
    return word_dict


def get_df(collection, words, res): 
    df = pd.DataFrame(columns=words)
    
    
    i=1
    while(i<=38):
        word_dict = OrderedDict((word, 0) for word in words)
        word_dict['w/l/d'] = res
        word_dict['matchday___xx'] = i
        if collection.find_one({"matchday": i}):
            for tweet in collection.find({"matchday": i}):
                word_dict = inc(word_dict, tweet['words'])           
            df = df.append(word_dict, ignore_index=True)
            
        i+=1
    return df
  
def getTrainSets(teams):
    for team_name in teams:
	words = get_words(team_name)
        col_win = db[team_name+'_win']
        col_lose = db[team_name+'_lose']
        col_draw = db[team_name+'_draw']
        df_main = pd.DataFrame()
        df_win = get_df(col_win, words, 1)
        df_lose = get_df(col_lose, words, -1)
        df_draw = get_df(col_draw, words, 0)
        df_main = df_main.append(df_win, ignore_index=True)
        df_main = df_main.append(df_lose, ignore_index=True)
        df_main = df_main.append(df_draw, ignore_index=True)
        df_main = df_main.to_csv(path+team_name+"_train.csv", index=False)
  

def get_words(team_name):
    with open(team_name+'words.txt', 'r') as f
        words = f.readlines()     
    return words 


getTrainSets(team_names)        
    