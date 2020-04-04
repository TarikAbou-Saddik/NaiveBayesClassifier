# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

# Basic class representation of a Tweet that we'll find in the corpus.

class Tweet:
  def __init__(self, raw_tweet):
    split_tweet = raw_tweet.split("\t", 3)
    self.id = split_tweet[0]
    self.username = split_tweet[1]
    self.language = split_tweet[2]
    self.text = split_tweet[3]


  def __str__(self):
    return 'UserID: {0}, Username: {1}, Language: {2}, Tweet: {3}'.format(self.id, self.username, self.language, self.text)

    