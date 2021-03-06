import networkx as nx
from node2vec import Node2Vec
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def node2vec():

    # FILES
    EMBEDDING_FILENAME = './word2vec_test.model'
    EMBEDDING_MODEL_FILENAME = './word2vec_test.vector'
    EDGES_EMBEDDING_FILENAME='./node2vec_test.vector'


    word_list = []
    with open("mr_clean.txt", 'r', encoding='utf-8') as fd:
        content = fd.readlines()  # 70000条分词后的数据放在数组中
        for c in content:  # 逐条读取
            words = c.strip().split(" ")
            word_list += words

    print(word_list)
    
    graph = nx.Graph() 
    
    for ind, word, in enumerate(word_list[:-1]):
        graph.add_edge(word, word_list[ind+1])
    
    # Precompute probabilities and generate walks - **ON WINDOWS ONLY WORKS WITH workers=1**
    node2vec = Node2Vec(graph, dimensions=300, walk_length=30, num_walks=200, workers=4)  # Use temp_folder for big graphs
    
    # Embed nodes
    model = node2vec.fit(window=10, min_count=1, batch_words=4)  # Any keywords acceptable by gensim.Word2Vec can be passed, `diemnsions` and `workers` are automatically passed (from the Node2Vec constructor)
    
    model.wv.most_similar('2')  # Outpsut node names are always strings

    # Save embeddings for later use
    model.wv.save_word2vec_format(EMBEDDING_FILENAME)

    # Save model for later use
    model.save(EMBEDDING_MODEL_FILENAME)

    # Embed edges using Hadamard method
    from node2vec.edges import HadamardEmbedder

    edges_embs = HadamardEmbedder(keyed_vectors=model.wv)

    # Look for embeddings on the fly - here we pass normal tuples
    edges_embs[('1', '2')]

    # Get all edges in a separate KeyedVectors instance - use with caution could be huge for big networks
    edges_kv = edges_embs.as_keyed_vectors()

    # Look for most similar edges - this time tuples must be sorted and as str
    edges_kv.most_similar(str(('1', '2')))

    # Save embeddings for later use
    edges_kv.save_word2vec_format(EDGES_EMBEDDING_FILENAME)

node2vec();