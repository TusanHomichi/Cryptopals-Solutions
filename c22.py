from matasano import *
from time import time, sleep

sleep(randint(40,1000))
seed = int(time())
r = mt19937(seed)
sleep(randint(40,1000))
output = r.rand()

cur = int(time())
for i in range(cur-2001,cur-39):
	test_r = mt19937(i)
	if test_r.rand() == output:
		print("Seed: %d" % i)
		
print("Actual seed: %d" % seed)