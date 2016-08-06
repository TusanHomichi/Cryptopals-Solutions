from matasano import *

file = open("c4.txt", 'r')
plains = []
for line in file:
	line = hex2bytes(line[:-1])
	for k in range(256):
		plain = rep_xor(line,[k])
		plains.append((chi2score(unigram(plain),uni_freq), plain))
	
plains = sorted(plains)
for i in range(10):
	print(plains[i][1][:20])