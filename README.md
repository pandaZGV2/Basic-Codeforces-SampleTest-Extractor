# Codeforces API Experimentation
---
## Basic-Codeforces-SampleTest-Extractor
This is a basic Codeforces Sample Testcase Extractor. It uses a simple bash script to run the required file (CPP/C) after extracting the sample input cases from CodeForces.
### Running the Shell Script
Example:
```console
$ chmod +x RCPP.sh
$ ./RCPP.sh 1469A.cpp
```
### Requirements
* Python3
* BeautifulSoup
* lxml
* numpy
* seaborn

## Rating Plotter for Codeforces
Run the program `Getuserratingplot.py` and enter the username of the person whose rating you want to plot. It uses the codeforces API to receive rating history in `JSON` format. The program then parses the data and plots it accordingly.
