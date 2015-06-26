__author__ = 'zhangye'
#this program annotates the tagged file with IV/DV and relationship terms
import os
import xlrd
from nltk.corpus import stopwords
from textblob import TextBlob
import re
stops = set(stopwords.words('english'))
def convert(str1):        #convert the original string to list of phrases/words
    if str1 == -9.0:
        return []
    if(type(str1) is unicode):
        str1 = str1.encode('ascii','ignore')
        str1 = str1.strip('.')
        str1 = str1.lower()
        str1 = str1.replace("see above","")
        str1 = str1.replace("as above","")
        str1 = str(TextBlob(str1).lower().correct())
        temp =  re.split(r'\.\. \.\.|,|/',str1)
        return [remove_mul_space((a.strip())) for a in temp if (a.strip().isspace()==False and a)]
    else:
        return []

def process_main_IV_DV(str1):    #convert IV/DV terms into list of terms
    if(str1!=-9 and str1!=0):
        IV_DV = str1.encode('ascii','ignore')
        return str(TextBlob(IV_DV.lower()).correct())

def process_second_IV_DV(str1):
    if str1==-9.0:
        return []
    if(type(str1) is unicode):
        str1 = str1.encode('ascii','ignore')
        str1 = str1.strip('.')
        str1 = str1.lower()
        str1 = str1.replace("see above","")
        str1 = str1.replace("as above","")
        str1 = str(TextBlob(str1.lower()).correct())
        temp =  re.split(r'\.\. \.\.|,|/',str1)
        return [remove_mul_space((a.strip())) for a in temp if (a.strip().isspace()==False and a)]
    else:
        return []

#def remove_punct(term):
 #   return " ".join(list(filter((lambda x: x not in stops),list(TextBlob(term).correct().words))))

#remove multiple spaces in the string
def remove_mul_space(str):
    return " ".join(str.split())

def charI_to_wordI(sentence,ori,charI):      #convert character index inside a string into the word index
    count = 0
    for wordI in range(len(ori)):
        if(len(ori[wordI])+count-1>=charI):
            return wordI
        count += (len(ori[wordI]) + 1)   #consider the space between words in the sentence

def main():
    tagged_dir = "geniatagger-3.0.1/tagged/"
    labeled_dir = "labelfiles/"
    for file_name in os.listdir("1. excel files"):
        if file_name.endswith(".xls") and not file_name.startswith("."):
            print file_name + " begin..."
            labled_file = open(labeled_dir + file_name[:-3]+".txt",'wb')
            book = xlrd.open_workbook("1. excel files/"+file_name)
            first_sheet = book.sheet_by_index(0)

            IV_title = process_main_IV_DV(first_sheet.cell(14,5).value)
            DV_title= process_main_IV_DV(first_sheet.cell(15,5).value)
            #rel_code_title = first_sheet.cell(19,5).value


            main_IV = process_main_IV_DV(first_sheet.cell(19,5).value)
            #print "main_IV: "+main_IV
            other_main_IV = process_second_IV_DV(first_sheet.cell(24,5).value)
            main_DV = process_main_IV_DV(first_sheet.cell(39,5).value)
            other_main_DV = process_second_IV_DV(first_sheet.cell(44,5).value)

            second_IV = process_main_IV_DV(first_sheet.cell(62,5).value)
            other_second_IV = process_second_IV_DV(first_sheet.cell(67,5).value)
            second_DV = process_main_IV_DV(first_sheet.cell(82,5).value)
            other_second_DV = process_second_IV_DV(first_sheet.cell(87,5).value)

            pri_relation = (first_sheet.cell(124,5).value)
            pri_code =  (first_sheet.cell(125,5).value)
            pri_terms = convert(first_sheet.cell(129,5).value)

            #sec_relation = (first_sheet.cell(136,5).value)
            sec_code = first_sheet.cell(137,5).value
            sec_terms = convert(first_sheet.cell(141,5).value)

            #build a dictionary of IV/DV terms and causal terms
            #key is the term   #value is the type
            term_dict = {}
            if IV_title!=-9: term_dict[IV_title] = "IV"
            if DV_title!=-9: term_dict[DV_title] = "DV"


            term_dict[main_IV] = "IV"
            for o in other_main_IV: term_dict[o] = "IV"
            term_dict[main_DV] = "DV"
            for o in other_main_DV: term_dict[o] = "DV"

            term_dict[second_IV] = "IV"
            for o in other_second_IV: term_dict[o] = "IV"
            term_dict[second_DV] = "DV"
            for o in other_second_DV: term_dict[o] = "DV"

            #term_dict[pri_relation] = "pri_rel"
            #if sec_relation!=-9: term_dict[sec_relation] = "sec_rel"
            for p in pri_terms: term_dict[p] = "pri_rel"
            for p in sec_terms: term_dict[p] = "sec_rel"

            for word in term_dict: print word,term_dict[word]
            filename = file_name.split(".")[0]
            f = open(tagged_dir+filename+".txt",'r')
            ori = []
            base = []
            pos = []
            chunk_tag = []
            ner = []
            line_no = 1
            for line in f:
                line = line.strip()
                if(len(line))==0:       #finish reading one sentence
                    num_tokens = len(ori)   #number of tokens in the sentence
                    #initialize the lables for IV/DV, causal terms and others
                    labels = ['Others'] * num_tokens
                    for word in term_dict:
                        if(word==None): continue
                        index = sentence.find(word)
                        if index != -1:
                            num_word = word.count(" ") + 1   # number of tokens in the 'word' term
                            num_pre_word = charI_to_wordI(sentence,ori,index)

                            # if this is "IV/DV"
                            if term_dict[word] == "IV" or term_dict[word] == "DV":
                                for j in range(num_word):
                                    labels[num_pre_word+j] = term_dict[word]
                            # if primary relationship, check whether code is greater than 0
                            elif term_dict[word] == "pri_rel":
                                if(pri_code>0):
                                    for j in range(num_word) : labels[num_pre_word+j] = "rel"
                            elif term_dict[word] == "sec_rel":
                                if(sec_code>0):
                                    for j in range(num_word): labels[num_pre_word+j] = "rel"

                            #if the IV/DV terms appear in the title



                    for k in range(len(ori)):
                        labled_file.write(ori[k]+"\t"+base[k]+"\t"+pos[k]+"\t" + chunk_tag[k]+"\t" + labels[k]+"\n")
                    labled_file.write("\n")
                    ori = []
                    base = []
                    pos = []
                    chunk_tag = []
                    ner = []

                else:
                    current = line.split("\t")
                    #print current
                    ori.append(current[0])
                    base.append(current[1])
                    pos.append(current[2])
                    chunk_tag.append(current[3])
                    ner.append(current[4])
                    sentence = " ".join([o.lower() for o in ori])
            labled_file.close()
            print file_name+" done..."
if __name__ == '__main__':
    main()
