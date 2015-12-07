import pymongo
from joblib import Parallel, delayed
import multiprocessing


client = pymongo.MongoClient()
db1 = client["team_results"]
db2 = client["n-grams"]

db3 = client["cleansed"]

num_cores = multiprocessing.cpu_count()

db2.connection.drop_database

def find_n_grams(input_lst, n):
    return list(zip(*[input_lst[i:] for i in range(n)]))

def get_n_grams(input_col):
    n_grams_lst = list() 
    for tweet in input_col.find():
        n_grams_lst.append(find_n_grams(tweet["words"], 2))
    return n_grams_lst

        

def insert_n_grams(output_col, n_grams):
    for n_gram in n_grams:
        if output_col.find_one({"words": n_gram}):
            output_col.update({"words": n_gram}, {"$inc": {"count": 1}}, upsert=True)
        else:
            output_col.insert({"words": n_gram, "count": 1})

def process(input_col, output_col):
    n_grams_lst = get_n_grams(input_col)
    for n_grams in n_grams_lst:
        insert_n_grams(output_col, n_grams)    

def bla(team_name):
    col1_win = db1["season15_16"]
    col1_lose = db1[team_name + '_lose']
    col1_draw = db1[team_name + '_draw']
    col2_win = db2[team_name + '_win']
    col2_lose = db2[team_name + '_lose']
    col2_draw = db2[team_name + '_draw']

    process(col1_win, col2_win)
    process(col1_lose, col2_lose)
    process(col1_draw, col2_draw)

def function(collection):
    for tweet in collection.find():
        collection.update(tweet, {"$set": {"n_grams": find_n_grams(tweet['words'], 2)}})

def rerun(name):
    db1[name]
    db2[name].drop()

    process(db1[name], db2[name])



def main():


    team_names = ['Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
    team_names = [team_name.lower().replace(" ", "_") for team_name in team_names]

    names = ['southampton_lose', 'southampton_draw', 'southampton_win', 'aston_villa_lose', 'aston_villa_draw','newcastle_draw','sunderland_draw']
    #collection = db3["season15_16"]
    #function(collection)
    #Parallel(n_jobs=num_cores)(delayed(bla)(team_name) for team_name in team_names) 
    Parallel(n_jobs=num_cores)(delayed(rerun)(name) for name in names) 



if __name__=="__main__":
    main()

         