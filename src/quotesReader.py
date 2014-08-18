from csv import DictReader
from quote import *
	
class QuotesReader():
	"""docstring for QuotesReader"""
	def __init__(self, filename, approvedName = None, contentName = None):
		self.filename = filename
		self.rows = DictReader(open(filename))

		# Set the default value for the approved column
		if approvedName is None: self.approvedName = "approved"
		else: self.approvedName = approvedName

		# Set the default value for the content column
		if contentName is None: self.contentName = "content"
		else: self.contentName = contentName

		self.getTextAndApproved()
		self.extractUniqueWords()
		self.wordPosition()
		
	def getTextAndApproved(self):
		"""Read a file and create a list of the content of quotes and a list with the associated moderation decision"""
		
		rows = self.rows
		
		quotes         = []
		quotesText     = []
		quotesApproved = []
		
		for row in rows:
			approved = int(row[self.approvedName])

			# Keep only published or refused quotes
			if approved in [-1, 1]:
				q = Quote(row[self.contentName])
				quotes.append(q)
				quotesText.append(q.getContent())
				quotesApproved.append(approved)

		self.quotesApproved = quotesApproved
		self.quotesText     = quotesText
		self.quotes         = quotes

	def extractUniqueWords(self):
		"""Builds a list of whitespace delimited tokens from a list of strings."""			

		words = ' '.join(self.quotesText)
		wordsUnique = []

		# Get non unique terms.
		wordsNonUnique = words.split()

		# Build the list of unique terms
		for term in wordsNonUnique:
			if term not in wordsUnique: wordsUnique.append(term)

		self.wordsUnique = wordsUnique
		self.saveWordsUnique()

	def saveWordsUnique(self):
		out = open('tmp/wordsUnique.txt', 'w')
		out.write(' '.join(self.wordsUnique))

	def wordPosition(self):
		"""Compute the vector of position of words for each quotes"""
		
		vectorPositions = []
		for quote in self.quotes:
			vectorPositions.append(quote.process(self.wordsUnique))

		self.wordPosition = vectorPositions
	
	def getApprovedAndWordPosition(self):
		return self.quotesApproved, self.wordPosition