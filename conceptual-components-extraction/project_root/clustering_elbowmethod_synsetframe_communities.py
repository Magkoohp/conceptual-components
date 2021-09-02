import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import sys
from yellowbrick.cluster import KElbowVisualizer
import numpy as np

def my_tokenizer(text):
    tokens = text.split(",")
    
    return tokens

def cluster_synsetframe_communities(filtered_enriched_synsetframe_csv, clusters_output_csv):
	colnames = ['community', 'doc', 'annotatedtext' , 'synsetframe', 'filteredsynsetframe', 'synsetframetriplet','nounverbwoframe', 'adjadvwoframe', 'annotatedsynsetframe']
	data = pd.read_csv(filtered_enriched_synsetframe_csv, skiprows=[0], names=colnames)

	community = data.community.tolist()
	docs = data.doc.tolist()
	annotateddocs = data.annotatedtext.tolist()
	wordnets = data.synsetframe.tolist()
	filteredsynsetframes = data.filteredsynsetframe.tolist()
	synsetframetriplets = data.synsetframetriplet.tolist()
	nounverbs = data.nounverbwoframe.tolist()
	adjadvs = data.adjadvwoframe.tolist()

	tfidf_vectorizer = TfidfVectorizer(max_df=0.90, max_features=200000, min_df=1, use_idf=True, tokenizer=my_tokenizer, ngram_range=(1,1))

	tfidf_matrix = tfidf_vectorizer.fit_transform(filteredsynsetframes) #fit the vectorizer to filteredsynsetframe

	terms = tfidf_vectorizer.get_feature_names()
	model = KMeans()
	visualizer = KElbowVisualizer(model, k=np.arange(1, 300, 10), timings= True)
	visualizer.fit(tfidf_matrix)
	optimal_k = visualizer.elbow_value_ 
	
	num_clusters = optimal_k

	agg = KMeans(n_clusters=num_clusters)
	agg.fit(tfidf_matrix.toarray())
	clusters = agg.labels_.tolist()

	arco_vd = { 'community': community, 'cluster': clusters, 'doc': docs, 'annotateddoc': annotateddocs, 'synsetframe': filteredsynsetframes, 'synsetframe triplet': synsetframetriplets, 'noun/verb w/o frame': nounverbs, 'adj/adv w/o frame': adjadvs}
	frame = pd.DataFrame(arco_vd, index = [clusters] , columns = ['community', 'cluster', 'doc', 'annotateddoc', 'synsetframe', 'synsetframe triplet', 'noun/verb w/o frame', 'adj/adv w/o frame'])


	frame.to_csv(clusters_output_csv)

	print(frame['cluster'].value_counts()) #number of docs per cluster


if __name__ == '__main__':
	cluster_synsetframe_communities(sys.argv[1], sys.argv[2])
