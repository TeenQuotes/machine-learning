from quotesReader import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV

qr = QuotesReader('data/realQuotes.csv')
quotesText, approved = qr.getQuotesTextAndApprove()
print "Retrieved quotesText and approved"
x_train, x_test, y_train, y_test = train_test_split(quotesText, approved, test_size = 0.4, random_state = 42)
vectorizer = TfidfVectorizer()
print "Training the tf-idf vectorizer"
x_train = vectorizer.fit_transform(x_train)
x_test = vectorizer.transform(x_test)

tunedParameters = [{'C': [1, 10, 20, 50], 'kernel': ['linear']}]

scores = ['recall', 'precision']

for score in scores:
    print("## Tuning hyper-parameters for %s" % score)

    clf = GridSearchCV(SVC(C=1), tunedParameters, cv = 2, scoring = score, verbose = True)
    clf.fit(x_train, y_train)

    print("Best parameters set found on development set:")
    print(clf.best_estimator_)
    print("Grid scores on development set:")
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() / 2, params))

    print("Detailed classification report:")
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    y_true, y_pred = y_test, clf.predict(x_test)
    print(classification_report(y_true, y_pred))