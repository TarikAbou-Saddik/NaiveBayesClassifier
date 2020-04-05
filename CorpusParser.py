# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

import os
from Tweet import Tweet

class CorpusParser:
  DEFAULT_DIR = "data"

  @staticmethod
  def parse_corpus(filename):
    path = CorpusParser.set_path(filename)
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
    path = CorpusParser.set_path(filename)
    with open(path, 'w') as file:
        file.write(lines)

  @staticmethod
  def set_path(filename):
    return os.path.join(CorpusParser.DEFAULT_DIR, filename)


    

  



