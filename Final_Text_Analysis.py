# -*- coding: utf-8 -*-
"""BlackCoffer Assignment text analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QhQjQWb4JPQb2zOQZyaZvergKiUWFEr0
"""

import pandas as pd
from nltk.tokenize import RegexpTokenizer , sent_tokenize
#from urllib.request import urlopen
from bs4 import BeautifulSoup
#from fake_useragent import UserAgent
import requests
import nltk
nltk.download('punkt')
#import urllib.request,sys,time ,requests

df = pd.read_excel('/content/Input.xlsx')
df.head()

a = df['URL'][10]
#b = a[a.index('.com')]
b = a[a.index('.com') + 5 : -1 ]
#a
b

#Extracting required text to List
df = pd.read_excel("/content/Input.xlsx")

def article_names(url):
  all_titles = []
  for i in range(len(url)):
    k = url[i]
    cleaned_title = k[k.index('.com/') + 5 :-1].replace('-',' ')
    all_titles.append(cleaned_title)

  return all_titles

url = df["URL"]
url_title = article_names(url)
url_title[1:10]

url[1]

url = 'https://insights.blackcoffer.com/how-does-metaverse-work-in-the-financial-sector/'
web = requests.get(url, headers= {'User-Agent':'XY'})
BS = BeautifulSoup(web.text)
#To get title from url
article_title = BS.find("h1", attrs={'class':'entry-title'}).get_text()
article_text = BS.find("div",attrs={'class':'td-post-content'}).get_text()
article_text

#Extracting each line and removing whitespaces(lead and trail)
lines = (line.strip() for line in article_text.splitlines())

#Breaking into text pieces
text_pieces = (phrase.strip() for line in lines for phrase in line.split("  "))

#Getting article text again with blank lines removed 
article_text = '\n'.join(piece for piece in text_pieces if piece)
article_text

#opening positive words file and converting to lowercase
pos = open('positive-words.txt','r')
posiwords = pos.read().lower()
posiwords

#converting positive words to a list
posilist = posiwords.split()
posilist[1:10]

#Merging all stopwords file into one file

sp1 = open('StopWords_Auditor.txt','r',encoding="ISO-8859-1")
sp2 = open('StopWords_Currencies.txt','r',encoding="ISO-8859-1")
sp3 = open('StopWords_DatesandNumbers.txt','r',encoding="ISO-8859-1")
sp4 = open('StopWords_Generic.txt','r',encoding="ISO-8859-1")
sp5 = open('StopWords_GenericLong.txt','r',encoding="ISO-8859-1")
sp6 = open('StopWords_Geographic.txt','r',encoding="ISO-8859-1")
sp7 = open('StopWords_Names.txt','r',encoding="ISO-8859-1")

sw1 = sp1.read()
sw2 = sp2.read()
sw3 = sp3.read()
sw4 = sp4.read()
sw5 = sp5.read()
sw6 = sp6.read()
sw7 = sp7.read()

SW = open('All_stopwords.txt','w')
stopwords = SW.write(sw1+sw2+sw3+sw4+sw5+sw6+sw7)
stopwords

#Loading positive words file and converting to lowercase
pos = open('positive-words.txt','r')
posiwords = pos.read().lower()
posilist = posiwords.split('\n')


#opening negative words file and converting to lowercase
neg = open('negative-words.txt','r',encoding="ISO-8859-1")
negatiwords = neg.read().lower()
negatilist = negatiwords.split('\n')


#opening all stopwords file and converting to lowercase
stop = open('All_stopwords.txt','r')
all_stop = stop.read().lower()
stoplist = all_stop.split('\n')

print(posilist[1:5] ,'\n', negatilist[1:5],'\n',stoplist[1:5])

#tokenizeing module ,removing punctuations
def tokening(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    words_before_cleaning = tokenizer.tokenize(text)
    #to get a list of those words from the text which are not in All_stopwords.txt file
    words_after_cleaning = list(filter(lambda token: token not in stoplist, words_before_cleaning))
    return words_after_cleaning

posilist[3]

"""#Extracting Derived Variables

Positive score
"""

def positive_score (text):
  posiword_count=0
  phrase = tokening(text)
  for word in phrase:
    if word in posilist:
       posiword_count +=1
      
    #retpos = posword
  return posiword_count

"""Negative score"""

def negative_score (text):
  negatiword_count=0
  phrase = tokening(text)
  for word in phrase :
    if word in negatilist :
       negatiword_count +=1

    #retneg = negword 
  return negatiword_count

"""Polarity score"""

def polarity_score (text) :
  pos = positive_score(text)
  neg = negative_score(text)
  polarity = (pos - neg) / ((pos + neg) + 0.000001)
  return round(polarity,2)

"""Subjectivity score"""

def subjectivity_score(text):
  


  ab1 = positive_score(text)
  ab2 = negative_score(text)
  ab3 = total_word_count(text)

  
  
  

  subjectivity_score =  (ab1 + ab2)/((ab3) + 0.0000001)
      
  return round(subjectivity_score,2)

"""#Analysis of Readability

Average Sentence Length
"""

def AverageSentenceLength (text):
  number_of_words = total_word_count(text)
  number_of_sentences = len (sent_tokenize(text))
  

  avg = number_of_words / number_of_sentences

  return round(avg,2)

a  = 'rafi is great. yeah i knoe. tell me something i dont know...'
len(sent_tokenize(a))

a= 'lets test here '
AverageSentenceLength(a)
#len(a.split())

"""Percentage of complex word"""

def percentage_complex_word(text):
    tokens = tokening(text)
    complexWord = 0
    complex_word_percentage = 0
    
    for word in tokens:
        vowels=0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    vowels += 1
            if(vowels > 2):
                complexWord += 1
    if len(tokens) != 0:
        complex_word_percentage = complexWord/len(tokens)
    
    return round(complex_word_percentage,2)

"""Fog Index"""

def fog_index(text):
  
    avg = AverageSentenceLength(text)
    complexes = percentage_complex_word(text)


    fogIndex = 0.4 * (avg + complexes)
    return round(fogIndex,2)

"""#Average number of words per sentence"""

def average_number_of_words_per_sentence(text):
  total_number_of_words = total_word_count(text)
  total_number_of_sentences = len(sent_tokenize(text))
  
  average_number_of_words_per_sentence = total_number_of_words/total_number_of_sentences
  return round(average_number_of_words_per_sentence,2)

"""#Complex word count"""

def complex_word_count(text):
    tokens = tokening(text)
    complexWord = 0
    
    for word in tokens:
        vowels=0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    vowels += 1
            if(vowels > 2):
                complexWord += 1
    return complexWord

"""#Word Count"""

def total_word_count(text):
    tokens = tokening(text)
    return len(tokens)

"""#Syllable Count Per Word"""

def sylabble_count_per_word(text):
    tokens = tokening(text)
    syllable = 0
    
    for word in tokens:
        vowels=0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    syllable +=1
    return syllable

sylabble_count_per_word('ae rafi ae')

"""#Personal Pronouns"""

def personal_pronouns(text):
  #token = tokening(text)
  texts = text.lower()
  tokenizer = RegexpTokenizer(r'\w+')
  tokens = tokenizer.tokenize(texts)



  count = 0
  for w in tokens:
    
    if (w=='US'):
      pass
    if (w =='i' or w=='we' or w =='ours' or w=='us'):
      count +=1
  return count

"""#Average Word Length"""

def avg_word_length(text):
  token = tokening(text)
  word_count = 0
  character_count = 0

  for word in token:
    word_count += 1
    for each_character in word:
      character_count += 1

  avg_word_length = character_count/word_count

  return round(avg_word_length,2)


trys = 'yes its called being sure'
#trys = trys.split(' ')
   
avg_word_length(trys)

"""#Smaller Text Analysis for faster output"""

URLS = df ["URL"]
URLS

corpus =[]
for url in URLS:

  page=requests.get(url , headers={"User-Agent": "XY"})
  #using beautiful soup for DATA CRAWLING  
  soup = BeautifulSoup(page.text , 'html.parser')
  #to get article title
  article_title = soup.find("h1",attrs = { 'class' : 'entry-title'}).get_text()

  #to get article text
  article_text = soup.find(attrs = { 'class' : 'td-post-content'}).get_text()
  #removing leading and trailing space from each line
  lines = (line.strip() for line in article_text.splitlines())

  #Breaking into text pieces
  text_pieces = (phrase.strip() for line in lines for phrase in line.split("  "))
  
  #Getting text egain with blank lines removed
  text = '\n'.join(piece for piece in text_pieces if piece)
  corpus.append(text)

corpus[1]

df2 = pd.DataFrame({'title':url_title,'corpus': corpus})

df2["POSITIVE SCORE"] = df2["corpus"].head() . apply (positive_score)
df2["NEGATIVE SCORE"] = df2["corpus"].head() . apply (negative_score)
df2["POLARITY SCORE"] = df2["corpus"].head() . apply (polarity_score)
df2["SUBJECTIVITY SCORE"] = df2["corpus"].head().apply(subjectivity_score)
df2["AVG SENTENCE LENGTH"] = df2["corpus"].head().apply (AverageSentenceLength)
df2["PERCENTAGE OF COMPLEX WORDS"] = df2["corpus"].head().apply (percentage_complex_word)
df2["FOG INDEX"] = df2["corpus"].head().apply(fog_index)
df2["AVG NUMBER OF WORDS PER SENTENCE"] = df2["corpus"].head(). apply (average_number_of_words_per_sentence)
df2["COMPLEX WORD COUNT"] = df2["corpus"].head(). apply (complex_word_count)
df2["WORD COUNT"] = df2["corpus"].head().apply (total_word_count)
df2["SYLLABLE PER WORD"] = df2["corpus"].head().apply (sylabble_count_per_word)
df2["PERSONAL PRONOUNS"] = df2["corpus"].head().apply (personal_pronouns)
df2["AVG WORD LENGTH"] = df2["corpus"].head().apply(avg_word_length)
df2

"""#Complete Text Analysis"""

#Using dataframe to apply functions
df1 = pd.DataFrame({'title':url_title,'corpus': corpus})
df1["URL_ID"] = df["URL_ID"]
df1["URL"] = df["URL"]
df1["POSITIVE SCORE"] = df1["corpus"].apply(positive_score)
df1["NEGATIVE SCORE"] = df1["corpus"].apply(negative_score)
df1["POLARITY SCORE"] = df1["corpus"].apply(polarity_score)
df1["SUBJECTIVITY SCORE"] = df1["corpus"].apply(subjectivity_score)
df1["AVG SENTENCE LENGTH"] = df1["corpus"].apply(AverageSentenceLength)
df1["PERCENTAGE OF COMPLEX WORDS"] = df1["corpus"].apply(percentage_complex_word)
df1["FOG INDEX"] = df1["corpus"].apply(fog_index)
df1["AVG NUMBER OF WORDS PER SENTENCE"] = df1["corpus"].apply(average_number_of_words_per_sentence)
df1["COMPLEX WORD COUNT"] = df1["corpus"].apply(complex_word_count)
df1["WORD COUNT"] = df1["corpus"].apply(total_word_count)
df1["SYLLABLE PER WORD"] = df1["corpus"].apply(sylabble_count_per_word)
df1["PERSONAL PRONOUNS"] = df1["corpus"].apply(personal_pronouns)
df1["AVG WORD LENGTH"] = df1["corpus"].apply(avg_word_length)
df1.head()

"""##Dropping columns to achieve desired output"""

Finally_done = df1.drop(['title','corpus'],axis = 1)
Finally_done.head()

"""#Exporting to an Excel File"""

Finally_done.to_excel('Filled Output Data Structure.xlsx', encoding='utf-8')





