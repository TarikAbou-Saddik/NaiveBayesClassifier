# Name: Tarik Abou-Saddik
# Date: Sunday April 5th, 2020
# Student ID: 27518722

from enum import Enum

class NGram(Enum):
  Unigram = 1
  Bigram = 2
  Trigram = 3

  @staticmethod
  def from_str(label):
    if label == 'Unigram':
      return NGram.Unigram
    if label == 'Bigram':
      return NGram.Bigram
    if label == 'Trigram':
      return NGram.Trigram

class Vocabulary(Enum):
  LowercaseOnly = 0
  LowerAndUpperCase = 1
  IsAlpha = 2

  @staticmethod
  def from_str(label):
    if label == 'LowercaseOnly':
      return Vocabulary.LowercaseOnly
    if label == 'LowerAndUpperCase':
      return Vocabulary.LowerAndUpperCase
    if label == 'IsAlpha':
      return Vocabulary.IsAlpha


class Language(Enum):
  Basque = 0
  Catalan = 1
  Galician = 2
  Spanish = 3
  English = 4
  Portuguese = 5