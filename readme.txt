Software Requirements:

- Java JRE 1.8.0 / Java OpenJDK version 11.0.8
- Python 2.7.17 / 3.6.7


Instructions to use the similarityTest.py script:

1) Open the script in text editor (E.g: Notepad++, Visual Studio, etc)

2) Change the absolute pathnames of the following folders to reflect the files' locations on your system:
	- CFGScanDroid (CFGScanDroid .jar file location)
	- originalAPK (Folder containing original APK files)
	- repackagedAPK (Folder containing repackaged APK files)
	- sigdump_OPath (Folder containing signatures .txt files of original APKs)
	- sigdump_RPath (Folder containing signatures .txt files of repackaged APKs)

3) Install networkx modules onto the Python platform (E.g: pip install networkx)

4) Ensure the APK files are indeed in the respective folders as indicated in Step 2.

5) Run the python file (E.g: "python similarityTest.py") and follow the program's instructions
