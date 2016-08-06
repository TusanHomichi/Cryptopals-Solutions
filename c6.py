from matasano import *
from base64 import b64decode

file = open('c6.txt','r')
ciph = ""
for line in file:
	ciph += line[:-1]
file.close()
ciph = b64decode(ciph)

keys = []
for kl in range(2,40):
	score = hamming(ciph[:kl],ciph[kl:2*kl]) + hamming(ciph[2*kl:3*kl],ciph[3*kl:4*kl])
	keys.append((score/kl,kl))
keys = sorted(keys)

for _,kl in keys:
	blocks = []
	for i in range(kl):
		block = bytes([ciph[j] for j in range(i,len(ciph),kl)])
		cand = block
		for k in range(256):
			plain = rep_xor(block,[k])
			if chi2score(uni_freq,unigram(plain)) < chi2score(uni_freq,unigram(cand)):
				cand = plain
		blocks.append(cand)
	guess = []
	for i in range(len(ciph)):
		guess.append(blocks[i%kl][i//kl])
	print(kl,bytes(guess)[:50]) 
	input()