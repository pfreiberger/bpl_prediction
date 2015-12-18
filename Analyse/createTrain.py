#creating training sets
from collections import OrderedDict
import pandas as pd
import pymongo

from joblib import Parallel, delayed
import multiprocessing

client = pymongo.MongoClient()
db = client['team_results']

num_cores = multiprocessing.cpu_count()

path_train = "./trainsets_last/"
path_test = "./testsets_last/"

team_names = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names = [team_name.lower().replace(" ", "_") for team_name in team_names]
#words = ["arsen", "win", "lose", "draw","jack", "ramesy", "word", "watch", "big", "good", "legend", "love"]

max_elems = [50, 100, 250]

def inc(word_dict, words):
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
    
    return word_dict

def get_train_df(collection, word_dict_plain, df, res): 
       
    for i in range(38):
        word_dict = word_dict_plain.copy()
        word_dict['w/l/d'] = res
        #word_dict['matchday___xx'] = i
        if collection.find_one({"matchday": i}):
            for tweet in collection.find({"matchday": i}):
                word_dict = inc(word_dict, tweet['words'])           
            df = df.append(word_dict, ignore_index=True)

    return df

def get_test_df(collection, team_name, word_dict_plain, df):
      
    for i in range(14):
        word_dict = word_dict_plain.copy()
        if collection.find_one({"team": team_name.replace("_", " "), "matchday": i+1}):
            for tweet in collection.find({"team": team_name.replace("_", " "), "matchday": i+1}):
                word_dict = inc(word_dict, tweet['words'])           
            df = df.append(word_dict, ignore_index=True)
    df = df.div(df.sum(axis=1), axis=0)
    return df
        
def get_train_set(team_name, n):
    words = get_words(team_name)
    word_dict_plain = OrderedDict((word, 0) for word in words)
    col_win = db[team_name + '_win']
    col_lose = db[team_name + '_lose']
    col_draw = db[team_name + '_draw']
    df_main = pd.DataFrame()
    df = pd.DataFrame(columns=words)
    df_win = get_train_df(col_win, word_dict_plain, df.copy(), 1)
    df_lose = get_train_df(col_lose, word_dict_plain, df.copy(), -1)
    df_draw = get_train_df(col_draw, word_dict_plain, df.copy(), 0)

    db_test = client["cleansed"]
    col_test = db_test['season15_16']
    df_test = get_test_df(col_test, team_name, word_dict_plain, df.copy())

    df_test.to_csv(path_test + team_name + "_test_unigram_"+ str(n)+".csv", index=False)

    df_main = df_main.append(df_win, ignore_index=True)
    df_main = df_main.append(df_lose, ignore_index=True)
    df_main = df_main.append(df_draw, ignore_index=True)
    df_main.to_csv(path_train + team_name + "_train_unigram_"+ str(n)+".csv", index=False)
    
def get_words(team_name):
    with open("./best/"+team_name+'_best_unigram_1000.txt', 'r') as f:
        words = f.readlines() 
    words = [word.strip() for word in words]    
    return words 

def get_bigrams(input_lst, n):
    return list(zip(*[input_lst[i:] for i in range(n)]))

#returns list of list of bigrams
def read_popular_bigrams(team_name):
    with open("./best/" +team_name+"_best_bigrams_1000.txt", 'r') as f:
        words = f.readlines() 
    words = [word.replace("'","").split(",") for word in words]
    return words 

def get_train_df_bigram(collection, word_dict_plain, df, res):   
    for i in range(25):
        word_dict = word_dict_plain.copy()
        word_dict['w/l/d'] = res
        #word_dict['matchday___xx'] = i
        if collection.find_one({"matchday": i+1}):        
            for tweet in collection.find({"matchday": i+1}):
                bigram_keys =[bigram_to_key(word) for word in get_bigrams(tweet['words'], 2)]
                word_dict = inc(word_dict, bigram_keys)  
   
            df = df.append(word_dict, ignore_index=True)
    df = df.div(df.sum(axis=1), axis=0)
    
    df["w/l/d"] = res

            
    return df

def get_test_set_bigram(team_name, n):
    words = [bigram_to_key(word) for word in read_popular_bigrams(team_name)][:n]
    col = db['season14_15']
    df_main = get_df(col, team_name, words)
    df_main.to_csv(path + team_name + "_test_bigram_"+ str(n)+".csv", index=False)


def bigram_to_key(bigram):
    return "".join(bigram).replace(" ", "").strip()

def get_train_set_bigram(team_name, n):
    words = read_popular_bigrams(team_name)
    words = words = [word.replace("'", "").replace("]", "").replace("[", "").replace(" ", "").split(",") for word in words]
    words = [bigram_to_key(word) for word in words][:n]
    word_dict_plain = OrderedDict((word, 0) for word in words)
    df = pd.DataFrame(columns=words)
    col_win = db[team_name + '_win']
    col_lose = db[team_name + '_lose']
    col_draw = db[team_name + '_draw']
    df_main = pd.DataFrame()
    df_win = get_train_df_bigram(col_win, word_dict_plain, df.copy(), 1)
    df_lose = get_train_df_bigram(col_lose, word_dict_plain, df.copy(), -1)
    df_draw = get_train_df_bigram(col_draw, word_dict_plain, df.copy(), 0)


    db_test = client["cleansed"]
    col_test = db_test['season14_15']
    df_test_bi = get_test_df_bigram(col_test, team_name, word_dict_plain, df.copy())

    df_test_bi.to_csv(path_test + team_name + "_test_bigram_last_"+ str(n)+".csv", index=False)
    
    df_main = df_main.append(df_win, ignore_index=True)
    df_main = df_main.append(df_lose, ignore_index=True)
    df_main = df_main.append(df_draw, ignore_index=True)
    df_main.to_csv(path_train + team_name + "_train_bigram_last_"+ str(n)+".csv", index=False)


def get_test_df_bigram(collection, team_name, word_dict_plain, df): 
    for i in range(25,38):
        word_dict = word_dict_plain.copy()
        if collection.find_one({"team": team_name.replace("_", " "), "matchday": i+1}):
            for tweet in collection.find({"team": team_name.replace("_", " "), "matchday": i+1}):
                bigram_keys =[bigram_to_key(word) for word in get_bigrams(tweet['words'], 2)]
                word_dict = inc(word_dict, bigram_keys)          
            df = df.append(word_dict, ignore_index=True)
    
    df = df.div(df.sum(axis=1), axis=0)

    return df


def read_popular_bigrams(team_name):
    with open("./best/" +team_name+"_best_bigram_1000.txt", 'r') as f:
        words = f.readlines() 
    return words 



if __name__ == "__main__":
    for n in max_elems:
        #Parallel(n_jobs=num_cores)(delayed(get_train_set)(team_name, n) for team_name in team_names) 
        Parallel(n_jobs=num_cores)(delayed(get_train_set_bigram)(team_name, n) for team_name in team_names)
        #Parallel(n_jobs=num_cores)(delayed(combined)(team_name) for team_name in team_names)  
    