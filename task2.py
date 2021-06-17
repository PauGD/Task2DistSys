import lithops
import tweepy
from sentiment_analysis_spanish import sentiment_analysis

import csv
from lithops import Storage
from lithops.multiprocessing import Process

def tweetmachine(name):
    auth = tweepy.OAuthHandler('XXXXXXXXXXXXX','XXXXXXXXXXXXXXXXXXx')
   
    api = tweepy.API(auth)
    resultats=[]
    querry= name + (' -filter:retweets')
    for res in tweepy.Cursor(api.search,q= querry, count=100,tweet_mode='extended', lang='es').pages(8):
        resultats.append(res)
    resz=[]
    i=0
    filename= name + '.csv'
    f=open(filename, 'w')
    with f as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for results in resultats:
            for tweet in results:
                if(tweet.retweeted==False):
                    text = tweet.full_text
                    hasht=''
                    hashtags=tweet.entities.get('hashtags')
                    for j in range(0, len(hashtags)):
                       
                        hasht=hasht+','+(hashtags[j]['text'])
                        
                    filewriter.writerow([tweet.id, text, tweet.user.name, tweet.retweet_count, tweet.created_at,hasht])
                resz.append(tweet)
                i=i+1

        

    f2= open(filename, 'rb')
    storage=Storage()
    keys=storage.list_keys('tweetbucket0135711')
    if filename in keys:
        backupfile=storage.get_object('tweetbucket0135711' , filename) 
        tempfilename=name+'-01.csv'
        storage.put_object('tweetbucket0135711', filename, f2 )

    storage.put_object('tweetbucket0135711', tempfilename,  backupfile )
    return resz[6]



if __name__ == '__main__':
    fexec = lithops.ServerlessExecutor(runtime='tweepysd/imatgefinal')
    fexec.map(tweetmachine, ['moderna', 'astrazeneca', 'pfizer' ])
    fexec.wait()
    print(fexec.get_result())
    fexec.plot(dst='/home/milax/proves') 
