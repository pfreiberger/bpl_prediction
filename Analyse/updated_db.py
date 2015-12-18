import pymongo
import nltk
from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()
client = pymongo.MongoClient()

db_old = client["team_results"]
db_new = client["team_results_new"]

team_names = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names = [team_name.lower().replace(" ", "_") for team_name in team_names]

def stem_words(words):
    res = list()
    for word in words:
        stemmer = nltk.stem.porter.PorterStemmer()
        stem = stemmer.stem(word)
        res.append(stem)
    return res

def read_from_file(file_name):
	f = open(file_name, "r")
	words = f.readlines()
	f.close()	
	return [word.strip() for word in words] 

def check_chars(word):
	for letter in word:
		if ord(letter) not in range(65,90) and ord(letter) not in range(97,123):
			return False
	return True

def check_word(word, team_name):
	stemmed = stem_words(team_names)
	word = word.strip()
	if word is not "http":
		if len(word) > 1:
			if word not in stemmed or word==team_name:
				if check_chars(word):
					return True
	return False	

def clean_words(team_name, words):
	words_new = list()	
	for word in words:
		if check_word(word, team_name):
			words_new.append(word)
	return words_new

def update(team_name):
	words = read_from_file("./popular_clean/" +team_name+"_clean_1500.txt")
	col_win_old = db_old[team_name+"_win"]
	col_lose_old = db_old[team_name+"_lose"]
	col_draw_old = db_old[team_name+"_draw"]

	col_win_new = db_new[team_name+"_win"]
	col_lose_new = db_new[team_name+"_lose"]
	col_draw_new = db_new[team_name+"_draw"]

	clean(words, team_name, col_win_old, col_win_new)
	clean(words, team_name, col_lose_old, col_lose_new)
	clean(words, team_name, col_draw_old, col_draw_new)


def clean(words, team_name, col1, col2):
	for tweet in col1.find():
		new_words = list()
		rest = clean_words(team_name, tweet["words"])
		for w in rest:
			if w in words:
				new_words.append(w)
		if len(new_words) >= 1:
			tweet["words"] = new_words
			try:
				col2.insert(tweet)
			except:
				pass



if __name__ == "__main__":
	Parallel(n_jobs=num_cores)(delayed(update)(team_name) for team_name in team_names)
