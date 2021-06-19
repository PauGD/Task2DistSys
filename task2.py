import lithops
import tweepy
from textblob import TextBlob
import csv
import pandas as pd
from lithops import Storage
from lithops.multiprocessing import Process

def tweetmachine(name):
    
    columns={'id':[],'text':[],'user':[],'retweets':[],'date':[],'hastags':[],'sentiment':[] }
    sent=''
    auth = tweepy.OAuthHandler('XXXXXX','XXXXXXXX')
   
    api = tweepy.API(auth)
    resultats=[]
    querry= name + (' -filter:retweets')
    for res in tweepy.Cursor(api.search,q= querry, count=100,tweet_mode='extended', lang='en').pages(10):
        resultats.append(res)
    resz=[]
    i=0
    
    filename= name + '.csv'
    f=open(filename, 'w')

    df=pd.DataFrame(columns)
    
    for results in resultats:
        for tweet in results:
            if(tweet.retweeted==False):
                text = tweet.full_text
                data=TextBlob(text)
                num=data.sentiment.polarity
                if( num >0):
                    sent='Positive'
                else: 
                    if(  num < 0):
                        sent='Negative'
                    else:
                        sent='Neutral'

                hasht=''
                hashtags=tweet.entities.get('hashtags')
                for j in range(0, len(hashtags)):
                       
                    hasht=hasht+','+(hashtags[j]['text'])
                        
                df.loc[len(df.index)]=[tweet.id, text, tweet.user.name, tweet.retweet_count, tweet.created_at,hasht,sent]
            resz.append(tweet)
            i=i+1

        

    f2= df.to_csv()
    storage=Storage()
    keys=storage.list_keys('tweetbucket0135711')
    if filename in keys:
        backupfile=storage.get_object('tweetbucket0135711' , filename) 
        tempfilename='old-'+name+'-01.csv'
        storage.put_object('tweetbucket0135711', tempfilename,  backupfile )
    
    storage.put_object('tweetbucket0135711', filename, f2 )
    storage.put_object('tweetbucket0135711', '01-'+filename, f2 )
    storage.put_object('tweetbucket0135711', '02-'+filename, f2 )
    
    return 0


if __name__ == '__main__':
    fexec = lithops.ServerlessExecutor(runtime='tweepysd/task2runtime001')
    fexec.map(tweetmachine, ['moderna', 'astrazeneca', 'pfizer', 'sputnik', 'coronavac'  ])
    fexec.wait()
    print(fexec.get_result())
    #fexec.plot(dst='/home/milax/proves') 