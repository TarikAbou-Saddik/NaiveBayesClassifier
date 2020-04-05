# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

import re
from math import log10
from Enums import Vocabulary, NGram, Language


class LanguageModel:
  def __init__(self, language, tweets, ngram_type, vocabulary, smoothing_value):
    self.language = language
    self.tweets = tweets
    self.ngram_type = ngram_type
    self.vocabulary = vocabulary
    self.smoothing_value = smoothing_value
    self.probabilities = self.generate_probabilities()

  def likelihood(self, tweet):
    # Break tweet into ngrams
    ngrams_tweet = self.get_ngrams_tweet(tweet)
    likelihood = 0
    # if LanguageModel.count == 0:
    #   print('Length of ngrams in tweet: {0}'.format(len(ngrams_tweet)))
    
    for ngram_tuple in ngrams_tweet:
      counter = 0
      if ngram_tuple in self.probabilities:
        counter = counter + 1
        likelihood = likelihood + log10(self.probabilities[ngram_tuple])
    #   if LanguageModel.count == 0:
    #     print('{0} probabilities used to sum to likelihood {1}'.format(counter, likelihood))
    # LanguageModel.count = LanguageModel.count + 1  
    return likelihood

  # TODO: Add smoothing to calculation
  # Calculating probabilities
  def generate_probabilities(self):
    probabilities = dict()
    ngrams = self.get_ngrams_all()
    ngrams_by_tuple_count = self.get_ngrams_by_tuple_count()
    ngrams_by_total_count = self.get_ngrams_by_total_count()
    for ngram_tuple in ngrams:
      count = ngrams_by_tuple_count[ngram_tuple]
      total_count = ngrams_by_total_count[ngram_tuple[0]]
      probabilities[ngram_tuple] = count / total_count
    return probabilities

  # Obtain a dictionary with key: tuple(ngram, next_char) and value: frequency in corpus
  def get_ngrams_by_total_count(self):
    ngrams_list = [ngram_tuple[0] for ngram_tuple in self.get_ngrams_all()]
    return LanguageModel.ngram_count_dict(ngrams_list)

  # Obtain a dictionary with key: ngram and value: frequency in corpus
  def get_ngrams_by_tuple_count(self):
    ngrams_list = self.get_ngrams_all()
    return LanguageModel.ngram_count_dict(ngrams_list)

  # Obtain a list of all the ngrams for the corpus
  def get_ngrams_all(self):
    ngrams_list = []
    for tweet in self.tweets:
      ngrams_list.append(self.get_ngrams_tweet(tweet))
    return LanguageModel.flatten_list(ngrams_list)
  
  # Obtain our ngrams from a single Tweet.
  def get_ngrams_tweet(self, body):
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

  # Helper methods
  def vocab_format(self, char):
    return str(char).lower() if self.vocabulary == Vocabulary.LowercaseOnly.name else str(char)

  def in_vocabulary(self, char):    
    if self.vocabulary == Vocabulary.LowerAndUpperCase.name or self.vocabulary == Vocabulary.LowercaseOnly.name:
      return True if re.search("[a-zA-Z]", char) else False
    if self.vocabulary == Vocabulary.IsAlpha.name:
      return True if str(char).isalpha() else False
    return False

  # Static methods
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
    return [element for child_list in parent_list for element in child_list]

  # For debug purposes
  def __str__(self):
    sample_tweet = self.tweets[0]
    ngrams = self.get_ngrams_tweet(sample_tweet)
    ngrams_tuple_count = LanguageModel.ngram_count_dict(ngrams)
    return 'Tweet: {0}\nLanguage: {1}\nNGrams: {2}\nNGramsTupleCount: {3}\n'.format(sample_tweet, self.language, ngrams, ngrams_tuple_count)