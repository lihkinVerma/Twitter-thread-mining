
import tweepy
import json
# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = ''
credentials['CONSUMER_SECRET'] = ''
credentials['ACCESS_TOKEN'] = ''
credentials['ACCESS_SECRET'] = ''

auth = tweepy.OAuthHandler(credentials.get('CONSUMER_KEY'), credentials.get('CONSUMER_SECRET'))
auth.set_access_token(credentials.get('ACCESS_TOKEN'), credentials.get('ACCESS_SECRET'))

api = tweepy.API(auth)

def get_all_tweets(tweet):
    screen_name = tweet.user.screen_name
    lastTweetId = tweet.id
    #initialize a list to hold all the tweepy Tweets
    allTweets = []
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    allTweets.extend(new_tweets)
    #save the id of the oldest tweet less one
    oldest = allTweets[-1].id - 1
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0 and oldest >= lastTweetId:
        print(f"getting tweets before {oldest}")
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        #save most recent tweets
        allTweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest =allTweets[-1].id - 1
        print(f"...{len(allTweets)} tweets downloaded so far")
    outtweets = [tweet.id for tweet in allTweets]
    return outtweets

def getAllTweetsInThreadAfterThis(tweetId):
    thread = []
    hasReply = True
    res = api.get_status(tweetId, tweet_mode='extended')
    allTillThread = get_all_tweets(res)
    thread.append(res)
    if allTillThread[-1] > res.id:
        print("Not able to retrieve so older tweets")
        return thread
    print("downloaded required tweets")
    startIndex = allTillThread.index(res.id)
    print("Finding useful tweets")
    quietLong = 0
    while startIndex!=0 and quietLong<25:
        nowIndex = startIndex-1
        nowTweet = api.get_status(allTillThread[nowIndex], tweet_mode='extended')
        if nowTweet.in_reply_to_status_id == thread[-1].id:
            quietLong = 0
            #print("Reached a useful tweet to be included in thread")
            thread.append(nowTweet)
        else:
            quietLong = quietLong + 1
        startIndex = nowIndex
    return thread

def getAllTweetsInThreadBeforeThis(tweetId):
    thread = []
    hasReply = True
    res = api.get_status(tweetId, tweet_mode='extended')
    while res.in_reply_to_status_id is not None:
        res = api.get_status(res.in_reply_to_status_id, tweet_mode='extended')
        thread.append(res)
    return thread[::-1]

def getAllTweetsInThread(tweetId):
    tweetsAll = []
    print("Getting all tweets before this tweet")
    tweetsAll = getAllTweetsInThreadBeforeThis(tweetId)
    print(len(tweetsAll))
    print("Getting all tweets after this tweet")
    tweetsAll.extend(getAllTweetsInThreadAfterThis(tweetId))
    return tweetsAll

def printAllTweet(tweets):
    if len(tweets)>0:
        print("Thread Messages include:-")
        for tweetId in range(len(tweets)):
            print(str(tweetId+1)+". "+tweets[tweetId].full_text)
            print("")
    else:
        print("No Tweet to print")

if __name__ == '__main__':
    myTweetId = '1260975880588996610'
    
    madhubalaTweetId = '1256174506374291457'
    middleMadhubalaTweetId = '1256177855924441089'
    lastMadhubalaTweetId = '1256178904244641794'

    keralaHighBenchTweetId = '1255758616260341760'
    lastKeralaBenchTweetId = '1255791362537971712'

    allTweets = getAllTweetsInThread(middleMadhubalaTweetId)
    printAllTweet(allTweets)
