

#----------------------------------
# Libraries to be import 
#----------------------------------
import matplotlib.pyplot as plt
import utils   # some convenient functions
get_ipython().magic('load_ext autoreload')
get_ipython().magic('autoreload 2')
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup 

#----------------------------------
# Google news API key for extracting dataset
#----------------------------------
API_KEY = '23d4b73d63aa478699da4b9ee7443e4b'

#----------------------------------
# Global Messages | Start
#----------------------------------
ScrapStart = "Fetching has been Initiated"
ScrapCompelete = "Fetching data is completed"


#------------------------------------------------------
# Creating an empty dataframe for storing the news data
#-------------------------------------------------------
dataset = pd.DataFrame({'region':[],'source':[],'url':[],'author':[],
                        'title':[],'desc':[],'publishedAt':[]})

#-----------------------------------------------------------------
# Reading who_data file into pd for getting the region list
#------------------------------------------------------------------
def read_who_data(csv_file):
    who_data = pd.read_csv(csv_file)
    regions = who_data['Region'].to_list()
    return regions


#-----------------------------------------------------------------
# Get list of regions
#------------------------------------------------------------------
list_of_regions = read_who_data("who_data.csv")
print("--------------------------------------------------------------------------------------------------")
print(list_of_regions)
print("--------------------------------------------------------------------------------------------------")
print("The regions included by WHO are:{} ".format(len(list_of_regions)))
print("--------------------------------------------------------------------------------------------------")

##-------------------------------------------------------------------------------##
# SCRAP DATA FROM GOOGLE NEWS USING GOOGLE API
##------------------------------------------------------------------------------##
'''Fetch dataset from google news using google api
    
    Arguments -> news source, dataframe & list of regions
    Returns ->  a csv file with news data and a message of completion
    -------------------------------------------------------------------------------
    '''
def scrap_data(source,dataframe,list_of_regions):
    sources = []
    urls = []
    authors = []
    titles = []
    descriptions = []
    publishing = []
    regions = []
    print(ScrapStart)
    for region in list_of_regions:
        url = ('http://newsapi.org/v2/everything?'
           'q'+region+'&'
           'q= COVID-19&'          # can use : "coronavirus"  also for fetching more data i.e 'q = coronavirus&'
           'sortBy=popularity&'
           'apiKey='+API_KEY)
        response = requests.get(url)
        news = response.json()
        #print(len(news['articles']))
        if response.status_code == 200:
            #print('Status Code = 200, Fetching data for {}'.format(region))
            for articles in news['articles']:
                sources.append(articles['source']['name'])
                urls.append(articles['url'])
                authors.append(articles['author'])
                titles.append(articles['title'])
                descriptions.append(articles['description'])
                publishing.append(articles['publishedAt'])
                regions.append(region)
        else:
            print('failure')   
    dataset['region'] = regions
    dataset['source'] = sources
    dataset['url'] = urls
    dataset['author'] = authors
    dataset['title'] = titles
    dataset['desc'] = descriptions
    dataset['publishedAt'] = publishing
    dataset.to_csv(source + ".csv",index = False)
    return ScrapComplete


#-----------------------------------------------------------------
# Get csv of news article using scrap_data()
#------------------------------------------------------------------
scrap_data('google_news1',dataset,list_of_regions)


news_data = pd.read_csv("google_news1.csv")

list_url = news_data['url'].to_list()

len(list_url)

article_text = []
count = 1
for i in list_url:
    r = requests.get(i).text
    soup = BeautifulSoup(r)
    pre = ""
    print(count)
    for j in soup.findAll('p'):
        #print(j.text)
        pre = pre + j.text
    count = count+1
    article_text.append(pre)


merge_data = pd.DataFrame({'region':news_data['region'],'source':news_data['source'],'url':news_data['url'],
                           'author':news_data['author'],'title':news_data['title'],'desc':article_text,
                           'publishedAt':news_data['publishedAt']})


merge_data.to_csv("news.csv", index = False)

