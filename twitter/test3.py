# -*- coding: utf-8 -*-
import random
import MeCab
from twitter import Twitter, OAuth
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context


t = Twitter(auth=OAuth(
        #下記各種キーは@shostako_Vc(インターン生奥野の個人アカウント)にて取得
        #CONSUMER_KEY
        consumer_key='wKzcIqCiE5b3PaMNgmT79HPWG',
        #CONSUMER_SECRET
        consumer_secret='PWZJUlbyAWB7nOH3kmBSWhsZcxbD2KFnrEnQr2wvglyJr2nLT4',
        #ACCESS_TOKEN
        token='2453905224-QVSlWWykfC3u47aahfO9pemOdwpBxbLuwmRBy4W',
        #ACCESS_TOKEN_SECRET
        token_secret='zg1v7BWjoPo3cGIoTqHjl3jcVadQhXnGWfyqN54gRG5gR'
    ))

remain = True #ループ判定
userTweets = [] #tweetの格納先
max_id = 997324427330121728
remainNum = 0
numberOfTweets = 300 #取ってくるtweetの数
count = 100 #一度のアクセスで何件取ってくるか
while remain:
    aTimeLine = t.statuses.user_timeline(user_id = 2799769662, count=count, max_id=max_id)
    for tweet in aTimeLine:
    	userTweets.append(tweet['text'])
    max_id = aTimeLine[-1]['id']-1
    remainNum = numberOfTweets - len(userTweets)
    count = remainNum
    if len(userTweets)+1 > numberOfTweets:
        print('finish search')
        remain = False

#userTweetsをlistからstrに変換
strTweets = ' '.join(userTweets)
#リプライ宛先とURLを排除
replypattern = '@[\w]+'
urlpattern = 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
processedTweets = re.sub(replypattern, ' ', strTweets)
processedTweets = re.sub(urlpattern, ' ', processedTweets)
#processedTweet.txtに前処理したツイートのテキストを記述
file = open('processedTweets.txt', 'w')
file.write(processedTweets)
#後でsrc = open(filename, "r").read()でread専用として開くためにclose
file.close()


#MeCabを使用してテキストデータを単語に分割する
def wakati(text):
	tag = MeCab.Tagger("-Owakati")
	m = tag.parse(text)
	result = m.rstrip(" \n").split(" ")
	return result

if __name__ == "__main__":
	filename = "processedTweets.txt"
	src = open(filename, "r").read()

	wordlist = wakati(src)
	#マルコフ連鎖用のテーブルを作成する
	markov = {}
	#markovを初期化された辞書と定義
	w1 = ""
	w2 = ""
	#w1,w2を空の文字列と定義
	for word in wordlist:
		#wordlistからひとつずつ要素を取り出しwordに代入して以下の処理を実行
		if w1 and w2:
			#w1とw2の両方がtrueの場合以下の処理を実行
			if (w1, w2) not in markov:
				#(w1, w2)というタプルが辞書markovのキーに無い場合以下の処理を実行
				markov[(w1, w2)] = []
				#(w1, w2)というタプルがキーのバリューに[]という空のリストを代入
				#print('w1 not in markov', w1, word)
				#print('w2 not in markov', w2, word)
				#print('not in markov', markov)
			markov[(w1, w2)].append(word)
			#(w1, w2)というタプルが辞書markovのキーにあった場合辞書markovの(w1, w2)キーのバリューにwordを追加
			#print('w1 append:', w1, word)
			#print('w2 append:', w2, word)
			#print('append', markov)
		w1, w2 = w2, word
		#w1とw2の少なくともどちらかがfalseの場合w1にw2を、w2にwordを代入
		#print('w1:', w1, word)
		#print('w2:', w2, word)
		#print('markov', markov)

	#エラー防止のため入力文章の形態素のうち最初の２つをmarkovに追加
	markov.update({(wordlist[-2], wordlist[-1]): [wordlist[0]],(wordlist[-1], wordlist[0]): [wordlist[1]]})

	#文章の自動作成
	count = 0
	count2 = 0
	sentence = ""
	w1, w2 = random.choice(list(markov.keys()))
	#140文字以下にするためcount < 140
	while count < 140:
		tmp = random.choice(markov[(w1, w2)])
		sentence += tmp
		w1, w2 = w2, tmp
		#sentenceに足す単語の文字数をcountに足すことで文字数を140字以内に制限
		count += len(tmp)
		#sentenceが140字を超えてしまったら最後に足した単語を削除
		if count > 140:
			sentence = sentence[:-len(tmp)]
	#sentenceの最後の文字が"。"になるまで後ろから文字を削除
	while count2 < 140:
		if sentence[-1:] != "。":
			sentence = sentence[:-1]
			count2 += 1
		else:
			break
	print(str(len(sentence)) + "文字")
	print(sentence)