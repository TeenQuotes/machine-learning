from csv import DictReader
from collections import Counter
from numpy import linspace
from math import floor
from quote import *

class QuotesReader():
	"""Read a bunch of quotes"""
	def __init__(self, filename, keepTypes = ["approve", "refuse"], useStemming = True, approvedColumnName = None, contentColumnName = None):
		self.filename = filename
		self.keepTypes = keepTypes
		self.useStemming = useStemming
		self.rows = DictReader(open(filename))

		# Set the default value for the approved column
		if approvedColumnName is None: self.approvedName = "approved"
		else: self.approvedName = approvedColumnName

		# Set the default value for the content column
		if contentColumnName is None: self.contentName = "content"
		else: self.contentName = contentColumnName

		self.getTextAndApproved()

	def getTextAndApproved(self):
		"""Read a file and create a list of the content of quotes
		and a list with the associated moderation decision"""

		rows = self.rows

		quotes         = []
		quotesText     = []
		quotesApproved = []

		for row in rows:
			approve = int(row[self.approvedName])
			q = Quote(row[self.contentName], approve, self.useStemming)

			# Keep only published or refused quotes
			if "approve" in self.keepTypes and q.isApproved():
				quotes.append(q)
			if "refuse" in self.keepTypes and q.isRefused():
				quotes.append(q)

		for q in quotes:
			if q.isApproved(): quotesApproved.append(1)
			else: quotesApproved.append(0)

		self.quotesApproved = quotesApproved
		self.quotesText     = [q.getContent() for q in quotes]
		self.quotes         = quotes

		print "%i exploitable quotes found" % len(quotes)

	def extractUniqueWords(self):
		"""Builds a list of whitespace delimited tokens from a list of strings."""

		words = ' '.join(self.quotesText)

		# Create a dictionnary word: nbOccurences
		freqs = Counter(words.split())

		# Keep words that appear at least 5 times
		freqs = {word: count for word, count in freqs.iteritems() if count >= 5}

		# Keep only the words
		wordsUnique = freqs.keys()

		print "Extracted %i unique words" % len(wordsUnique)

		self.wordsUnique = wordsUnique
		self.saveWordsUnique()

	def saveWordsUnique(self):
		"""Save the list of wordsUnique in a text file"""
		out = open('tmp/wordsUnique.txt', 'w')
		out.write(' '.join(self.wordsUnique))

	def constructListProgress(self):
		"""Create a list containing the ID for each 10 % of the total number of quotes
		For example if we have 10 quotes: [1 2 ... 9 10]"""

		nbQuotes = len(self.quotes)
		rangeProgress = linspace(0.1 * nbQuotes, nbQuotes, 10)
		rangeProgress = map(floor, rangeProgress)
		rangeProgress = map(int, rangeProgress)

		return rangeProgress

	def wordPosition(self):
		"""Compute the vector of position of words for each quotes"""

		print "Computing the vector for each quote"
		vectorPositions = []
		idQuote = 1
		rangeProgress = self.constructListProgress()

		for quote in self.quotes:
			# Print the progress
			if idQuote in rangeProgress:
				index = (rangeProgress.index(idQuote) + 1) * 10
				print "%i%% done" % index
			vectorPositions.append(quote.process(self.wordsUnique))
			idQuote += 1

		self.wordPosition = vectorPositions

	def getApprovedAndWordPosition(self):
		self.extractUniqueWords()
		self.wordPosition()
		return self.quotesApproved, self.wordPosition

	def getQuotesTextAndApprove(self):
		return self.quotesText, self.quotesApproved