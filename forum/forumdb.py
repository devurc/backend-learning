# "Database code" for the DB Forum.

import datetime

import psycopg2
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database="forum")
  c = db.cursor()
  c.execute("select content, time from posts order by time desc")
  return c.fetchall()
  db.close()
  

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  #POSTS.append((content, datetime.datetime.now()))
  db = psycopg2.connect(database="forum")
  c = db.cursor()
  c.execute("insert into posts values (%s)", (bleach.clean(content),))
  db.commit()
  db.close()
