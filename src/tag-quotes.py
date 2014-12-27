from __future__ import print_function

from quotesReader import *

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline

from sklearn.cluster import KMeans, MiniBatchKMeans

import logging
from optparse import OptionParser
import sys
from time import time

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Parse CLI arguments
op = OptionParser()
op.add_option("--no-minibatch", action="store_false", dest="minibatch", default=True,
							help="Use ordinary k-means algorithm (in batch mode).")
op.add_option("--no-idf", action="store_false", dest="use_idf", default=True,
							help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--use-hashing", action="store_true", default=False,
							help="Use a hashing feature vectorizer")
op.add_option("--n-features", type=int, default=10000,
							help="Maximum number of features (dimensions) to extract from text.")
op.add_option("--nb-clusters", type=int, default=5,
							help="The number of categories we want to create")
op.add_option("--verbose", action="store_true", dest="verbose", default=False,
							help="Print progress reports inside k-means algorithm.")

print(__doc__)
op.print_help()

(opts, args) = op.parse_args()
if len(args) > 0:
		op.error("This script takes no arguments.")
		sys.exit(1)

###############################################################################
# Read quotes

qr = QuotesReader('data/realQuotes.csv', ["approve"], False)
dataset, approved = qr.getQuotesTextAndApprove()
nbClusters = opts.nb_clusters
print("%d documents" % len(dataset))
print("%d number of clusters" % nbClusters)
print()

###############################################################################
# Extract features
print("Extracting features from the dataset using a sparse vectorizer")
t0 = time()
if opts.use_hashing:
		if opts.use_idf:
				# Perform an IDF normalization on the output of HashingVectorizer
				hasher = HashingVectorizer(n_features=opts.n_features,
																	 stop_words='english', non_negative=True,
																	 norm=None, binary=False)
				vectorizer = make_pipeline(hasher, TfidfTransformer())
		else:
				vectorizer = HashingVectorizer(n_features=opts.n_features,
																			 stop_words='english',
																			 non_negative=False, norm='l2',
																			 binary=False)
else:
		vectorizer = TfidfVectorizer(max_df=0.5, max_features=opts.n_features,
																 min_df=2, stop_words='english',
																 use_idf=opts.use_idf)
X = vectorizer.fit_transform(dataset)

print("Done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)
print()

###############################################################################
# Do the actual clustering

if opts.minibatch:
		km = MiniBatchKMeans(n_clusters=nbClusters, init='k-means++', n_init=1,
												 init_size=1000, batch_size=1000, verbose=opts.verbose)
else:
		km = KMeans(n_clusters=nbClusters, init='k-means++', max_iter=100, n_init=1,
								verbose=opts.verbose)

print("Clustering sparse data with %s" % km)
t0 = time()
km.fit(X)
print("Done in %0.3fs" % (time() - t0))
print()

# Store the ID of each quote in a list by cluster number
k = 0
clusters = {}
for prediction in km.labels_:
	if prediction not in clusters:
		clusters[prediction] = [k]
	else:
		clusters[prediction].append(k)

	k += 1

if not opts.use_hashing:
		print("Top terms per cluster:")
		order_centroids = km.cluster_centers_.argsort()[:, ::-1]
		terms = vectorizer.get_feature_names()
		for i in range(nbClusters):
				print("Cluster %d (%i elements):" % (i, len(clusters[i])), end='')
				for ind in order_centroids[i, :10]:
						print(' %s' % terms[ind], end='')
				print()