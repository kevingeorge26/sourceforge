"""
@author: kevin

script to print all the bigrams and trigrams from the documentation of projects in sorted order

"""
import nltk
from nltk.collocations import *
import os
import shutil
import re
from collections import defaultdict
from string import maketrans
import math

base_folder = "//home//kevin//workspace//SourceForge//final"
punctuations = "[!\"#$%&'()*+,./:;<=>?@[\]^`{|}]'-"
trantab = maketrans(punctuations, " " * len(punctuations))
english_stop_words = set(word.strip() for word in open("stop_words.txt"))
py_keywords = set(word.strip() for word in open("python.txt"))
c_keywords = set(word.strip() for word in open("c.txt"))
cpp_keywords = set(word.strip() for word in open("c++.txt"))
java_keywords = set(word.strip() for word in open("java.txt"))

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

def read_project(project_path, project_name):
    print project_name
    allwords = []
    for (path, subfolder, files) in os.walk(project_path):
        for file_name in files:
             
             if re.search(r"(.+\.txt$|.+\.readme$|.+\.html$)", file_name):
                src_file_path = path + "//" + file_name
                with open(src_file_path) as document:
                    for line in document:
                        line = line.strip().translate(trantab)  # remove punctuations
                        allwords.extend(filter(lambda x: x not in english_stop_words, map(lambda x: x.lower(), line.split())))            

   
    # calculate bigrams
    finder = BigramCollocationFinder.from_words(allwords)
    scored = finder.score_ngrams( bigram_measures.raw_freq  )
    
    scored.sort(key = lambda x:x[1],reverse=True)
    
    result_file = open(base_folder + "//..//bigrams//" + project_name + ".txt", "w")
    result_file.write("Project folder name = %s \n" %(project))
    result_file.write("********************************************************************************************** \n\n")

    for items in scored:
        result_file.write(" ( %s , %s ) = %f \n" % (items[0][0], items[0][1], items[1]) )

    result_file.close()

    # calculate trigrams
    finder = TrigramCollocationFinder.from_words(allwords)
    scored = finder.score_ngrams( trigram_measures.raw_freq  )

    scored.sort(key = lambda x:x[1],reverse=True)
    
    result_file = open(base_folder + "//..//trigrams//" + project_name + ".txt", "w")
    result_file.write("Project folder name = %s \n" %(project))
    result_file.write("********************************************************************************************** \n\n")

    for items in scored:
        result_file.write(" ( %s , %s ,%s) = %f \n" % (items[0][0], items[0][1], items[0][2], items[1]) )

    result_file.close()



if __name__ == '__main__':
    for project in os.listdir(base_folder):
        read_project(base_folder + "//" + project,project)    