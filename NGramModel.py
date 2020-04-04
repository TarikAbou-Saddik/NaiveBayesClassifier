# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

import re
from enum import Enum

class NGram(Enum):
  Unigram = 1
  Bigram = 2
  Trigram = 3

class Vocabulary(Enum):
  LowercaseOnly = 0
  LowerAndUpperCase = 1
  IsAlpha = 2

class NGramModel:
  def __init__(self, corpus_dict, ngram_type, vocabulary):
    self.corpus_dict = corpus_dict
    self.ngram_type = ngram_type
    self.vocabulary = vocabulary
    # A dictionary, with key Tweet.Id and value list of ngrams
    self.ngrams_dict = self.generate_ngrams()

  def generate_ngrams(self):
    # Iterate through the tweets bodies
    ngrams_dict = dict()
    for tweet_id, tweet in self.corpus_dict.items():
      ngrams_dict[tweet_id] = self.n_char_split(tweet.body)
    
    return ngrams_dict
  
  # TODO: Think about sentence boundaries?
  def n_char_split(self, body):
    ngrams = []
    if self.ngram_type == NGram.Unigram.name:
      for char in body:
        if self.in_vocabulary(char):
          ngrams.append(char)
  
    tweet_chars = list(body)
    num_chars = len(tweet_chars)

    # Ex. abc*def -> [ab, bc, de, ef]
    if self.ngram_type == NGram.Bigram.name:
      for i in range(0, num_chars):
        # Reached sentence boundary.
        if i == num_chars - 1:
          break
        char1 = tweet_chars[i]
        char2 = tweet_chars[i + 1]
        if self.in_vocabulary(char1) and self.in_vocabulary(char2):
          ngrams.append(str(char1) + str(char2))

    # Ex. abc*def -> [abc, def]
    if self.ngram_type == NGram.Trigram.name:
      for i in range(0, num_chars):
        # Reached sentence boundary.
        if i == num_chars - 1:
          break
        char1 = tweet_chars[i]
        char2 = tweet_chars[i + 1]
        char3 = tweet_chars[i + 2]
        if self.in_vocabulary(char1) and self.in_vocabulary(char2) and self.in_vocabulary(char3):
          ngrams.append(str(char1) + str(char2) + str(char3))

    return ngrams

  def in_vocabulary(self, char):
    if self.vocabulary == Vocabulary.LowercaseOnly.name:
      return True if re.search("[a-z]", char) else False
    
    if self.vocabulary == Vocabulary.LowerAndUpperCase.name:
      return True if re.search("[a-zA-Z]", char) else False
    
    if self.vocabulary == Vocabulary.IsAlpha.name:
      return True if str(char).isalpha() else False

  # Debug. Print out the first resulting ngram.
  def __str__(self):
    key = list(self.ngrams_dict.keys())[0]
    value = self.ngrams_dict[key]
    return 'Tweet ID: {0}\n{1}: {2}'.format(key, self.ngram_type, value)










      


