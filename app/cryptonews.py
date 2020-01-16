from crypto_news_api import CryptoControlAPI

#create a function for getting the top news articles for a specific coin
def get_top_News(x):
    
    api = CryptoControlAPI("46af633bdcb9d4ad4772ded65505727c") #get the API key from the CryptoCompare website
    top_news_raw = api.getTopNewsByCoin(x)
    for i in range(0,3):
        print(top_news_raw[i]['title'])
    
#call the function for articles of bitcoin
get_top_News('bitcoin')