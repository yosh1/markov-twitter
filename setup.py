# -*- coding: utf-8 -*-
import random
import MeCab
import json
import os
import re
import datetime
from requests_oauthlib import OAuth1Session
import pprint


def fetch_twit(keyw):
    if os.path.isfile(os.path.join(os.getcwd()+"/twit_{}_{}".format(keyw, datetime.date.today()))):
        with open("twit_{}_{}".format(keyw, datetime.date.today()), "r") as file:
            dat = file.read()
        return dat
    sent = ""
    name = 'from:@{} -"RT" -"いいねされた数:"'.format(keyw)
    replypattern = re.compile('@[\w]+')
    urlpattern = re.compile('https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')

    CK = 'wKzcIqCiE5b3PaMNgmT79HPWG'
    CS = 'PWZJUlbyAWB7nOH3kmBSWhsZcxbD2KFnrEnQr2wvglyJr2nLT4'
    AT = '2453905224-QVSlWWykfC3u47aahfO9pemOdwpBxbLuwmRBy4W'
    ATS = 'zg1v7BWjoPo3cGIoTqHjl3jcVadQhXnGWfyqN54gRG5gR'
    twitter = OAuth1Session(CK, CS, AT, ATS)


    url = "https://api.twitter.com/1.1/search/tweets.json"

    params = {'q': name, 'count': 200}

    req = twitter.get(url, params=params)

    if req.status_code == 200:
        search_timeline = json.loads(req.text)
        for tweet in search_timeline['statuses']:
            twit = tweet['text'].strip().replace("\n", "")
            i = re.sub(replypattern, '', twit)
            i = re.sub(urlpattern, '', i)

            sent += i + "\n"
            max_id = tweet["id"]
    else:
        print("ERROR: %d" % req.status_code)

    for i in range(10):
        params = {'q': name, 'count': 200, max_id: max_id}

        req = twitter.get(url, params = params)

        if req.status_code == 200:
            search_timeline = json.loads(req.text)
            for tweet in search_timeline['statuses']:
                twit = tweet['text'].strip().replace("\n", "")
                i = re.sub(replypattern, '', twit)
                i = re.sub(urlpattern, '', i)

                sent += i + "\n"
                max_id = tweet["id"]
        else:
            return 1
    with open("twit_{}_{}".format(keyw, datetime.date.today()), "w") as file:
        file.write(sent)
    return sent