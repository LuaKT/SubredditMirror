import os
import json
import sqlite3
import pprint

#Json to Sqlite

DB_FILE = "frisson.db"

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()
#c.execute('create table submissions (post_id, title, is_self, url, selftext, author, nsfw)')
#c.execute('create table resubmitted (post_id, reposted)')
fail_list = []

for filename in os.listdir(os.getcwd()+"/r-frisson"):
	try:
		data = json.load(open("r-frisson/"+filename))
		#print filename
		#post_id, title, is_self, url, selftext, author, created, nsfw
		
		output_data = [	data[0]['data']['children'][0]['data']['id'],
						data[0]['data']['children'][0]['data']['title'],
						data[0]['data']['children'][0]['data']['is_self'],
						data[0]['data']['children'][0]['data']['url'],
						data[0]['data']['children'][0]['data']['selftext'],
						data[0]['data']['children'][0]['data']['author'],
						data[0]['data']['children'][0]['data']['created_utc'],
						data[0]['data']['children'][0]['data']['over_18'],
						]
		c.execute('INSERT OR IGNORE into submissions values (?,?,?,?,?,?,?,?)', output_data)
		c.execute('INSERT OR IGNORE into resubmitted values (?,?)', [data[0]['data']['children'][0]['data']['id'], False])
	except ValueError:
		fail_list.append(filename)
		print "FAIL: " + filename
conn.commit()
c.close()
