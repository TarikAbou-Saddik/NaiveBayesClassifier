# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

from CorpusParser import CorpusParser
from LanguageModel import LanguageModel
from Enums import Vocabulary, NGram, Language, Result

import time

# TODO: Implement smoothing.
# TODO: Complete Trace output
# TODO: Complete Eval output
# TODO: required model with V=0 n=1 d=0
# TODO: required model with V=1 n=2 d=0.5
# TODO: required model with V=1 n=3 d=1
# TODO: required model with V=2 n=2 d=0.3

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

    # Output our created language classifier
    print(self)

  def train(self):
    print('\nTraining our model using file: \'{0}\''.format(self.training_file_name))
    # Create a language model for each language found in the training corpus.
    tweets_by_lang = self.group_tweets_by_lang()
    num_languages = len(tweets_by_lang)
    count = 1
    start_time = time.time()
    for (language, tweets) in tweets_by_lang.items():
      model = LanguageModel(language, tweets, self.ngram_type, self.vocabulary, self.smoothing_value)
      print('[{0}% completed]: {1} language model created.'.format(round((count / num_languages) * 100), Language.from_str(language).name))
      count = count + 1
      self.language_models.append(model)
    end_time = time.time()
    print('Training completed. [{0}s elapsed]'.format(round(end_time - start_time)))

  def classify(self):
    print('\nClassifying tweets from test file: \'{0}\''.format(self.test_file_name))
    test_tweets = self.test_tweets_dict
    count = 1
    prior_percent = 0
    num_test_tweets = len(test_tweets)
    start_time = time.time()
    for (tweet_id, tweet) in test_tweets.items():
      percent_complete = round((count / num_test_tweets) * 100)
      if percent_complete % 25 == 0 and percent_complete != 0 and prior_percent != percent_complete:
        print('{0}% of test corpus classified'.format(percent_complete))
        prior_percent = percent_complete
      count = count + 1
      most_likely_class = str()
      highest_probability = 0
      for model in self.language_models:
        probability = model.likelihood(tweet.body)
        if probability < highest_probability:
          highest_probability = probability
          most_likely_class = model.language
      self.classified_tweets[tweet_id] = (most_likely_class, highest_probability, str())
    end_time = time.time()
    print('Test corpus classification completed. [{0}s elapsed]'.format(round(end_time - start_time)))
    self.output_trace()
    self.output_eval()

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
    total_num_classes = len(self.classified_tweets)
    total_num_correct = [tweet for tweet in self.classified_tweets if tweet[2] == Result.Correct.value]
    accuracy = round((total_num_correct / total_num_classes), 4)
    return '{0}\r'.format(accuracy)

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
    print('\nOutputting trace file...')
    lines = []
    for (tweet_id, tweet) in self.test_tweets_dict.items():
      class_tuple_result = self.classified_tweets[tweet_id]
      calculated_class = class_tuple_result[0]
      class_score = '{:.2e}'.format(class_tuple_result[1])
      correct_class = tweet.language
      label = 'Correct' if correct_class == calculated_class else 'Wrong'
      # Set whether the result was correct or not.
      class_tuple_result[2] =  Result.Correct.value if label == 'Correct' else Result.Wrong.value
      lines.append('{0}  {1}  {2}  {3}  {4}\r'.format(tweet_id, calculated_class, class_score, correct_class, label))
    
    CorpusParser.write(self.get_filename('trace'), ''.join(lines))

  # TODO: Implement
  def output_eval(self):
    print('Outputting evaluation file...')
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
    return '{0}_{1}_{2}_{3}.txt'.format(file_type, self.vocabulary, self.ngram_type, self.smoothing_value)

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
Language Classifier Parameters
------------------------------
Vocabulary Choice: {0}
N-Gram Size: {1}
Smoothing Value: {2}'''.format(self.vocabulary, self.ngram_type, self.smoothing_value)
  

