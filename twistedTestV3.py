from twisted.internet import protocol
from twisted.web.resource import Resource
from twisted.internet import reactor  ,threads ,  utils
from twisted.web.server import NOT_DONE_YET
from twisted.web import server

from time import sleep 
import datetime

class PongProcessProtocol(protocol.ProcessProtocol):
  '''
		A process protocol 
	'''
	imported_file  = None
	listImported = False
	
	def write_a_T(self):
		reactor.callInThread(childrenFile.write, 'T\n')
		
	def add_to_pong(self , add):
		self._pong+=add

	def parse_request(self , request):
		if 'ping' in request.args:
			ping = int(request.args['ping'][0])

		else:
			ping = 127

		self._pong = 0

		processRequestTime = False
		startTime = datetime.datetime.now()
		
		if ping & 8:	
			self.write_a_T()
			ds =threads.deferToThread(numerical_list_to_Convert , self.imported_file)
			ds.addCallback(sort_list)
			ds.addErrback(deferred_error)
			
		if ping & 16:
			self.write_a_T()			
			od =threads.deferToThread(numerical_list_to_Convert , self.imported_file)
			od.addCallback(count_number_odds)
			od.addCallback(self.add_to_pong)

		if ping & 1:	
			self._n = 0 

		if ping & 2:	
			processRequestTime = True

		if ping & 4	:
			reactor.callInThread(wait_ms , 0.01)
								
		if ping & 32:
			self.add_to_pong(2)

		if processRequestTime:
			''' end of the process time '''
			endTime = datetime.datetime.now()
			timeTaken = endTime - startTime
			self.add_to_pong(timeTaken.microseconds)		

	def connectionMade(self , request):
		output = utils.getProcessOutput(self.parse_request,request)
		output.addCallbacks(self.writeResponse)
        

	def writeResponse(self, pong):
		self.transport.write("<html> pong " + str(self._pong) + "</html>")
		self.transport.loseConnection()



def import_file():
	imported_file =  open('r10000.txt')
	return imported_file

def wait_ms(ms):
	sleep(ms)
	

def sort_list(list_to_sort):
	list_to_sort.sort()


def numerical_list_to_Convert(list_to_convert):
	return list(list_to_convert)


def count_number_odds(list_to_count_odds):
	oddNums = 0 
	for num in list_to_count_odds:
		if int(num) % 2 == 0:
			oddNums+=1

  	return oddNums

def deferred_error(f):
	'''
	Error handling for defers
	'''
	print "errback"
	print "we got an exception: %s" % (f.getTraceback())
	f.trap(RuntimeError)


global childrenFile
childrenFile = open('children.txt', 'w+')

class Pong(Resource):
	

	def render_GET(self , request):

		if not self.listImported:
			self.imported_file =  import_file()
			self.listImported = True

		#ppp = PongProcessProtocol()
		#reactor.spawnProcess(ppp, ["wc"], {})
		reactor.callLater(0, self.parse_request, request)

		return NOT_DONE_YET

root = Resource()
root.putChild("ping" , Pong())
site = server.Site(root)
reactor.listenTCP(8000, site)
reactor.suggestThreadPoolSize(30)

try:
    reactor.run()
except KeyboardInterrupt:
	childrenFile.close()
	reactor.stop()
