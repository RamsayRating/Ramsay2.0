#!/usr/bin/env python3
import twitter
import sqlite3
from sqlite3 import Error
import os.path
import random
import numpy as np
import math
from unidecode import unidecode
from watson_developer_cloud import ToneAnalyzerV3



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_tweet(conn, tweet):
	sql = ''' INSERT INTO tweets VALUES(?,?)'''
	cur = conn.cursor()
	cur.execute(sql, tweet)
	idnum = cur.lastrowid
	cur.close()
	return idnum

def select_all_tweets(conn):
	"""
	Query all rows in the tasks table
	:param conn: the Connection object
	:return:
	"""
	cur = conn.cursor()
	cur.execute("SELECT * FROM tweets")

	rows = cur.fetchall()

	for row in rows:
		print(row)

	print("\n")


def connect_to_database():
	database = "tweetdatabase.db"

	sql_create_tweets_table = """ CREATE TABLE IF NOT EXISTS tweets (
	                                    rating text,
	                                    tweet text
	                                ); """


	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	db_path = os.path.join(BASE_DIR, database)
	# create a database connection
	conn = create_connection(db_path)
	if conn is not None:
		# create projects table
		create_table(conn, sql_create_tweets_table)
		conn.commit()
	else:
		print("Error! cannot create the database connection.")

	return(conn)

def sentiment_analysis(name, conn):
	"""
	This function takes a file and creates a dictionary of each line's sentiment analysis.
	>>> sentiment_analysis('EmmanuelMacron', {})
	{'EmmanuelMacron': [0.1466666666666667, 0.0, -0.1, 0.0, 0.42000000000000004, 0.0, 0.115, 0.0, 0.1325, 0.0, 0.03333333333333333, 0.0, 0.27, -0.12, 0.0, 0.22, 0.27, 0.1, 0.15, 0.075, 0.0, 0.0, 0.0, 0.17, 0.0, 0.07666666666666666, 0.2, 0.0, 0.0, 0.2, 0.2525, -0.35, 0.0, 0.0, 0.1, 0.0, 0.15, 0.0, 0.0, 0.56, 0.0, 0.25, 0.22, 0.0, 0.0, 0.45, 0.0, 0.0, 0.023333333333333334, 0.025000000000000022, 0.0, 0.0, -0.125, 0.0, 0.0, 0.0, 0.15, 0.13666666666666666, 0.1, 0.11, 0.0, 0.0, -0.4, 0.0, 0.0, 0.2, 0.625, 0.0, 0.0, 0.0, 0.09999999999999999, 0.0, 0.05, 0.25, 0.0, 0.0, 0.0, 0.22, 0.0, 0.22, 0.22, 0.53, -0.15, 0.0, 0.0, 0.4, 0.0, 0.0, 0.009999999999999995, 0.0, 0.0, -0.016666666666666663, 0.1, 0.0, 0.15, 0.0, 0.1, 0.0, -0.25, 0.0, -0.25166666666666665, 0.22, 0.17, 0.0, 0.0, -0.7, 0.0, 0.22, 0.22, 0.0, 0.2, 0.0, 0.0, 0.0, 0.13, 0.17, 0.0, 0.1275, 0.0, 0.0, 0.1, 0.15, -0.16249999999999998, 0.1, 0.8, 0.14, 0.0, 0.0, -0.1, 0.0, 0.0, 0.0, 0.30833333333333335, 0.0, 0.185, 0.0, 0.0, 0.0, -0.09000000000000001, 0.0, 0.08, -0.75, 0.22, 0.0, -0.3, 0.21000000000000002, 0.010000000000000009, -0.03125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.17500000000000002, 0.3499999999999999, 0.09833333333333334, 0.135, 0.0, 0.0, 0.08, 0.2, 0.0, -0.2, 0.0, 0.2233333333333333, 0.0, 0.29, 0.0, 0.0, 0.0, 0.0, 0.6625000000000001, 0.29, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.32, 0.4, -0.24, 0.0, -0.125, 0.15, 0.0, 0.7, 0.0, 0.22, 0.0, 0.0, 0.5, 0.0, 0.2, -0.21875, 0.25, 0.26, 0.185, 0.08333333333333333, 0.23]}
	"""
	cursor = conn.cursor()
	tone_analyzer = ToneAnalyzerV3(
		    username='2ed2f0c6-1722-472d-9126-224897b991af',
		    password='UcuSde1YmeK6',
		    version='2016-05-19')
	l = open(name + '.txt')
	lines = l.readlines()
	l.close()
	feel_dict = {'':0.0,'Anger':2.0,'Fear':2.0, 'Sadness':2.0, 'Disgust':2.0,'Joy':1.0, 'Excitement':1.0}
	for i in lines:
		max_score = 0.0
		max_feel = ''
		tone = tone_analyzer.tone(i, 'emotion')
		for feel in tone['document_tone']['tone_categories']:
			for feeling in feel['tones']:
				if feeling['score'] > max_score:
					max_score = feeling['score']
					max_feel = feeling['tone_name']

		create_tweet(conn, (feel_dict[max_feel], i[0:-1]))
		conn.commit()
	select_all_tweets(conn)
		#print(max_score, max_feel)
		#blob1 = TextBlob(i, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
		


def retrieve_text(name, number):
	consumer_k = open('consumer_key.txt').read().strip()
	consumer_s = open('consumer_secret.txt').read().strip()
	access_key = open('access_token_key.txt').read().strip()
	access_secret = open('access_token_secret.txt').read().strip()
	api = twitter.Api(consumer_key=	consumer_k,
                  consumer_secret= consumer_s,
                  access_token_key= access_key,
                  access_token_secret= access_secret)

	l = open(name + '.txt', 'w')
	status = api.GetUserTimeline(screen_name='@' + name, count = number)

	for i in status:

		i = unidecode(i.text)
		if "MasterChef" not in i and "HellsKitchen" not in i \
			and "MASTERCHEF" not in i and "#" not in i and "@" not in i:
			j = i.split(" ")
			j = j[0:-1]
			i = ' '.join(word for word in j)
			l.write(i)
			l.write('\n')
		
	l.close()

def retrieve_tweet_database(conn, rating):
	cur = conn.cursor()
	cur.execute("SELECT * FROM tweets WHERE rating = ?",(rating,))

	rows = cur.fetchall()
	return(random.choice(rows)[1])

#retrieve_text('GordonRamsay', 203)
conn = connect_to_database()
#select_all_tweets(conn)
#sentiment_analysis('GordonRamsay', conn)
#print(retrieve_tweet_database(conn, 2.0))

