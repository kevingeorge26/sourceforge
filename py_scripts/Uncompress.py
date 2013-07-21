"""
@author: kevin

this is script is used unzip folder of type
jar, tar.gz , zip"""

from pyunpack import Archive
import os
import shutil
import re
from collections import defaultdict
from string import maketrans
import math

base_folder = "//home//kevin//workspace//SourceForge//final"
punctuations = "[!\"#$%&'()*+,./:;<=>?@[\]^`{|}]'-"
trantab = maketrans(punctuations, " " * len(punctuations))

py_keywords = set(word.strip() for word in open("python.txt"))
c_keywords = set(word.strip() for word in open("c.txt"))
cpp_keywords = set(word.strip() for word in open("c++.txt"))
java_keywords = set(word.strip() for word in open("java.txt"))
english_stop_words = set(word.strip() for word in open("stop_words.txt"))

english_stop_words = english_stop_words.union(py_keywords, c_keywords, cpp_keywords, java_keywords)


def parseFolder(srcFolder):
    for project in os.listdir(srcFolder):
        path = srcFolder + "//" + project
        
        for file_name in os.listdir(path):
            if re.search(r"(zip$|tar.gz$|jar$)", file_name):
                try:
                    Archive(path + "//" + file_name).extractall(path)
                    
                    doc_keyword_dict, total_word_count_doc, total_document_count = calculateDocumentFrequency(path)
                    code_keyword_dict, total_count_code = calculateSrcCodeFrq(path)

                    if doc_keyword_dict and code_keyword_dict:
                        common_word_set = set(code_keyword_dict.keys()).intersection(set(doc_keyword_dict.keys()))
                        result_file = open(srcFolder + "//" + "result"+"//" + project + ".txt", "w")
                        result_dict = {}
                        
                        result_file.write("Project folder name = %s \n" %(project))
                        result_file.write("********************************************************************************************** \n\n")

                        for word in common_word_set:
                            result_dict[word] = code_keyword_dict[word]
                            # result_dict[word] = (doc_keyword_dict[word][0] / float(total_word_count_doc) ) * math.log10(total_document_count/ float(doc_keyword_dict[word][1])) 
                       
                         
                        for word in sorted(result_dict,key=result_dict.get,reverse=True):
                            tfidf = (doc_keyword_dict[word][0] / float(total_word_count_doc) ) * math.log10(total_document_count/ float(doc_keyword_dict[word][1])) 
                            result_file.write(" word = %s | frequency in documentation = %d | frequency in source code = %d | tf-idf = %f \n" %(word, doc_keyword_dict[word][0], code_keyword_dict[word], tfidf))

                        result_file.close()
                except:
                    print "***********error for folder*********** " +project


def calculateDocumentFrequency(srcFolder):
    """
    @return
    dict = key = word , [freq of the word , number of documents it was found]
    integer = total number of words 
    integer = total number of documents
    """
    doc_keyword_count = {}
    doc_keyword_count = defaultdict(lambda: [0,0])
    total_word_count = 0
    total_document_count = 0

    for (path, subfolder, files) in os.walk(srcFolder):
        for file_name in files:
            if re.search(r"(.+\.txt$|.+\.readme$|.+\.html$)", file_name):

                src_file_path = path + "//" + file_name

                words_in_file = set([])
                with open(src_file_path) as document:
                    for line in document:
                        line = line.strip().translate(trantab)  # remove punctuations
                        for unique_word in filter(lambda x: x not in english_stop_words, map(lambda x: x.lower(), line.split())):
                            doc_keyword_count[unique_word][0] += 1
                            words_in_file.add(unique_word)
                            total_word_count += 1

                for word in words_in_file:
                    doc_keyword_count[word][1] += 1

                total_document_count += 1


    # for word in sorted(doc_keyword_count, key=doc_keyword_count.get, reverse=True):
    #     print word, doc_keyword_count[word]
    return doc_keyword_count, total_word_count, total_document_count


def calculateSrcCodeFrq(srcFolder):
    ''' pass the src folder and it creates a frequency count of the words
    occuring in the source file
    * remove the keywords
    * remove certain punctuations
    for now it handles .py .c .cpp and .java files

    @return
    dict = key = word , freq in src
    integer = total words in src
    '''
    src_keyword_count = {}
    src_keyword_count = defaultdict(lambda: 0)
    total_count = 0

    for (path, subfolder, files) in os.walk(srcFolder):
        for file_name in files:          
            
            if re.search(r"(.+\.py$|.+\.cpp$|.+\.c$|.+\.java$|.+\.h$)", file_name):
                
                stop_words = set([])
                
                if re.search(r".+\.py$", file_name):
                    stop_words = py_keywords
                elif re.search(r".+\.cpp$", file_name):
                    stop_words = cpp_keywords
                elif re.search(r".+\.c$", file_name) or re.search(r".+\.h$", file_name):
                    stop_words = c_keywords
                else:
                    stop_words = java_keywords
                
                # print "reading src code  " + file_name
                src_file_path = path + "//" + file_name

                with open(src_file_path) as src_code:
                    for line in src_code:
                        line = line.strip().translate(trantab)  # remove punctuations
                        for unique_word in filter(lambda x: x not in stop_words, map(lambda x: x.lower(), line.split())):
                            src_keyword_count[unique_word] += 1
                            total_count += 1

    # for word in sorted(src_keyword_count, key=src_keyword_count.get, reverse=True):
    #     print word, src_keyword_count[word]
    return src_keyword_count, total_count


if __name__ == '__main__':
    parseFolder("//home//kevin//workspace//SourceForge//final")
    # parseFolder("//home//kevin//workspace//SourceForge//py_scripts//test")