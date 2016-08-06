from matasano import *

class SRP_Client:
	def __init__(self):
		self.N = 2**256-2**224+2**192+2**96-1 	#Arbitrary, from NIST curve
		self.g = 2

	def Login(self, username, password):
		self.username = username
		self.password = password
		self.a = randint(0,self.N-1)
		self.A = pow(self.g,self.a,self.N)
		self.Send((self.username,self.A))
		self.OnRecv = self.GenerateHmac
		
	def GenerateHmac(self, msg):
		salt = msg[0]
		B = msg[1]
		u = bytes2int(hash(int2bytes(self.A)+int2bytes(B),sha256))
		x = bytes2int(hash(salt+self.password,sha256))
		S = int2bytes(pow(B,self.a+u*x,self.N))
		K = hash(S,sha256)
		h = hmac(K,salt,sha256)
		self.Send((self.username,h))
		self.OnRecv = self.PrintMsg
		
	def PrintMsg(self,msg):
		print("Logged in: %r" % msg)
		
	def Send(self,msg):
		self.conn.Send(msg,self)
		
class MITM_Server:
	def __init__(self):
		self.N = 2**256-2**224+2**192+2**96-1 	#Arbitrary, from NIST curve
		self.g = 2
		self.msg_count = 0
	
	def OnRecv(self, msg):
		if self.msg_count == 0:
			self.I = msg[0]
			self.A = msg[1]
			self.Send((b'',self.g))
			self.u = bytes2int(hash(int2bytes(self.A)+int2bytes(self.g),sha256))
		elif self.msg_count == 1:
			self.hash = msg[1]
			
		self.msg_count += 1
			
	def OfflineCheck(self, p):
		v = pow(self.g, bytes2int(hash(p,sha256)), self.N)
		test = hmac(hash(int2bytes((self.A*pow(v,self.u,self.N))%self.N),sha256),b'',sha256)
		return test==self.hash
		
	def Send(self,msg):
		self.conn.Send(msg,self)
		
C = SRP_Client()
S = MITM_Server()
conn = Connection(C,S)

C.Login(b'user', b'pass')
while not conn.Done():
	conn.Update()
	
