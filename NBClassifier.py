# Name: Tarik Abou-Saddik
# Date: Sunday March 29, 2020
# Student ID: 27518722

class NBClassifier:
  TRAIN_FILE = 'training-tweets.txt'
  TEST_FILE = 'test-tweets-given.txt'
  
  def __init__(self, parameters):
    self.vocabulary = parameters[0]
    self.ngram_size = parameters[1]
    self.smoothing_value = parameters[2]
    self.training_file = parameters[3]
    self.test_file = parameters[4]

  def train(self):
    print('Training model')

  

