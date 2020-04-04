# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

import os
from Tweet import Tweet

class CorpusFileHandler:
  DEFAULT_DIR = "data"

  @staticmethod
  def parse_corpus(filename, vocabulary):
    path = CorpusFileHandler.set_path(filename)
    tweets = dict()
    with open(path, "r") as file:
      for line in file:
        if line == '\n':
          break
        tweet = Tweet(line)
        tweets[tweet.id] = tweet
    return tweets
  
  @staticmethod
  def write(filename, lines):
    path = CorpusFileHandler.set_path(filename)
    with open(path, 'w') as file:
        file.write(lines)

  @staticmethod
  def set_path(filename):
    return os.path.join(CorpusFileHandler.DEFAULT_DIR, filename)

  # By default, print out the tweets
  def __str__(self):
    for tweet in self.tweets.values():
      print(tweet)


    

  



