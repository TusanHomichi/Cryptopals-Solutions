from matasano import *

class DH_Client:
	def __init__(self):
		self.OnRecv = self.Ack
		
	def Ack(self,msg):
		self.p = msg[0]
		self.g = msg[1]
		self.Send(True)
		self.OnRecv = self.MakeKey

	def MakeKey(self,msg):
		priv = randint(0,self.p-1)
		pub = pow(self.g,priv,self.p)
		self.key = hash(int2bytes(pow(msg,priv,self.p)),sha1)[:16]
		self.Send(pub)
		self.OnRecv = self.Echo

	def Echo(self,msg):
		plain = pkcs7_unpad(aes_cbc_dec(msg[0],self.key,msg[1]))
		iv = randbytes(16)
		self.Send((aes_cbc_enc(pkcs7_pad(plain),self.key,iv),iv))

	def Send(self,msg):
		self.conn.Send(msg,self)

class DH_Server:
	def __init__(self):
		pass

	def Start(self,p=37,g=5):
		self.p = p
		self.g = g
		self.Send((self.p,self.g))
		self.OnRecv = self.SeeAck

	def SeeAck(self,msg):
		if msg:
			self.priv = randint(0,self.p-1)
			pub = pow(self.g,self.priv,self.p)
			self.Send(pub)
			self.OnRecv = self.FinishKey

	def FinishKey(self,msg):
		self.key = hash(int2bytes(pow(msg,self.priv,self.p)),sha1)[:16]
		del(self.priv)
		iv = randbytes(16)
		self.Send((aes_cbc_enc(pkcs7_pad(b"Hello!"),self.key,iv),iv))
		self.OnRecv = self.CheckEcho

	def CheckEcho(self,msg):
		plain = pkcs7_unpad(aes_cbc_dec(msg[0],self.key,msg[1]))
		if plain != b"Hello!":
			raise Exception("DH failed")

	def Send(self,msg):
		self.conn.Send(msg,self)

class MITM:
	def __init__(self):
		self.msg_count = 0
		
	def OnRecv(self,msg):
		if self.msg_count == 0:
			self.conn2.Send((msg[0],1),self)
			self.key = hash(int2bytes(1),sha1)[:16]
		elif self.msg_count%2 == 0:
			self.conn2.Send(msg,self)
		else:
			self.conn1.Send(msg,self)
		
		if self.msg_count >= 4:
			print("MITM: %r" % pkcs7_unpad(aes_cbc_dec(msg[0],self.key,msg[1])))
		
		self.msg_count += 1
	

print("Regular DH")
A = DH_Server()
B = DH_Client()
conn = Connection(A,B)

A.Start()

while not conn.Done():
	conn.Update()
	
	
print()
print("MITM Connection") #Makes g=1, cases g=p and g=p-1 are similar
A = DH_Server()
B = DH_Client()
M = MITM()

c1 = Connection(A,M)
M.conn1 = c1

c2 = Connection(M,B)
M.conn2 = c2

A.Start()

while not c1.Done() or not c2.Done():
	c1.Update()
	c2.Update()