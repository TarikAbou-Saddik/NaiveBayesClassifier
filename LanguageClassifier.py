# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

from CorpusParser import CorpusParser
from LanguageModel import LanguageModel
from Enums import Vocabulary, NGram


class LanguageClassifier:

  VOCAB_DEFAULT = Vocabulary.LowercaseOnly.name
  NGRAM_DEFAULT = NGram.Unigram.name
  DELTA_DEFAULT = 0.5
  TRAIN_FILE = 'training-tweets.txt'
  TEST_FILE = 'test-tweets-given.txt'
  
  def __init__(self, parameters):
    params = self.parse_params(parameters)

    self.vocabulary = params[0]
    self.ngram_type = params[1]
    self.smoothing_value = params[2]
    self.training_file_name = params[3]
    self.test_file_name = params[4]

    # Obtain our training and test tweets in the form of a dictionary: {key: tweet_id, value: tweet}
    self.training_tweets_dict = CorpusParser.parse_corpus(self.training_file_name)
    self.test_tweets_dict = CorpusParser.parse_corpus(self.test_file_name)

    # Our list of language models
    self.language_models = []

    # Classified tweets
    self.classified_tweets = dict()

  def train(self):
    # Create a language model for each language found in the training corpus.
    for (language, tweets) in self.group_tweets_by_lang().items():
      model = LanguageModel(language, tweets, self.ngram_type, self.vocabulary, self.smoothing_value)
      self.language_models.append(model)

  def classify(self):
    for (tweet_id, tweet) in self.test_tweets_dict.items():
      most_likely_class = ''
      highest_probability = 0
      for model in self.language_models:
        probability = model.likelihood(tweet.body)
        if probability > highest_probability:
          highest_probability = probability
          most_likely_class = model.language
      self.classified_tweets[tweet_id] = most_likely_class

  def group_tweets_by_lang(self):
    tweets_list = self.training_tweets_dict.values()
    tweets_by_language = dict()
    for tweet in tweets_list:
      language = tweet.language
      if language in tweets_by_language:
        tweets_by_language[language].append(tweet.body)
        continue
      tweets_by_language[language] = [tweet.body]
    return tweets_by_language

  def model_accuracy(self):
    return ''

  def per_class_precision(self):
    return ''
  
  def per_class_recall(self):
    return ''
  
  def per_class_f1(self):
    return ''
  
  def macro_f1(self):
    return ''

  def weight_avg_f1(self):
    return ''

  def output_trace(self):
    lines = []
    for (tweet_id, tweet) in self.test_tweets_dict.items():
      calculated_class = self.classified_tweets[tweet_id]
      class_score = 0
      correct_class = tweet.language
      label = 'Correct' if correct_class == calculated_class else 'Wrong'
      lines.append('{0}  {1}  {2}  {3}  {4}\r'.format(tweet_id, calculated_class, class_score, correct_class, label))
    
    CorpusParser.write(self.get_filename('trace'), ''.join(lines))

  # TODO: Implement
  def output_eval(self):
    lines = []
    # Accuracy
    lines.append(self.model_accuracy())
    # Per-class precision
    lines.append(self.per_class_precision())
    # Per-class recall
    lines.append(self.per_class_recall())
    # Per-class F1-measure
    lines.append(self.per_class_f1())
    # Macro-F1 and weighted-average F1
    lines.append('{0}  {1}'.format(self.macro_f1(), self.weight_avg_f1()))

    CorpusParser.write('eval', ''.join(lines))

  def get_filename(self, file_type):
    return '{0}_{1}_{2}_{3}'.format(file_type, self.vocabulary, self.ngram_type, self.smoothing_value)

  def parse_params(self, parameters):
    parsed_params = []
    parsed_params.append(Vocabulary(int(parameters[0])).name if len(parameters) > 0 else LanguageClassifier.VOCAB_DEFAULT)
    parsed_params.append(NGram(int(parameters[1])).name if len(parameters) > 1 else LanguageClassifier.NGRAM_DEFAULT)
    parsed_params.append(int(parameters[2]) if len(parameters) > 2 else LanguageClassifier.DELTA_DEFAULT)
    parsed_params.append(str(parameters[3]) if len(parameters) > 3 else LanguageClassifier.TRAIN_FILE)
    parsed_params.append(str(parameters[4]) if len(parameters) > 4 else LanguageClassifier.TEST_FILE)
    return parsed_params

  def __str__(self):
    return '''
Vocabulary Choice: {0}
N-Gram Size: {1}
Smoothing Value: {2}'''.format(self.vocabulary, self.ngram_type, self.smoothing_value)
  

