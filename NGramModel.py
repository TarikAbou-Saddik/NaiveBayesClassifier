# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

import re
from Enums import Vocabulary, NGram

class NGramModel:
  def __init__(self, corpus_dict, ngram_type, vocabulary):
    self.corpus_dict = corpus_dict
    self.ngram_type = ngram_type
    self.vocabulary = vocabulary
    # A dictionary, with key Tweet.Id and value list of Tuple(ngram, next character)
    self.ngrams_dict = self.generate_ngrams()
    # A dictionary. key: Tuple(ngram, next character), value: the total number of occurences in the corpus
    self.ngram_by_count = self.ngram_count()
    # A dictionary. key: n-gram, value: the total number of occurences in the corpus
    self.ngram_by_total_count = self.ngram_total_count()
    # {(ngram, next_char): P(next_char | ngram)}
    self.probabilities = self.generate_probabilities()

  def generate_ngrams(self):
    # Iterate through the tweets bodies
    ngrams_dict = dict()
    for tweet_id, tweet in self.corpus_dict.items():
      ngrams_dict[tweet_id] = self.n_char_split(tweet.body)
    return ngrams_dict

  def generate_probabilities(self):
    ngrams = NGramModel.flatten_list(self.ngrams_dict.values())
    probabilities = dict()
    for ngram_tuple in ngrams:
      count = self.ngram_by_count[ngram_tuple]
      total_count = self.ngram_by_total_count[ngram_tuple[0]]
      probabilities[ngram_tuple] = count / total_count
    return probabilities

  def ngram_total_count(self):
    ngram_list = [tup[0] for tup in self.ngram_by_count.keys()]
    return NGramModel.ngram_count_dict(ngram_list)

  def ngram_count(self):
    ngram_list = NGramModel.flatten_list(self.ngrams_dict.values())
    return NGramModel.ngram_count_dict(ngram_list)
  
  # TODO: Think about sentence boundaries?
  def n_char_split(self, body):
    ngrams = []
    tweet_chars = list(body)
    num_chars = len(tweet_chars)

    for i in range(0, num_chars):
      ngram_length = NGram.from_str(self.ngram_type).value
      # Break if we reach end of tweet
      if i == (num_chars - ngram_length):
        break
      # Collect our n chars for the n-gram
      chars_list = [tweet_chars[i + j] for j in range(0, ngram_length)]
      if all(self.in_vocabulary(char) for char in chars_list):
        next_char = tweet_chars[i + ngram_length] if (i + ngram_length) <= num_chars and self.in_vocabulary(tweet_chars[i + ngram_length]) else ''
        result_tuple = (self.vocab_format(''.join(chars_list)), self.vocab_format(next_char))
        ngrams.append(result_tuple)
    return ngrams

  @staticmethod
  def ngram_count_dict(ngram_list):
    ngram_by_count = dict()
    for ngram in ngram_list:
      if ngram in ngram_by_count:
        ngram_by_count[ngram] = ngram_by_count[ngram] + 1
        continue
      ngram_by_count[ngram] = 1
    return ngram_by_count

  @staticmethod
  def flatten_list(parent_list):
    return [ngram for child_list in parent_list for ngram in child_list]

  def vocab_format(self, char):
    return str(char).lower() if self.vocabulary == Vocabulary.LowercaseOnly.name else str(char)

  def in_vocabulary(self, char):    
    if self.vocabulary == Vocabulary.LowerAndUpperCase.name or self.vocabulary == Vocabulary.LowercaseOnly.name:
      return True if re.search("[a-zA-Z]", char) else False
    if self.vocabulary == Vocabulary.IsAlpha.name:
      return True if str(char).isalpha() else False
    return False

  # Debug. Print out a selected n-gram to see if it works.
  def __str__(self):
    tweet_id = list(self.ngrams_dict.keys())[3]
    # List of tuples
    ngram_list = self.ngrams_dict[tweet_id]
    ngram_count_dict = NGramModel.ngram_count_dict(ngram_list)
    ngram_total_count_dict = NGramModel.ngram_count_dict([tup[0] for tup in ngram_list])
    return 'Tweet ID: {0}\n{1}: {2}\nLanguage: {3}\nNGramByCount: {4}\nNGramByTotalCount: {5}'.format(tweet_id, self.ngram_type, ngram_list, self.corpus_dict[tweet_id].language, ngram_count_dict, ngram_total_count_dict)










      


