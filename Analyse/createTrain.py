#creating training sets
from collections import OrderedDict
import pandas as pd
import pymongo

from joblib import Parallel, delayed
import multiprocessing

client = pymongo.MongoClient()
db = client['team_results']
db = client['n_grams']

num_cores = multiprocessing.cpu_count()

path = "./trainsets/"

team_names = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names = [team_name.lower().replace(" ", "_") for team_name in team_names]
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
        #word_dict['matchday___xx'] = i
        if collection.find_one({"matchday": i}):
            for tweet in collection.find({"matchday": i}):
                word_dict = inc(word_dict, tweet['words'])           
            df = df.append(word_dict, ignore_index=True)
            
        i+=1
    return df
  
def get_train_sets(teams):
    for team_name in teams:
        get_train_set(team_name)        
  
        
def get_train_set(team_name):
    words = get_words(team_name)
    #words = ["arsen", "win", "lose", "draw","jack", "ramesy", "word", "watch", "big", "good", "legend", "love"]
    col_win = db[team_name + '_win']
    col_lose = db[team_name + '_lose']
    col_draw = db[team_name + '_draw']
    df_main = pd.DataFrame()
    df_win = get_df(col_win, words, 1)
    df_lose = get_df(col_lose, words, -1)
    df_draw = get_df(col_draw, words, 0)
    df_main = df_main.append(df_win, ignore_index=True)
    df_main = df_main.append(df_lose, ignore_index=True)
    df_main = df_main.append(df_draw, ignore_index=True)
    df_main.to_csv(path + team_name + "_train.csv", index=False)
    

def get_words(team_name):
    with open("./popular/"+team_name+'_popular.txt', 'r') as f:
        words = f.readlines() 
    words = [word.strip() for word in words]    
    return words 



def get_bigrams(input_lst, n):
    return list(zip(*[input_lst[i:] for i in range(n)]))

#returns list of list of bigrams
def read_popular_bigrams(team_name):
    with open("./popular/" +team_name+"_bigrams.txt", 'r') as f:
        words = f.readlines() 
    words = [word.replace("'","").split(",") for word in words]
    return words 

def get_df_bigram(collection, words, res):
    df = pd.DataFrame(columns=words)
    
    
    i=1
    while(i<=38):
        word_dict = OrderedDict((word, 0) for word in words)
        word_dict['w/l/d'] = res
        #word_dict['matchday___xx'] = i
        if collection.find_one({"matchday": i}):
            for word in words:
                for tweet in collection.find({"matchday": i}):
                    word_dict = inc(word_dict, get_bigrams(tweet['words']))           
                df = df.append(word_dict, ignore_index=True)
            
        i+=1
    return df



def get_train_set_bigram(team_name):
    col_win = db[team_name + '_win']
    col_lose = db[team_name + '_lose']
    col_draw = db[team_name + '_draw']
    df_main = pd.DataFrame()
    df_win = get_df_bigram(col_win, words, 1)
    df_lose = get_df_bigram(col_lose, words, -1)
    df_draw = get_df_bigram(col_draw, words, 0)
    
    df_main = df_main.append(df_win, ignore_index=True)
    df_main = df_main.append(df_lose, ignore_index=True)
    df_main = df_main.append(df_draw, ignore_index=True)
    df_main.to_csv(path + team_name + "_train.csv", index=False)

if __name__ == "__main__":
    Parallel(n_jobs=num_cores)(delayed(get_train_set)(team_name) for team_name in team_names) 
       

#get_train_set("arsenal")
    