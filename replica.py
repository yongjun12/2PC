import xmlrpclib 
from SimpleXMLRPCServer import SimpleXMLRPCServer
import sqlite3 as lite
import os.path


class Replica:
	def __init__(self, name):
		self.name = name
		self.file = open(self.name + '.log', 'a+')

		try:
			self.conn = lite.connect(self.name + '.db')
			self.cur = self.conn.cursor()
			if(os.path.isfile(self.name + '.db') == False):
				self.file.write("Create table info Commit\n")
				self.cur.execute('CREATE TABLE IF NOT EXISTS Info(key INT PRIMARY KEY, value TEXT)')
				self.conn.commit()
		except lite.Error, e:
			print "Error %s" % e.args[0]
			sys.exit(1)
		# finally:
		# 	if(self.conn):
		# 		self.conn.close()

	def recover(self):
		last_line = ""
		self.file = open(self.name + ".log", "r+")

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

		if action == "put":
			print "recover put function" 
			self.cur.execute('INSERT INTO Info VALUES(? , ?)', (para[1], para[2]))
			
		elif action == "get":
			print "recover get function" 
			self.cur.execute('SELECT value FROM Info WHERE KEY = ?', para[1])
		elif action == "del":
			print "recover del function" 
			self.cur.execute('DELETE FROM Info WHERE KEY = ?', para[1])

		self.conn.commit()
		self.file = open(self.name + ".log", "a+")
		self.file.write(" Commit\n")
		self.file.flush()
		self.isRecover = 0
	



	def rep_get(self, key):
		ret = ""
		print self.name
		
		self.file = open(self.name + '.log', 'a+')
		self.file.write("get " + key)
		self.file.flush()

		try:
			self.cur.execute('SELECT value FROM Info WHERE key = ?', key)
			ret = self.cur.fetchone()
			# print  type(ret)
		except Exception, e:
			print e.args

		return str(ret)

	def rep_put(self, key, value):

		self.file = open(self.name + '.log', 'a+')
		self.file.write("put " + key + " " + value)
		# self.file.flush()

		try:
			self.cur.execute('INSERT OR REPLACE INTO Info VALUES(?, ?)', (key, value))
		except lite.Error, e:
			print e.args

		return True

	def rep_del(self, key):

		self.file = open(self.name + '.log', 'a+')
		self.file.write("del " + key)
		self.file.flush()

		try:
			self.cur.execute('DELETE FROM Info WHERE key = ?', key)
		except lite.Error, e:
			print e.args
		return True
	
	def rep_decide(self):
		line = self.log.readline()
		params = line.split(" ")
		if(params[0]):
			rep_recover()
			return False
		else:
			return True

	def rep_commit(self):
		try:
			self.conn.commit()
		except lite.Error, e:
			print e.args

		self.file = open(self.name + '.log', 'a+')
		self.file.write(" Commit\n")
		self.file.flush()

		return True		

	def rep_abort(self):
		try: 
			self.conn.abort()
		except lite.Error, e:
			print e.args

		self.file = open(self.name + '.log', 'a+')
		self.file.write(" Abort\n")
		self.file.flush()

		return True

def main():
	try:
		server = SimpleXMLRPCServer(("localhost", 8000))
		# server2 = SimpleXMLRPCServer(("localhost", 8001))
		print "Listen"
		replica = Replica('Bob')
		replica.recover()
		# relica2 = Replica('Anne')
		server.register_instance(replica)
		server.serve_forever()


	except Exception,e:
		print e.args

	# replica = Replica('Bob')
	# print replica.rep_get('1')

if __name__ == '__main__':
	main()
