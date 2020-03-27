# Name: Tarik Abou-Saddik
# Date: Sunday March 29, 2020
# Student ID: 27518722

import sys
from NBClassifier import NBClassifier

def main():
  
  # V = type of vocab, n = size of n-gram, δ = smoothing value, name of file for training, name of file for testing
  model_parameters = sys.argv[1:]

  # Check if command line arguments passed. 
  if not is_valid(model_parameters):
    print('\nA wrong number of parameters were entered. Please provide 5 parameters.\n')
    return

  # Create our classifier object that will house our model using the parameters.
  classifier = NBClassifier(*model_parameters)

  # Train our model with the training set provided.
  classifier.train()


def is_valid(args):
  return len(args) >= 3 and len(args) <= 5


# Run our main program.
if __name__ == "__main__":
  main()