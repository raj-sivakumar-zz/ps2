import tweepy
import csv
import requests
import json
from govtrack.api import GovTrackClient
import urllib
import numpy as np



#insert own consumer_key and secret and access key and secret to start
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    tweet_list = []

    #make initial request for 100 most recent tweets
    recent_tweets = api.user_timeline(screen_name = screen_name,count=100)

    #save most recent tweets
    tweet_list.extend(recent_tweets)

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.text.encode("utf-8"),
                    tweet.retweet_count,
                    tweet.favorite_count,
                    tweet.created_at.isoformat(),
                    tweet.place if tweet.place else None]
                    for tweet in tweet_list]

    #write the csv
    with open('pelosi-Sivakumar.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["text", "tweet count", "likes", "date", "location"])
        writer.writerows(outtweets)

    pass

# include your own propublica access key at end of response request.get()
def get_bills():

    data_bills = requests.get('https://www.govtrack.us/api/v2/bill?q=cybersecurity').json()
    bills = data_bills['objects']
    roles =[]
    for i, bill in enumerate(bills):
        person_id = str(bills[i]['sponsor_role']['id'])
        role_entry = requests.get('https://www.govtrack.us/api/v2/role?id=' + person_id).json()

        add_role = str(role_entry['objects'][0]['party'])
        roles.append(add_role)

    data_out = [[bills[i]['title'],
                bills[i]['id'],
                bills[i]['sponsor']['lastname'],
                0] for i, bill in enumerate(bills)]
    for i, entry in enumerate(roles):
        data_out[i][3] = roles[i]


    with open('cybersecurity-Sivakumar.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "bill_id", "lastname", "party"])
        for i in range(0,20):
            writer.writerow(data_out[i][:])

    pass


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("NancyPelosi")
    get_bills()
