from matasano import *
from time import time,sleep
import hashlib

def insec_comp(a,b):
	for i in range(len(a)):
		if a[i] != b[i]:
			return False
		sleep(0.005)
	return True

key = bytes([randint(97,122) for i in range(16)])
def check(file,mac):
	return insec_comp(hmac(key,file,sha1),mac)
	
def leak(file):
	print(bytes2hex(hmac(key,file,sha1)))
	mac = b'\x00'*sha1.hash_size
	for i in range(sha1.hash_size):
		times = []
		for j in range(256):
			tot = 0
			rounds = 50
			mac = mac[:i] + bytes([j]) + mac[i+1:]
			for k in range(rounds):
				t1 = time()
				check(file,mac)
				t2 = time()
				tot += t2-t1
			times.append((tot,j))
		times = sorted(times, reverse=True)
		mac = mac[:i] + bytes([times[0][1]]) + mac[i+1:]
		print(i,hex(mac[i]))
	return mac
	
check(b"file",leak(b"file"))