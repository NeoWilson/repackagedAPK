#!/usr/bin/env python
# coding=utf-8
# download repackaging pairs

import os
import sys

sourceFile="C:/Users/wilso/Desktop/Final_Year_Project/Core_Files/v3/FYP/repackaging_pairs.txt"
originalAPK="C:/Users/wilso/Desktop/Final_Year_Project/Core_Files/v3/FYP/originalAPK/"
repackagedAPK="C:/Users/wilso/Desktop/Final_Year_Project/Core_Files/v3/FYP/repackagedAPK/"

originalList=os.listdir(originalAPK)
repackagedList={}

APIKEY="a52054307648be3c6b753eb55c093f4c2fa4b03e452f8ed245db653fee146cdd"

f=open(sourceFile)

downloadcnt=len(originalList)
print (downloadcnt)

x=0
y=0

for line in f.readlines():
    
    y = y + 1

    print ("Y is:{0}".format(y))

    line=line.replace("\n","")

    SHA256_ORIGINAL = line.split(",")[0]
    SHA256_REPACKAGE = line.split(",")[1]

    apkfile = SHA256_ORIGINAL+".apk"

    if apkfile in originalList:
        print (apkfile)
        index=originalList.index(apkfile)
        print (index)
        print ("the apk is..."+originalList[index])
        print ("The file exists!...")
        x = x + 1
        print ("X is {0}".format(x))
        continue
    else:
        print ("download apk....")
        curl = 'cd {0} && curl -O --remote-header-name -G -d apikey={1} -d sha256={2} https://androzoo.uni.lu/api/download'

    cmd = curl.format(originalAPK, APIKEY, SHA256_ORIGINAL)
    os.system(cmd)
    cmd = curl.format(repackagedAPK, APIKEY, SHA256_REPACKAGE)
    os.system(cmd)

    

    


f.close()
