__author__ = 'zhangye'
import os
import xlrd
from nltk.corpus import stopwords
from textblob import TextBlob
import re
import codecs
from dateutil.parser import parse
#this program generates sentence files for GENIA tagger

stops = set(stopwords.words('english'))
#if these words are in the sentence, ignore the sentence
ignore = ["posted on","word count","sentence","title","press release issued","date:","body:"]
def is_ignore(text):
    if(text.startswith("words") or text.startswith("title") or text.startswith("body -") or text.startswith("sentences")
       or text.startswith("sentence count") or text.startswith("date:") or text.startswith("date published:")
       or text.startswith("published on") or text.startswith("posted ")):
         return 1
    for str in ignore:
        if(str in text):
            return 1
    return 0

def is_date(string):
    try:
        parse(string)
        return 1
    except ValueError:
        return 0

def ignore_left(string):       #ignore rest of the text if current line contains certain words
    if "notes to editors" in string or "for further information" in string\
        or "please contact:" in string or "link to paper:" in string:
         return True
    else:
        return False
Chambers_sentence = "Chambers_sen/"
j = 1
dic = {}     #key is the term, value is the list of files where it appears
for file_name in os.listdir("1. excel files"):
    if file_name.endswith("csv"):
        filename = file_name.split('.')[0]
        f = codecs.open("5. Press releases/"+filename[:-2]+".txt",'r',encoding='utf-8')
        text = f.readlines()
        text = [i.encode('ascii','ignore') for i in text]
        writeFile = open(Chambers_sentence+filename+".txt",'wb')
        #check each line  whether contains relationship terms
        k = 0
        title_flag = 0
        while (k < (len(text))):
            line = text[k]
            original = line
            if(line.strip().isspace() or not line):  #line is empty
                k += 1
                continue
            line = line.strip()
            if(is_ignore(line.lower())):      #line contains 'removable' words
                k += 1
                continue
            if(k<=10 and is_date(line)==1):   #line contains date
                k += 1
                continue
            #write the current line with the label into the sentences directory
            if (ignore_left(line.lower())):
                break
            if line:
                writeFile.write(line+"\n")
            k += 1
        writeFile.close()
