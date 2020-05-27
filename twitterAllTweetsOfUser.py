
import tweepy
import json
import csv
# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = 'v3l3OYpM4sd7MgiYL4GrX2eHf'
credentials['CONSUMER_SECRET'] = '8Mfydb6NbauCXoz72vRPwJWBxaeKu3K3w2YwUezqaUIj2Wh9e7'
credentials['ACCESS_TOKEN'] = '1034663748286533632-pDZr9bs94fdlgYW8gMxtdbzqCakFg3'
credentials['ACCESS_SECRET'] = 'XXiYXIl1fxJPuoR8QDPMN257D8RbaRJwpWBsEaVGyxx9h'

auth = tweepy.OAuthHandler(credentials.get('CONSUMER_KEY'), credentials.get('CONSUMER_SECRET'))
auth.set_access_token(credentials.get('ACCESS_TOKEN'), credentials.get('ACCESS_SECRET'))

def get_all_tweets(screen_name):
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        print(f"...{len(alltweets)} tweets downloaded so far")
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    #write the csv  
    with open('new_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("greeneyedabyss")

