from matasano import *

plains = []
ciph = hex2bytes("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
for k in range(256):
	plain = rep_xor(ciph,[k])
	plains.append((ks_score(unigram(plain),uni_freq), plain))
	
plains = sorted(plains)
for i in range(10):
	print(plains[i][1][:20])