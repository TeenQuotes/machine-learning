from quotesReader import *
from sklearn import svm, cross_validation

qr = QuotesReader('data/realQuotes.csv')
approved, wordPosition = qr.getApprovedAndWordPosition()
X_train, X_test, y_train, y_test = cross_validation.train_test_split(wordPosition, approved, test_size=0.4, random_state=0)
clf = svm.SVC(kernel = "rbf")
clf.fit(X_train, y_train)
print clf.score(X_test, y_test)