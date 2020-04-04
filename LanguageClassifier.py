# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

import enum
from CorpusParser import CorpusFileHandler

class Vocabulary(enum.Enum):
  Lowercase = 0
  LowerUpper = 1
  IsAlpha = 2

class NGram(enum.Enum):
  Unigram = 1
  Bigram = 2
  Trigram = 3

class LanguageClassifier:

  TRAIN_FILE = 'training-tweets.txt'
  TEST_FILE = 'test-tweets-given.txt'
  VOCAB_DEFAULT = Vocabulary.Lowercase
  NGRAM_DEFAULT = NGram.Unigram
  DELTA_DEFAULT = 0.5
  
  def __init__(self, parameters):
    params = self.parse_params(parameters)

    self.vocabulary = params[0]
    self.ngram_size = params[1]
    self.smoothing_value = params[2]
    self.training_file_name = params[3]
    self.test_file_name = params[4]

    # Obtain our training and test tweets in the form of a dictionary
    self.training_tweet_info = CorpusFileHandler.parse_corpus(self.training_file_name, self.vocabulary)
    self.test_tweet_info = CorpusFileHandler.parse_corpus(self.test_file_name, self.vocabulary)

    # Results
    self.model_classes = dict()

  def train(self):
    print('Training model') 

  def test(self):
    print('Testing our model')

  def output_trace(self):
    lines = []
    for tweet_id, tweet in self.test_tweet_info.items():
      model_class = self.model_classes[tweet_id]
      class_score = 0
      correct_class = tweet.language
      label = 'correct'
      lines.append('{0}  {1}  {2}  {4}  {5}\r'.format(tweet_id, model_class, class_score, correct_class, label))
    
    CorpusFileHandler.write(self.get_filename('trace'), ''.join(lines))

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

    CorpusFileHandler.write('eval', ''.join(lines))

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

  def get_filename(self, file_type):
    return '{0}_{1}_{2}_{3}'.format(file_type, self.vocabulary, self.ngram_size, self.smoothing_value)

  def parse_params(self, parameters):
    parsed_params = []
    parsed_params.append(parameters[0] if len(parameters) > 0 else LanguageClassifier.VOCAB_DEFAULT)
    parsed_params.append(parameters[1] if len(parameters) > 1 else LanguageClassifier.NGRAM_DEFAULT)
    parsed_params.append(parameters[2] if len(parameters) > 2 else LanguageClassifier.DELTA_DEFAULT)
    parsed_params.append(parameters[3] if len(parameters) > 3 else LanguageClassifier.TRAIN_FILE)
    parsed_params.append(parameters[4] if len(parameters) > 4 else LanguageClassifier.TEST_FILE)
    return parsed_params

  def __str__(self):
    return '''
Vocabulary Choice: {0}
N-Gram Size: {1}
Smoothing Value: {2}'''.format(self.vocabulary, self.ngram_size, self.smoothing_value)
  
