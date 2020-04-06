# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

from CorpusParser import CorpusParser
from LanguageModel import LanguageModel
from Enums import Vocabulary, NGram, Language, ClassifyTupleResult

import time

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
    # {key: tweet_id, value = tuple(calc_class, score, real_class)}
    self.classified_tweets_by_id = dict()
    self.classified_tweets_by_class = dict()

    # Metrics
    self.per_class_precision = dict()
    self.per_class_recall = dict()
    self.per_class_f1 = dict()

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
      print('[{0}% completed]: {1} language model created. {2} tweets parsed.'.format(round((count / num_languages) * 100), Language.from_str(language).name, len(tweets)))
      count = count + 1
      self.language_models.append(model)
    end_time = time.time()
    print('Training completed. A total of {0} tweets parsed. [{1}s elapsed]'.format(len(self.training_tweets_dict),round(end_time - start_time)))

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
        print('{0}% of test corpus classified.'.format(percent_complete))
        prior_percent = percent_complete
      count = count + 1
      most_likely_class = str()
      highest_probability = float("-inf")
      for model in self.language_models:
        probability = model.likelihood(tweet.body)
        if probability > highest_probability:
          highest_probability = probability
          most_likely_class = model.language
      correct_class = tweet.language
      result_tuple = (most_likely_class, highest_probability, correct_class)
      self.classified_tweets_by_id[tweet_id] = result_tuple
      if correct_class in self.classified_tweets_by_class:
        self.classified_tweets_by_class[correct_class].append(result_tuple)
      else:
        self.classified_tweets_by_class[correct_class] = [result_tuple]
    end_time = time.time()
    print('Test corpus classification completed. {0} tweets classified. [{1}s elapsed]'.format(len(self.test_tweets_dict),round(end_time - start_time)))
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
    total_num_classes = len(self.classified_tweets_by_id)
    total_num_correct = len([tweet for tweet in self.classified_tweets_by_id if tweet[ClassifyTupleResult.CalculatedClass.value] == tweet[ClassifyTupleResult.CorrectClass.value]])
    accuracy = round((total_num_correct / total_num_classes), 4)
    return '{0}\r'.format(accuracy)

  # TODO: Refactor this.
  def calc_precision(self):
    # Order of classes: eu, ca, gl, es, en, pt
    per_class = dict()
    classes = self.classified_tweets_by_class.keys()
    tuple_result_list = LanguageModel.flatten_list(self.classified_tweets_by_class.values())
    for chosen_class in classes:
      tp = len([result for result in tuple_result_list if chosen_class == result[ClassifyTupleResult.CalculatedClass.value] and chosen_class == result[ClassifyTupleResult.CorrectClass.value]])
      fp = len([result for result in tuple_result_list if chosen_class == result[ClassifyTupleResult.CalculatedClass.value] and chosen_class != result[ClassifyTupleResult.CorrectClass.value]])
      precision = round(tp / (tp + fp), 4)
      per_class[chosen_class] = precision
    self.per_class_precision = per_class
  
  # TODO: Refactor this.
  def calc_recall(self):
    # Order of classes: eu, ca, gl, es, en, pt
    per_class = dict()
    classes = self.classified_tweets_by_class.keys()
    tuple_result_list = LanguageModel.flatten_list(self.classified_tweets_by_class.values())
    for chosen_class in classes:
      tp = len([result for result in tuple_result_list if chosen_class == result[ClassifyTupleResult.CalculatedClass.value] and chosen_class == result[ClassifyTupleResult.CorrectClass.value]])
      fn = len([result for result in tuple_result_list if chosen_class != result[ClassifyTupleResult.CalculatedClass.value] and chosen_class == result[ClassifyTupleResult.CorrectClass.value]])
      recall = round(tp / (tp + fn), 4)
      per_class[chosen_class] = recall
    self.per_class_recall = per_class

  def calc_f1(self):
    per_class = dict()
    classes = self.classified_tweets_by_class.keys()
    for chosen_class in classes:
      precision = self.per_class_precision[chosen_class]
      recall = self.per_class_recall[chosen_class]
      f1 = round((2 * precision * recall) / (precision + recall), 4) if precision + recall > 0 else float(0.0000)
      per_class[chosen_class] = f1
    self.per_class_f1 = per_class
  
  def macro_f1(self):
    sum_f1 = 0
    f1_list = self.per_class_f1.values()
    for f1 in f1_list:
      sum_f1 = sum_f1 + f1
    return round(sum_f1 / len(f1_list), 4)

  def weight_avg_f1(self):
    classes = self.classified_tweets_by_class.keys()
    tuple_result_list = LanguageModel.flatten_list(self.classified_tweets_by_class.values())
    sum_weighted_f1 = 0
    for chosen_class in classes:
      chosen_class_correct_count = len([result for result in tuple_result_list if result[ClassifyTupleResult.CorrectClass.value] == chosen_class])
      sum_weighted_f1 = sum_weighted_f1 + self.per_class_f1[chosen_class] * chosen_class_correct_count
    return round(sum_weighted_f1 / len(tuple_result_list), 4)

  # TODO: Check if something's up with the score.
  def output_trace(self):
    print('\nOutputting trace file...')
    lines = []
    for tweet_id in self.test_tweets_dict:
      class_tuple_result = self.classified_tweets_by_id[tweet_id]
      calculated_class = class_tuple_result[ClassifyTupleResult.CalculatedClass.value]
      correct_class = class_tuple_result[ClassifyTupleResult.CorrectClass.value]
      class_score = '{:.2e}'.format(class_tuple_result[ClassifyTupleResult.Score.value])
      label = 'Correct' if correct_class == calculated_class else 'Wrong'
      lines.append('{0}  {1}  {2}  {3}  {4}\r'.format(tweet_id, calculated_class, class_score, correct_class, label))
    
    CorpusParser.write(self.get_filename('trace'), ''.join(lines))

  def output_eval(self):
    print('Outputting evaluation file...')
    lines = []
    # Accuracy
    lines.append(self.model_accuracy())
    # Per-class precision
    self.calc_precision()
    lines.append(self.format_metric(self.per_class_precision))
    # Per-class recall
    self.calc_recall()
    lines.append(self.format_metric(self.per_class_recall))
    # Per-class F1-measure
    self.calc_f1()
    lines.append(self.format_metric(self.per_class_f1))
    # Macro-F1 and weighted-average F1
    lines.append('{0}  {1}'.format(self.macro_f1(), self.weight_avg_f1()))

    CorpusParser.write(self.get_filename('eval'), ''.join(lines))

  def format_metric(self, per_class):
    return '{:.4f}  {:.4f}  {:.4f}  {:.4f}  {:.4f}  {:.4f}\r'.format(per_class['eu'], per_class['ca'], per_class['gl'], per_class['es'], per_class['en'], per_class['pt'])

  def get_filename(self, file_type):
    vocab_int = Vocabulary.from_str(self.vocabulary).value
    ngram_int = NGram.from_str(self.ngram_type).value
    return '{0}_{1}_{2}_{3}.txt'.format(file_type, vocab_int, ngram_int, self.smoothing_value)

  def parse_params(self, parameters):
    parsed_params = []
    parsed_params.append(Vocabulary(int(parameters[0])).name if len(parameters) > 0 else LanguageClassifier.VOCAB_DEFAULT)
    parsed_params.append(NGram(int(parameters[1])).name if len(parameters) > 1 else LanguageClassifier.NGRAM_DEFAULT)
    parsed_params.append(float(parameters[2]) if len(parameters) > 2 else LanguageClassifier.DELTA_DEFAULT)
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
  

