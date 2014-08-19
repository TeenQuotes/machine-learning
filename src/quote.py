# -*- coding: utf-8 -*-
from string import lower, punctuation as stringPunctuation
from stemming.porter2 import stem
from re import sub

class Quote(object):
	"""docstring for Quote"""
	def __init__(self, content):
		super(Quote, self).__init__()
		self.content = content
		self.wordsUnique = []

		# Sanitize the content of a quote
		self.sanitize()

	def sanitize(self):
		"""Sanitize and normalize the content of a quote"""

		# Lowercase
		self.content = lower(self.content)

		# Replace smileys with words
		self.content = sub("♥|<3", "heartsmiley", self.content)
		self.content = sub(":\)|:-\)|;\)|;-\)", "happysmiley", self.content)
		self.content = sub(":\(|:-\(|:'\(|:/", "sadsmiley", self.content)

		# Stem each word of the sentence
		self.content = ' '.join([stem(word) for word in self.content.split()])
		
		# Remove punctuation
		self.content = "".join(l for l in self.content if l not in stringPunctuation)

	def getContent(self):
		return self.content

	def loadWordsUnique(self):
		self.wordsUnique = open('tmp/wordsUnique.txt').read().split()

	def process(self, wordsUnique = None):
		"""Compute the vector of position of words for a quote"""
		
		terms = self.getContent().split()
		
		# Load wordsUnique if it was not given
		if wordsUnique is None:
			# Check if wordsUnique was not loaded
			if len(self.wordsUnique) == 0:
				self.loadWordsUnique()
			wordsUnique = self.wordsUnique

		# For each word of the quote, determine
		# the position of the word in wordsUnique
		positions = []
		for term in terms:
			if term in wordsUnique:
				index = wordsUnique.index(term)
				if index not in positions: positions.append(index)

		# Compute the final vector
		# 1 if the word is present in the quote
		# 0 otherwise 
		vector = []
		for i in range(len(wordsUnique)):
			if i in positions:
				vector.append(1)
			else:
				vector.append(0)

		return vector