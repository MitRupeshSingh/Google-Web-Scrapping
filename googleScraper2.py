# import library

from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib
import nltk
from nltk.util import ngrams

# the keyword for analyzing in a website
searchKeyword = str(raw_input("Enter the keyWord: "))

'''
fp = open(urlFilename, 'r')
line = fp.readline()
while line:
        word = line.strip()
        stopWords.append(word)
        savefile.write(word+",")		
        line = fp.readline()
		
fp.close()
'''

#get only text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# get only text from html
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)
			  

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

# n-grams for maximum repeated words count
def word_grams(words, min=1, max=5):
    s = []
    for n in range(min, max):
        for ngram in ngrams(words, n):
            s.append(' '.join(str(i) for i in ngram))
    return s

# get all the words 
def textScrap(html):
	entireText=""
	for words in text_from_html(html).encode("utf-8").strip().split(" "):
		if words!=" ":
			entireText=entireText.strip().lower()+" "+words.strip()
	return entireText


'''

a single html file is taken as input as google will block
your ip if you scrap through website long hours

'''

if __name__ == '__main__':

        #get top results as per user defined
	topResults = int(input("Input the number of top results: "))
	savefile=open("topResults.csv","a")
	#url for test
	html = urllib.urlopen('https://www.addictivetips.com/microsoft-office/find-correlation-between-datasets-in-excel-2010/').read()
	webUrl=urlName[0:urlName.index(.com)]+".com"
	stopWords = getStopWordList('stopwords.txt')

	entireText=textScrap(html)
	savefile.write(str(len(entireText.split(' '))))
	savefile.write(", ")

        #word count in the website
	wordCount = {}
	for words in word_grams(entireText.split(' ')):
		if words.strip()!=" " and words.strip()!="," and words.strip()!="/":
			if words in wordCount:
				wordCount[words]=wordCount[words]+1
			else:
				if(words in stopWords):
					continue
				else:
					wordCount[words]=1

	print(wordCount[searchKeyword])


	#Find top results for 1 keyword, 2 keywords, 3 keywords and 4 keywords 
	countoneWord=0
	counttwoWord=0
	countthreeWord=0
	countfourWord=0		
	for key, value in sorted(wordCount.items(), key=lambda x: (-x[1], x[0])):
		if len(key.split(' '))==4:
			if countfourWord<topResults:
				print "%s: %s" % (key, value)
				savefile.write(key.replace(",", " ")+","+str(value)+",")
			countfourWord=countfourWord+1
		elif len(key.split(' '))==2:
			if counttwoWord<topResults:
				print "%s: %s" % (key, value)
				savefile.write(key.replace(",", " ")+","+str(value)+",")
			counttwoWord=counttwoWord+1
		elif len(key.split(' '))==3:
			if countthreeWord<topResults:
				print "%s: %s" % (key, value)
				savefile.write(key.replace(",", " ")+","+str(value)+",")
			countthreeWord=countthreeWord+1
		else:
			if countoneWord<topResults:
				print "%s: %s" % (key, value)
				savefile.write(key.replace(",", " ")+","+str(value)+",")
			countoneWord=countoneWord+1


	#check for search keywords in header
	headers=""
	soup = BeautifulSoup(html, 'html.parser')
	for h1 in soup.findAll('h1'):
		headers=headers+" "+h1.text.encode("utf-8")+" "
	for h2 in soup.findAll('h2'):
		headers=headers+" "+h2.text.encode("utf-8")+" "
	for h3 in soup.findAll('h3'):
		headers=headers+" "+h3.text.encode("utf-8")+" "		
		
	countKeyNum=headers.split(" ")
	i=0
	for n in countKeyNum:
		if n.lower().strip()==searchKeyword.lower().strip():
			i=i+1
	# save number of times keywords appeared in the headwords
	savefile.write(str(i)+" ")
	
	
	
	
	
	
		
