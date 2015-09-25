import time
import sys
import praw
import sqlite3


try:
	USERNAME = sys.argv[1]
	PASSWORD = sys.argv[2]
	DB_FILE = sys.argv[3]
except IndexError:
	exit("Missing arguments")
	
conn = sqlite3.connect(DB_FILE)
conn.row_factory = sqlite3.Row
c = conn.cursor()

r = praw.Reddit(user_agent='FrissonMirror')
r.login(username=USERNAME, password=PASSWORD, disable_warning=True)

subreddit = r.get_subreddit('frisson_mirror')

def submit(title, link_url, is_self, selftext, nsfw):
	r.submit(subreddit, title, url=link_url if not is_self else None, text=selftext if is_self else None)

c.execute('SELECT * from submissions INNER JOIN resubmitted ON submissions.post_id = resubmitted.post_id ORDER BY submissions.created ASC')
result = c.fetchall()

try:
	for submission in result:
		if submission['reposted'] == 0:
			print "POSTING: " + submission['post_id']
			try:
				submit(submission['title'], submission['url'], submission['is_self'], submission['selftext'], submission['nsfw'])
				c.execute('INSERT OR REPLACE into resubmitted VALUES (?, ?)', [submission['post_id'], True])
				conn.commit()
				print "Sleeping 3 seconds"
				time.sleep(3)
			except praw.errors.AlreadySubmitted:
				print "Already Submitted, ignoring: " + submission['post_id']
				c.execute('INSERT OR REPLACE into resubmitted VALUES (?, ?)', [submission['post_id'], True])
				conn.commit()
				pass
except Exception, e:
	print "FAIL SUBMIT"
	print e
	conn.commit()
	c.close()

conn.commit()
c.close()