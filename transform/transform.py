import csv
import pymongo
import pandas as pd
import datetime
import nltk
from datetime import datetime
from datetime import date
import time
import csv

tags_to_keep = ["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "VBP"]
del_tags = ["http", "\@", "app"]

server = pymongo.MongoClient('localhost', 27017)
db = server['cleansed']
pure_col = db['pure']



def transform_screenscraper():
    docs = list()
    for tweet in screen_col.find():
        print("tweet")
        hashtags = [x.lower() for x in tweet["hashtags"]]
        doc = transform(int(tweet["_id"]), tweet["text"], hashtags, tweet["timestamp"], 1)
        docs.append(doc)
        if len(docs)==10:            
            transformed.insert(docs)
            docs = list()
            break
            
    if docs:
        transformed.insert(docs)
            
    
def convert_to_datetime(d, ss):
    if ss==1:
        d = date.fromtimestamp(int(d))
    elif ss == 2:
        d = datetime.strptime(d, "%a %b %d %H:%M:%S %z %Y")
    elif ss == 3:
        d = date.fromtimestamp(int(d)//1000)
    else:
        return null
    
    return datetime.combine(d, datetime.min.time())

def transform_twitter():    
    docs = list()
    for tweet in twitter_col.find():
        hashtags = [x["text"] for x in tweet["entities"]["hashtags"]]
        
        doc = transform(int(tweet["_id"]), tweet["text"], hashtags, tweet["timestamp_ms"], 3)

        docs.append(doc)
        if len(docs)==10:            
            transformed.insert(docs)
            docs = list()
            break
            
    if docs:
        transformed.insert(docs)

#Sun Oct 18 06:41:05 +0000 2015 => %a %b %d %H:%M:%S %z %Y
def transform_usertweets():    
    docs = list()
    for tweet in user_col.find():
        hashtags = [x["text"] for x in tweet["entities"]["hashtags"]]
        doc = transform(int(tweet["_id"]), tweet["text"], hashtags, tweet["created_at"], 2)
        docs.append(doc)
        if len(docs)==10:      
            transformed.insert(docs)
            docs = list()
            
    if docs:
        transformed.insert(docs)

def transform(id, text, hashtags, d, ss):
    words = remove_words(text)
    stemmed_words = stem_words(words)
    hashtags = [x.lower().replace('#', "") for x in hashtags]    
    dte = convert_to_datetime(d, ss)
    doc = {"_id": int(id), "words": stemmed_words, "date": dte, "hashtags": hashtags}
    return doc
 
def add_matchday(collection, filename, start):
    headings = ["date", "home", "away", "matchday"]
    matches = pd.read_csv(filename, header=headings)
    
    for match in matches:
        matchday = row['date']
        home_team = row['home']
        away_team = row['away']
        matchday = row['matchday']
        home_query = {"team": home_team.lower(), "date": {"$gte": start}, "date": {"$lt": end}, "matchday": {"$exitsts": False}}
        away_query = {"team": away_team.lower(), "date": {"$gte": start}, "date": {"$lt": end}, "matchday": {"$exitsts": False}}
        home_set_doc = {"set": {"home/away": 'h', "matchday": matchday}}
        away_set_doc = {"set": {"home/away": 'a', "matchday": matchday}}
        collection.update(home_query, home_set_doc)
        collection.update(away_query, away_set_doc)
        start = end;
            
def add_season(collection):
    collection.update({"date": {"$lte": datetime(2015-6-1-0-0)}}, {"$set": "season": "14_15"})
    collection.update({"date": {"$gt": datetime(2015-6-1-0-0)}}, {"$set": "season": "15_16"})

def add_team(collection, dict):
    for key, value in dict.items():
        print(key)
        print(value)
        collection.update_many({"hashtags": {"$in": value}}, {"$set": {"team": key}})

def separate_teams(col, dict):
    for element in dict:
        team = element.key
        hashtags = element.value
        collection = db[team]
        elements = col.find({"hashtag": {"$in": hahstags}}, {'text': 1, 'hashtags': 1, 'date': 1})
        collection.intsert(elements)

def delete(collection, hastags):
    collection.delete({"hashtag" : {'$nin': hashtags}})

def remove_words(text):
    tokens = nltk.word_tokenize(text)
    tagged_words = nltk.pos_tag(tokens)
    words = list()
    for word in tagged_words:
        if word[1] in tags_to_keep:
            if "." not in word[0]:
                words.append(word[0].lower())
            
    return words
     
def stem_words(words):
    res = list()
    for word in words:
        stemmer = nltk.stem.porter.PorterStemmer()
        stem = stemmer.stem(word)
        res.append(stem)
    return res

def create_team_dict(filename):
    d = dict()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            key = row[0].lower()
            values = row[1:]
            values = [x.lower() for x in values]
            d[key] = values
    return d
    
dic = create_team_dict('./team_hashtag.csv')
add_team(pure, dic)
add_matchday(pure, './championship1415.csv', datetime(2014-8-10-0-0))
add_season(pure)