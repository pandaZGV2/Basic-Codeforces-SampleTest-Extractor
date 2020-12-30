import sys
import json
import urllib.request,urllib.parse,urllib.error
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import re

contestno=re.findall("[0-9]+",sys.argv[1])
qno=re.findall("^[A-Z]",sys.argv[2])
# print(contestno, qno)
testno="1469"
testletter="D"
CFURL = "http://codeforces.com/contest/" + contestno[0] +"/problem/"+ qno[0]
html = urllib.request.urlopen(CFURL).read()
soup =BeautifulSoup(html,'html.parser')
div=soup.find_all('div', class_="input")
f = open("input.txt","w")
for i in div:
    a=i.find('pre')
    if a:
        f.write(a.text.strip())
f.close()        
# print(div)
# print(Problem_Info)


