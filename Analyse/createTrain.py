#creating training sets
from collections import OrderedDict
import pandas as pd
import pymongo

from joblib import Parallel, delayed
import multiprocessing

client = pymongo.MongoClient()
db = client['team_results']

num_cores = multiprocessing.cpu_count()

path = "./trainsets/"

team_names = ['arsenal']
words = ["arsen", "win", "lose", "draw","jack", "ramesy", "word", "watch", "big", "good", "legend", "love"]

def inc(word_dict, words):
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
    
    return word_dict


def get_df(collection, words, res): 
    df = pd.DataFrame(columns=["win", "draw"])
    word_dict = OrderedDict((word, 0) for word in words)
    word_dict['w/l/d'] = res
    i=1
    while(i<=38):
        for tweet in collection.find({"matchday": i}):
            word_dict = inc(word_dict, tweet['text'])           
            df = df.append(word_dict, ignore_index=True)
            
        print(i)
        i+=1
  
def getTrainSets(teams, words):
    for team_name in teams:
        col_win = db[team_name+'_win']
        col_lose = db[team_name+'_lose']
        col_draw = db[team_name+'_draw']
        df_main = pd.DataFrame()
        df_win = get_df(col_win, words, 1)
        df_lose = get_df(col_lose, words, -1)
        df_draw = get_df(col_draw, words, 0)
        df_main.append(df_win, ignore_index=True)
        df_main.append(df_lose, ignore_index=True)
        df_main.append(df_draw, ignore_index=True)
        df.to_csv(path+team+"_train.csv")
        
        
def write_files(team_name, words):
    col_win = db[team_name+'_win']
    col_lose = db[team_name+'_lose']
    col_draw = db[team_name+'_draw']
    df_main = pd.DataFrame()
    df_win = get_df(col_win, words, 1)
    df_lose = get_df(col_lose, words, -1)
    df_draw = get_df(col_draw, words, 0)
    df_main.append(df_win, ignore_index=True)
    df_main.append(df_lose, ignore_index=True)
    df_main.append(df_draw, ignore_index=True)
    df.to_csv(path+team+"_train.csv")
    

    

getTrainSets(team_names, words)        
    