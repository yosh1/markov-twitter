# -*- coding: utf-8 -*-
import random
import MeCab

#MeCabを使用してテキストデータを単語に分割する
def wakati(text):
	t = MeCab.Tagger("-Owakati")
	m = t.parse(text)
	result = m.rstrip(" \n").split(" ")
	return result

if __name__ == "__main__":
	filename = "introduction.txt"
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
	while count < 140:
		tmp = random.choice(markov[(w1, w2)])
		sentence += tmp
		w1, w2 = w2, tmp
		count += len(tmp)
		if count > 140:
			sentence = sentence[:-len(tmp)]
	while count2 < 140:
		if sentence[-1:] != "。":
			sentence = sentence[:-1]
			count2 += 1
		else:
			break
	print("この文章は" + str(len(sentence)) + "文字です")
	print(sentence)