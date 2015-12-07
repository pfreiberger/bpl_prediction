import pandas as pd
import pymongo

client = pymongo.MongoClient()
db = client["n-grams"]

max_elems = 1000

team_names_14_15 = ['Man United', 'Man City','Arsenal','Chelsea','Liverpool','West Ham','Leicester','Everton','Swansea','Crystal Palace','Tottenham','West Brom','Southampton','Aston Villa','Stoke','Newcastle','Sunderland']
team_names_14_15 = [team_name.lower().replace(" ", "_") for team_name in team_names_14_15]

def get_data(file_name,n):
    return clean_df(pd.read_csv(file_name, sep="\t", names=["word", "count"]), max_elems)

def clean_df(df, n):
	df = df[df["count"].map(type) != str]
	df = df.sort("count", ascending=False)

	return df.head(n)


#"".replac(" ", "_")

def creat_files():
	for team_name in team_names_14_15:
	    team_name = team_name.lower().replace(" ", "_")
	    df_win = get_data("./result_word_count_14_15/"+  team_name + "_win_wc.csv", max_elems)
	    df_lose = get_data("./result_word_count_14_15/"+  team_name + "_lose_wc.csv", max_elems)
	    df_draw = get_data("./result_word_count_14_15/"+  team_name + "_draw_wc.csv", max_elems)

	    df_win.to_csv("./result_word_count_14_15_proc/"+  team_name + "_win_wc_" + str(max_elems) +".csv", index=False, encoding="utf-8")
	    df_lose.to_csv("./result_word_count_14_15_proc/"+  team_name + "_lose_wc_" + str(max_elems) +".csv", index=False, encoding="utf-8")
	    df_draw.to_csv("./result_word_count_14_15_proc/"+  team_name + "_draw_wc_" + str(max_elems) +".csv", index=False, encoding="utf-8")

def add_to_set(word_set, word_list):
	for word in word_list:
		word_set.add(word)
	return word_set

def get_single_words(file_name):
	df = pd.read_csv(file_name, sep=",", names=["word", "count"], encoding="utf-8")
	return list(df["word"])


def get_total_words(team_name, max_elems):
	words = set()
	file_win = "./result_word_count_14_15_proc/"+  team_name + "_win_wc_" + str(max_elems) +".csv"
	file_lose = "./result_word_count_14_15_proc/"+  team_name + "_lose_wc_" + str(max_elems) +".csv"
	file_draw = "./result_word_count_14_15_proc/"+  team_name + "_draw_wc_" + str(max_elems) +".csv"

	words = add_to_set(words, get_single_words(file_win))
	words = add_to_set(words, get_single_words(file_lose))
	words = add_to_set(words, get_single_words(file_draw))

	return words

def write_to_file(words, file_name):
	words = list(words)
	f = open(file_name, "w+")
	for word in words:
		try:
			f.write(word)
			f.write("\n") 
		except UnicodeEncodeError:
			print("couldn't write word, ecoding error")
	f.close()

def save_words_for_teams(max_elems):
	for team_name in team_names_14_15:
		words = get_total_words(team_name, max_elems)
		write_to_file(words, "./popular/" + team_name + "_popular.txt")


def get_popular_bigrams(collection):
	ngrams = [str(tweet["words"]).strip('[]') for tweet in collection.find({"count": {"$gte": 50}})]
	return ngrams


def combine_bigrams(team_name):
	words = list()
	file_win = db[team_name+"_win"]
	file_lose = db[team_name+"_draw"]
	file_draw = db[team_name+"_lose"]

	words = distinct_list(words, get_popular_bigrams(file_win))
	words = distinct_list(words, get_popular_bigrams(file_lose))
	words = distinct_list(words, get_popular_bigrams(file_draw))

	return words

def distinct_list(list1, list2):
	for elem in list2:
		if elem in list1:
			continue
		else:
			list1.append(elem)
	return list1

def bigram_master():
	for team_name in team_names_14_15:
		print(team_name)
		words = combine_bigrams(team_name)
		write_to_file(words, "./popular/" +team_name+"_bigrams.txt")


if __name__ == "__main__":
	#creat_files()
	#save_words_for_teams(max_elems)
	print("step one")
	bigram_master()

