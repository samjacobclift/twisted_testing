
from twisted.web.resource import Resource
from twisted.internet import reactor
#from twisted.internet import threads , defer
from twisted.web import server
#from twisted.internet.defer import Deferred

from time import sleep 
import datetime

numberOfThreads = 15


class Pong(Resource):

  def render_GET(self ,request):

		''' get the ping'''
		if 'ping' in request.args:
			ping = int(request.args['ping'][0])

		else:
			''' no ping so default to 127'''
			ping = 127


		pp = Parse_Pong()
		pong = pp.parse_the_ping(ping)
		#d = Deferred()
		#d.addCallback(pp.parse_the_ping)
		#d.addErrback(pp.failed)

		#d.callback(ping)

		return "<html> pong " + str(pong) + "</html>"


class Parse_Pong():
	'''
	Parse the pong
	'''
	def parse_the_ping(self , ping):
		n = 0
		processRequestTime = False
		startTime = datetime.datetime.now()
		_listImported = False

		''' 1: n =0 '''
		if bin(ping).endswith('1'):	
			n = 0 

		ping = ping >> 1

		''' 2: Process Request Time '''
		if bin(ping).endswith('1'):	
			processRequestTime = True

		ping = ping >> 1
		
		''' 4: Sleep '''
		if bin(ping).endswith('1'):	
			self.wait_ms(0.01)

		ping = ping >> 1
		
		''' 8: load (if not already loaded) numeric conversion and sort ''' 
		if bin(ping).endswith('1'):	
			if not _listImported:
				_listImported = True
				self.numerical_list_Import_Convert()

			''' sort '''
			self.sort_list()

		ping = ping >> 1
		
		''' 16: count the number of odd numbers in the list ''' 
		if bin(ping).endswith('1'):	
			if not _listImported:
				_listImported = True
				self.numerical_list_Import_Convert()

			n+=self.count_number_odds(self._numbers)

		ping = ping >> 1

		''' 32: number of times reading the file ''' 
		#if bin(ping).endswith('1'):
			


		if processRequestTime:
			''' end of the process time '''
			endTime = datetime.datetime.now()
			timeTaken = endTime - startTime
			n+= timeTaken.microseconds

		return n

	   
	def failed(self):
		''' failed'''
		print 'failed'

	def wait_ms(self ,ms):
		''' Waits for 10ms '''
		sleep(ms)
		
	def sort_list(self):
		''' sorts a given list '''
		self._numbers.sort()

	def numerical_list_Import_Convert(self):

		numberFile =  open('r10000.txt')
		self._numbers =[]

		for n in numberFile:
	 	 	self._numbers.append(int(n))


	def count_number_odds(self ,list_to_count_odds):
		''' finds the number of odds in a list '''
		oddNums = 0 

		for num in list_to_count_odds:
			if num % 2 == 0:
				oddNums+=1

	  	return oddNums



root = Resource()
root.putChild("ping" , Pong())
site = server.Site(root)
reactor.listenTCP(8000, site)

''' Create a pool of threads '''
reactor.suggestThreadPoolSize(numberOfThreads)
# Start the reactor
try:
    reactor.run()
except KeyboardInterrupt:
    reactor.stop()
