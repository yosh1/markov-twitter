# -*- coding: utf-8 -*-
import random
import MeCab
import json
import setup
from requests_oauthlib import OAuth1Session

CK = 'wKzcIqCiE5b3PaMNgmT79HPWG'
CS = 'PWZJUlbyAWB7nOH3kmBSWhsZcxbD2KFnrEnQr2wvglyJr2nLT4'
AT = '2453905224-QVSlWWykfC3u47aahfO9pemOdwpBxbLuwmRBy4W'
ATS = 'zg1v7BWjoPo3cGIoTqHjl3jcVadQhXnGWfyqN54gRG5gR'
twitter = OAuth1Session(CK, CS, AT, ATS)


def wakati(text):
	tag = MeCab.Tagger("-Owakati")
	m = tag.parse(text)
	result = m.rstrip(" \n").split(" ")
	return result


def mar(name):
	src = setup.fetch_twit(name)

	wordlist = wakati(src)
	markov = {}
	w1 = ""
	w2 = ""
	for word in wordlist:
		if w1 and w2:
			if (w1, w2) not in markov:
				markov[(w1, w2)] = []
			markov[(w1, w2)].append(word)
		w1, w2 = w2, word
	markov.update({(wordlist[-2], wordlist[-1]): [wordlist[0]],(wordlist[-1], wordlist[0]): [wordlist[1]]})

	count = 0
	count2 = 0
	sentence = ""
	w1, w2 = random.choice(list(markov.keys()))
	while count < 100:
		tmp = random.choice(markov[(w1, w2)])
		sentence += tmp
		w1, w2 = w2, tmp
		count += len(tmp)
		if count > 100:
			sentence = sentence[:-len(tmp)]
#while count2 < 140:
        #if sentence[-1:] != "。":
        #	sentence = sentence[:-1]
        #	count2 += 1
        #else:
        #	break

	if not len(sentence):
		mar(name)
	return sentence + " . . ."
#, len(sentence)
