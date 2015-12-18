import pandas as pd
import pymongo
import nltk

from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()

client = pymongo.MongoClient()
db = client["n-grams"]

max_list = [1500]

team_names_14_15 = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names_14_15 = [team_name.lower().replace(" ", "_") for team_name in team_names_14_15]

def stem_words(words):
    res = list()
    for word in words:
        stemmer = nltk.stem.porter.PorterStemmer()
        stem = stemmer.stem(word)
        res.append(stem)
    return res

def get_data(file_name, n, team_name=None):
    return clean_df(pd.read_csv(file_name, sep="\t", names=["word", "count"]), n, team_name)

def clean_df(df, n, team_name = None):
	df = df[df["count"].map(type) != str]
	df = df.sort("count", ascending=False)
	df = df[df["count"] >10]
	new_df = pd.DataFrame(columns = ["word", "count"])

	for index, row in df.iterrows():
		if check_word(row["word"], team_name):
			new_df = new_df.append(row, ignore_index=True)
	return new_df.head(n)


def creat_files(max_elems):
	for team_name in team_names_14_15:
	    team_name = team_name.lower().replace(" ", "_")
	    df_win = get_data("./result_word_count_14_15/"+  team_name + "_win_wc.csv", max_elems, team_name)
	    df_lose = get_data("./result_word_count_14_15/"+  team_name + "_lose_wc.csv", max_elems, team_name)
	    df_draw = get_data("./result_word_count_14_15/"+  team_name + "_draw_wc.csv", max_elems, team_name)

	    df_win.to_csv("./result_word_count_14_15_proc/"+  team_name + "_win_wc_" + str(max_elems) +".csv", index=False, encoding="utf-8")
	    df_lose.to_csv("./result_word_count_14_15_proc/"+  team_name + "_lose_wc_" + str(max_elems) +".csv", index=False, encoding="utf-8")
	    df_draw.to_csv("./result_word_count_14_15_proc/"+  team_name + "_draw_wc_" + str(max_elems) +".csv", index=False, encoding="utf-8")

def add_to_set(word_set, word_list):
	for word in word_list:
		if word not in word_set:
			word_set.append(word)
	return word_set

def get_single_words(file_name):
	df = pd.read_csv(file_name, sep=",", names=["word", "count"], encoding="utf-8")
	words = list(df["word"])
	return words

def get_total_words(team_name, max_elems):
	words = list()
	file_win = "./result_word_count_14_15_proc/"+  team_name + "_win_wc_" + str(max_elems) +".csv"
	file_lose = "./result_word_count_14_15_proc/"+  team_name + "_lose_wc_" + str(max_elems) +".csv"
	file_draw = "./result_word_count_14_15_proc/"+  team_name + "_draw_wc_" + str(max_elems) +".csv"

	words = add_to_set(words, get_single_words(file_win))
	words = add_to_set(words, get_single_words(file_lose))
	words = add_to_set(words, get_single_words(file_draw))

	return words

def read_from_file(file_name):
	f = open(file_name, "r")
	words = f.readlines()
	words = [word.strip() for word in words] 
	words = [word for word in words if not word==""]
	f.close()
	return words 

def write_to_file(words, file_name):
	words = list(words)
	f = open(file_name, "w+")
	for word in words:

		try:
			f.write(str(word))
			f.write("\n") 
		except UnicodeEncodeError:
			print("couldn't write word, ecoding error")
	f.close()

def save_words_for_teams(max_elems):
	for team_name in team_names_14_15:
		words = get_total_words(team_name, max_elems)
		write_to_file(words, "./popular/" + team_name + "_popular_" +str(max_elems)+".txt")

def clean_bigrams(collection, ngrams, team_name):
	new_ngrams = list()
	for ngram in ngrams:
		if check_words(ngram, team_name):
			new_ngrams.append(ngram)
		else:
			collection.remove({"words": ngram})

	return new_ngrams

def get_popular_bigrams(collection, team_name):
	ngrams = [tweet["words"] for tweet in collection.find({"count": {"$gte": 50}})]
	ngrams = clean_bigrams(collection, ngrams, team_name)
	return ngrams

def combine_bigrams(team_name):
	words = list()
	file_win = db[team_name+"_win"]
	file_lose = db[team_name+"_draw"]
	file_draw = db[team_name+"_lose"]

	words = distinct_list(words, get_popular_bigrams(file_win, team_name))
	words = distinct_list(words, get_popular_bigrams(file_lose, team_name))
	words = distinct_list(words, get_popular_bigrams(file_draw, team_name))

	return words

def distinct_list(list1, list2):
	for elem in list2:
		if elem in list1:
			continue
		else:
			list1.append(elem)
	return list1

def check_words(words, team_name):
	for word in words:
		if not check_word(word, team_name):
			return False
	return True

def check_chars(word):
	for letter in word:
		if ord(letter) not in range(65,90) and ord(letter) not in range(97,123):
			return False
	return True

def check_word(word, team_name):
	stemmed = stem_words(team_names_14_15)
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

def master_clean(max_elems):
	for team_name in team_names_14_15:
		words = read_from_file("./popular/" + team_name + "_popular_" +str(max_elems)+".txt")
		words = clean_words(team_name, words)
		write_to_file(words, "./popular_clean/" +team_name+"_clean_" +str(max_elems)+".txt")

def bigram_master(team_name):	
	print(team_name)
	words = combine_bigrams(team_name)
	write_to_file(words, "./popular_bigram/" +team_name+"_bigrams.txt")

	#print("step one")
	#bigram_master()

if __name__ == "__main__":
	#print("create sorted files")
	#Parallel(n_jobs=num_cores)(delayed(creat_files)(max_elem) for max_elem in max_list) 
	#print("create popular word files")
	#Parallel(n_jobs=num_cores)(delayed(save_words_for_teams)(max_elem) for max_elem in max_list)
	#Parallel(n_jobs=num_cores)(delayed(master_clean)(max_elem) for max_elem in max_list) 
	Parallel(n_jobs=num_cores)(delayed(bigram_master)(team_name) for team_name in team_names_14_15) 
