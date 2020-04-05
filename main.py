# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

import sys
from LanguageClassifier import LanguageClassifier

def main():
  
  # V = type of vocab
  # n = size of n-gram 
  # δ = smoothing value 
  # Name of file for training
  # Name of file for testing
  model_parameters = sys.argv[1:]

  # Create our classifier object that will house our model using the parameters.
  classifier = LanguageClassifier(model_parameters)

  # Train our model with the training set provided.
  classifier.train()

  print('Done training model.')

  # Test our classifier model on the test set.
  classifier.classify()

  print('Done classifiying. See Trace and Evaluation files in data folder.')

# Run our main program.
if __name__ == "__main__":
  main()