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

base_folder = "//home//kevin//workspace//SourceForge//final"
punctuations = "[!\"#$%&'()*+,./:;<=>?@[\]^`{|}]'"
trantab = maketrans(punctuations, " " * len(punctuations))

py_keywords = set(word.strip() for word in open("python.txt"))
c_keywords = set(word.strip() for word in open("c.txt"))
cpp_keywords = set(word.strip() for word in open("c++.txt"))
java_keywords = set(word.strip() for word in open("java.txt"))
english_stop_words = set(word.strip() for word in open("stop_words.txt"))

english_stop_words = english_stop_words.union(py_keywords, c_keywords, cpp_keywords, java_keywords)


def parseFolder(srcFolder):
    for (path, subfolder, files) in os.walk(srcFolder):
        for file_name in files:
            if re.search(r"(zip|tar.gz|jar)", file_name):
                print path + "//" + file_name
                

def calculateDocumentFrequency(srcFolder):
    doc_keyword_count = {}
    doc_keyword_count = defaultdict(lambda: 0)

    for (path, subfolder, files) in os.walk(srcFolder):
        for file_name in files:
            if re.search(r"(.+\.txt|.+\.readme|.+\.html)", file_name):
                print file_name
                src_file_path = path + "//" + file_name

                with open(src_file_path) as document:
                    for line in document:
                        line = line.strip().translate(trantab)  # remove punctuations
                        for unique_word in filter(lambda x: x not in english_stop_words, map(lambda x: x.lower(), line.split())):
                            doc_keyword_count[unique_word] += 1

    # for word in sorted(doc_keyword_count, key=doc_keyword_count.get, reverse=True):
    #     print word, doc_keyword_count[word]


def calculateSrcFrq(srcFolder):
    ''' pass the src folder and it creates a frequency count of the words
    occuring in the source file
    * remove the keywords
    * remove certain punctuations
    for now it handles .py .c .cpp and .java files
    '''
    
    src_keyword_count = {}
    src_keyword_count = defaultdict(lambda: 0)

    for (path, subfolder, files) in os.walk(srcFolder):
        
        for file_name in files:
            
            
            if re.search(r"(.+\.py|.+\.cpp|.+\.c|.+\.java)", file_name):
                print file_name
                stop_words = set([])
                
                if re.search(r".py", file_name):
                    stop_words = py_keywords
                elif re.search(r".cpp", file_name):
                    stop_words = cpp_keywords
                elif re.search(r".c", file_name):
                    stop_words = c_keywords
                else:
                    stop_words = java_keywords
                
                src_file_path = path + "//" + file_name

                with open(src_file_path) as src_code:
                    for line in src_code:
                        line = line.strip().translate(trantab)  # remove punctuations
                        for unique_word in filter(lambda x: x not in stop_words, map(lambda x: x.lower(), line.split())):
                            src_keyword_count[unique_word] += 1

    for word in sorted(src_keyword_count, key=src_keyword_count.get, reverse=True):
        print word, src_keyword_count[word]


if __name__ == '__main__':
    parseFolder("//home//kevin//workspace//SourceForge//py_scripts//test")