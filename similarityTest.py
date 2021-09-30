#!/usr/bin/env python
# coding=utf-8

import subprocess
import os
import sys
import time
from func_timeout import func_timeout, FunctionTimedOut
import networkx as nx
from networkx.algorithms import isomorphism
import networkx.algorithms.isomorphism as iso

CFGScanDroid= "C:/Users/wilso/Desktop/Final_Year_Project/Core_Files/repackagedAPK/CFGScanDroid-master/target/CFGScanDroid-0.1-jar-with-dependencies.jar"   #Absolute path of the folder containing the CFGScanDroid .jar file
originalAPK = "C:/Users/wilso/Desktop/Final_Year_Project/Core_Files/repackagedAPK/originalAPK/"															#Absolute path to the folder containing the original APKs
repackagedAPK = "C:/Users/wilso/Desktop/Final_Year_Project/Core_Files/repackagedAPK/repackagedAPK/"														#Absolute path to the folder containing the repackaged APKs
sigdump_OPath = "C:/Users/wilso/Desktop/Final_Year_Project/Core_Files/repackagedAPK/sigdump_O/"															#Absolute path to the folder containing the CFG signatures of original APKs
sigdump_RPath = "C:/Users/wilso/Desktop/Final_Year_Project/Core_Files/repackagedAPK/sigdump_R/"															#Absolute path to the folder containing the CFG signatures of repackaged APKs

APK1 = "05F25C4B6A02A5F5724268518DB984BE7C2627DBA16695EF6FFDE029EDD3AE26"										#Original APK Sample 1
APK2 = "B5F5128B41D9445883799ED438D170E1B7D1DFF2364B05C5EA6436A9B46F0F1A"										#Repackaged APK of Sample 1	


timeout = 5

######## Scan and dump APK's CFG signatures into .txt files #########

def scanDumpSig():

	#APK1 = raw_input("Enter the name of the original APK: ")
	selectedAPK1 = APK1 + '.apk'
	#APK2 = raw_input("Enter the name of the possible repackaged APK: ")
	selectedAPK2 = APK2 + '.apk'

	apk_1 = os.path.join(originalAPK,selectedAPK1)
	apk_2 = os.path.join(repackagedAPK,selectedAPK2)

	if os.path.exists(apk_1) and os.path.exists(apk_2):
			
		cmd1 = 'java -jar ' + CFGScanDroid + ' -d -b -f ' + apk_1 + ' > ' + sigdump_OPath + '/' + APK1 + '.txt'
		cmd2 = 'java -jar ' + CFGScanDroid + ' -d -b -f ' + apk_2 + ' > ' + sigdump_RPath + '/' + APK2 + '.txt'
		print ("Extracting CFG signatures from original APK ...")	
		os.system(cmd1)
		print ("Extracting CFG signatures from possible repackaged APK ...")
		os.system(cmd2)
		return APK1, APK2
	
	elif not os.path.exists(apk_1) and os.path.exists(apk_2):
		print (apk_1 + " not found! Exiting Program...")
		sys.exit()
	elif os.path.exists(apk_1) and not os.path.exists(apk_2):
		print (apk_2 + " not found! Exiting Program...")
		sys.exit()
	else:
		print (apk_1 + " and " + apk_2 + " not found! Exiting Program...")
		sys.exit()

######## Create networkx graph based on CFG signature's format #########

def createGraph(lines):

	line = lines.split(";")
	G = nx.DiGraph()
	i = 0

	while(i < len(line)):
		if (i == 0):
			sigName = line[i] #line[0] = Signature's Name
		elif (i == 1):
			nodes = line[i]  #line[1] = Number of nodes to be created
			if (int(nodes) > 100000):
				break
		else:
			c2 = 0
			x = line[i].split(":")
			while (c2 < 1):
				n = x[1].split(",")
				for n1 in n:
					if "\n" in n1:
						n1 = n1.replace("\n","")
					G.add_edge(x[0],n1)
				c2 += 1

		i += 1

    #print (line)
    #print (x)
    #print (len(x))
    #print (x[0])
	#print (sorted(G.nodes))
	#print (sorted(G.edges))
	#exit()
	return G, sigName

######## VF2 Algorithm #########

def matching(graph_1, graph_2,matchCount):
	graphMatch = isomorphism.DiGraphMatcher(graph_1,graph_2)
	#if graphMatch.subgraph_is_isomorphic():
	if graphMatch.is_isomorphic():
	#if nx.could_be_isomorphic(graph_1, graph_2):
	#if nx.is_isomorphic(graph_1,graph_2):
		matchCount += 1
		print ("\nMatch found!")
		print ("\nMatched Counter:")
		print (matchCount)
		print ("")
		graph_1.clear()
		graph_2.clear()
		return matchCount
	else:
		print ("\nNo match!\n")
		graph_1.clear()
		graph_2.clear()
		return matchCount

######## Comparing graphs of original and repackaged APKs #########

def matchGraph(APK1,APK2):

	sigdump_1 = APK1 + '.txt'
	sigdump_2 = APK2 + '.txt'
	
	sigdump_1 = os.path.join(sigdump_OPath,sigdump_1)
	sigdump_2 = os.path.join(sigdump_RPath,sigdump_2)

	timeStart = time.perf_counter()

	if os.path.exists(sigdump_1) and os.path.exists(sigdump_2):
						
		
		openSigdump_O = open(sigdump_1,"r+")
		openSigdump_R = open(sigdump_2,"r+")

		print ("Formatting 1st Signature file ...")
		#Removing irrelevant line in 1st Signature file
		readSigdump_O = openSigdump_O.readlines()
		openSigdump_O.close()
		del readSigdump_O[0]
		editSigdump_O = open(sigdump_1,"w+")
		for line in readSigdump_O:
			editSigdump_O.write(line)
		editSigdump_O.close()

		print ("Formatting 2nd Signature file ...")
		#Removing irrelevant line in 2nd Signature file
		readSigdump_R = openSigdump_R.readlines()
		openSigdump_R.close()
		del readSigdump_R[0]
		editSigdump_R = open(sigdump_2,"w+")
		for line in readSigdump_R:
			editSigdump_R.write(line)
		editSigdump_R.close()
	
		print ("Formatting completed! Beginning similarity test ...\n")
		openSigdump_O = open(sigdump_1,"r+")
		openSigdump_R = open(sigdump_2,"r+")		

	elif not os.path.exists(sigdump_1) and os.path.exists(sigdump_2):
		print (sigdump_1 + " not found! Exiting Program...")
		sys.exit()
	elif os.path.exists(sigdump_1) and not os.path.exists(sigdump_2):
		print (sigdump_2 + " not found! Exiting Program...")
		sys.exit()
	else:
		print (sigdump_1 + " and " + sigdump_2 + " not found! Exiting Program...")
		sys.exit()
	
	readSigdump_O = openSigdump_O.readlines()
	readSigdump_R = openSigdump_R.readlines()

	matchCount = 0

	for line1 in readSigdump_O:
		if "\n" in line1:
			line1 = line1.replace("\n","")
		graph_1, sigName1 = createGraph(line1)
		print (sigName1)
		for line2 in readSigdump_R:
			if "\n" in line2:
				line2 = line2.replace("\n","")
			if sigName1 in line2:
				graph_2, sigName2 = createGraph(line2)
				print (sigName2)
				print ("\nChecking similarity ...")
				try:
					matchCount = func_timeout(timeout,matching,args=(graph_1,graph_2,matchCount))
					break
				except FunctionTimedOut:
					print("\nTimeout!! Skipping component...\n")
					break

	score = float((matchCount * 100.00)/(min(len(readSigdump_O),len(readSigdump_R))))

	timeEnd = time.perf_counter()
	timeTaken = timeEnd - timeStart

	print ("\n--- Similarity Test Result ---\n")
	print ("Total Match Counter: ")
	print (matchCount)
	print ("\nCFG Signature List 1's Total Count:")
	print (len(readSigdump_O))
	print ("\nCFG Signature List 2's Total Count:")
	print (len(readSigdump_R))
	print ("\nSimilarity Percentage: " + ("{:.2f}".format(round(score,2))) + "%")
	print ("\nElapsed Time: " + ("{:.2f}".format(round(timeTaken,2))) + " seconds\n")
	
	openSigdump_O.close()
	openSigdump_R.close()

if __name__ == '__main__':	
		
	APK1, APK2 = scanDumpSig()
	matchGraph(APK1,APK2)