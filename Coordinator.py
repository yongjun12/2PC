import xmlrpclib
import random
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
from multiprocessing import Lock


class Coordinator:

	def __init__(self):
		self.replicas = []
		self.replica_add = []
		self.lock = threading.Lock()
		self.file = open("Coor.log", "a+")
		self.tran_id = 0
		self.isRecover = 0

	def recover(self):
		last_line = ""
		self.file = open("Coor.log", "r+")

		for line in self.file:
			last_line = line

		para = last_line.split(" ")
		
		if(str(para[-1]) == "Commit\n" or str(para[-1]) == "Abort\n"):
			print "Do not need to recover"
			return True
		# 	self.replica_add = para[1].split(",")
		# 	for add in self.replica_add:
		# 		self.replicas.append(xmlrpclib.ServerProxy(add))
		
		action = para[0]
		self.isRecover = 1

		if action == "put":
			print "recover put function" 
			self.co_put(para[1], para[2])
		elif action == "get":
			print "recover get function" 
			self.co_get(para[1])
		elif action == "del":
			print "recover del function" 
			self.co_del(para[1])

		self.isRecover = 0


	def co_put(self, key, value):
		print "executing co_put"

		self.lock.acquire()
		print "lock acquire success"

		self.file = open("Coor.log", "a+")

		print "isRecover" + str(self.isRecover)
		if not self.isRecover:
			self.file.write("put" + " " + key + " " + value)

		flag = ""

		print "running function on " 
		for item in self.replicas:
			print str(item) + " "
			try:
				flag = item.rep_put(key, value)
				print "flag: " + str(flag)
			except Exception, e:
				print e.args
			if(flag == False):
				self.co_abort()
				self.file.write(" " + "Abort\n")
				return false

		self.co_commit()
		self.file.write(" " + "Commit\n")
		self.file.close()
		self.lock.release()
		

	def co_get(self, key):
		print "co_get"
		self.file = open("Coor.log", "a+")
		self.file.write("get " + key)

		random_num = random.randrange(0, len(self.replicas), 1);
		value = self.replicas[random_num].rep_get(key)
		print "Get value %s" % value

		self.file.write(" Commit\n")
		self.co_commit()

	def co_del(self, key):
		print "co_del"
		self.file = open("Coor.log", "a+")
		self.file.write("del " + key)

		self.lock.acquire()
		for item in self.replicas:
			print item
			try:
				flag = item.rep_del(key)
				print "flag: " + str(flag)
			except Exception, e:
				print e.args
			if(flag == False):
				self.co_abort()
				self.file.write(" " + "Abort\n")
				return false

		self.co_commit()
		self.file.write(" " + "Commit\n")
		self.file.close()
		self.lock.release()



	def co_commit(self):

		print "Calling all replicas to commit"
		for item in self.replicas:
			item.rep_commit()

	def co_abort(self):
		print "Calling all replicas to abort"
		for item in self.replicas:
			item.rep_abort()

def main():
	coor = Coordinator()
	replica_add = ["http://192.168.22.144:8001"]
	print "Connected to replica"

	for add in replica_add:
		try:
			client = xmlrpclib.ServerProxy(add)
			print client
		except:
			print "Wrong"
		coor.replicas.append(client)

	# coor.recover()
	coor.co_put("2", "Testcase2")
	coor.co_put("3", "Testcase3")
	# coor.co_del("2")
	# coor.co_get("2")
	# coor.recover()
 	# coor.co_put("2", "hi")
 	# modify the last transaction to not commit or abort

 	# coor.co_get("2")
 	# coor = Coordinator()


if __name__ == '__main__':
	main()