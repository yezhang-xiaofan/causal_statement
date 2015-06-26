__author__ = 'zhangye'
#this programs is a script that taggs a directory of files
import subprocess
import os
tagged_dir = "tagged"
senten_dir = "../Chambers_sen"
for file in os.listdir(senten_dir):
    f = open(tagged_dir+"/"+file,'wb')
    temp = subprocess.Popen(["./geniatagger", "<", senten_dir+"/"+file],shell=True,stdout=f)
    temp.kill()
    print file+"...done."
