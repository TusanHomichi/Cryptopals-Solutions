from matasano import *

class SRP_Server:
	def __init__(self):
		self.N = 2**256-2**224+2**192+2**96-1 	#Arbitrary, from NIST curve
		self.g = 2
		self.k = 3
		self.salts = {}
		self.hashes = {}
		self.OnRecv = self.Init_SRP
	
	def Register(self, username, password):
		salt = randbytes(16)
		x = bytes2int(hash(salt+password,sha256))
		v = pow(self.g,x,self.N)
		self.salts[username] = salt
		self.hashes[username] = v

	def Init_SRP(self,msg):
		username = msg[0]
		A = msg[1]
		b = randint(0,self.N-1)
		B = (self.k*self.hashes[username]+pow(self.g,b,self.N))%self.N
		u = bytes2int(hash(int2bytes(A)+int2bytes(B),sha256))
		S = int2bytes(pow(A*pow(self.hashes[username],u,self.N),b,self.N))
		self.K = hash(S,sha256)
		self.Send((self.salts[username],B))
		self.OnRecv = self.Check_SRP

	def Check_SRP(self,msg):
		self.Send(hmac(self.K,self.salts[msg[0]],sha256) == msg[1])
		self.OnRecv = self.Init_SRP
		
	def Send(self,msg):
		self.conn.Send(msg,self)
		
class SRP_Client_Bad:
	def __init__(self):
		self.N = 2**256-2**224+2**192+2**96-1 	#Arbitrary, from NIST curve
		self.g = 2
		self.k = 3
		self.salts = {}
		self.hashes = {}
	
	def Login(self, username, password):
		self.username = username
		self.password = password
		self.Send((self.username,0))
		self.OnRecv = self.GenerateHmac
		
	def GenerateHmac(self, msg):
		salt = msg[0]
		S = int2bytes(0)
		K = hash(S,sha256)
		h = hmac(K,salt,sha256)
		self.Send((self.username,h))
		self.OnRecv = self.PrintMsg
		
	def PrintMsg(self,msg):
		print("Logged in: %r" % msg)
		
	def Send(self,msg):
		self.conn.Send(msg,self)
		
		
C = SRP_Client_Bad()
S = SRP_Server()
conn = Connection(C,S)

S.Register(b'user',b'pass')

print("Good login")
C.Login(b'user', b'pass')
while not conn.Done():
	conn.Update()
	
print()
print("Bad login")
C.Login(b'user', b'passw')
while not conn.Done():
	conn.Update()