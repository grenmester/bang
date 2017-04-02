from socketIO_client import SocketIO, LoggingNamespace
import struct
import threading
import Queue
import time


class ClientCommand(object):
	""" A command to the client thread.
		Each command type has its associated data:

	   CONNECT:    (host, port) tuple
		SEND:       Data string
		RECEIVE:    None
		CLOSE:      None
	"""
	CONNECT, SEND, RECEIVE, CLOSE = range(4)

	def __init__(self, type, data=None):
		self.type = type
		self.data = data


class ClientReply(object):
	""" A reply from the client thread.
		Each reply type has its associated data:

		ERROR:      The error string
		SUCCESS:    Depends on the command - for RECEIVE it's the received
					data string, for others None.
	"""
	ERROR, SUCCESS = range(2)

	def __init__(self, type, data=None):
		self.type = type
		self.data = data


class SocketClientThread(threading.Thread):
	""" Implements the threading.Thread interface (start, join, etc.) and
		can be controlled via the cmd_q Queue attribute. Replies are
		placed in the reply_q Queue attribute.
	"""
	def __init__(self, cmd_q=None, reply_q=None):
		super(SocketClientThread, self).__init__()
		self.cmd_q = cmd_q or Queue.Queue()
		self.reply_q = reply_q or Queue.Queue()
		self.alive = threading.Event()
		self.alive.set()
		self.socket = None

		self.handlers = {
			ClientCommand.CONNECT: self._handle_CONNECT,
			ClientCommand.CLOSE: self._handle_CLOSE,
			ClientCommand.SEND: self._handle_SEND,
			ClientCommand.RECEIVE: self._handle_RECEIVE,
		}

	def run(self):
		while self.alive.isSet():
			try:
				# Queue.get with timeout to allow checking self.alive
				cmd = self.cmd_q.get(True, 0.1)
				self.handlers[cmd.type](cmd)
			except Queue.Empty as e:
				continue

	def join(self, timeout=None):
		self.alive.clear()
		threading.Thread.join(self, timeout)

	def _handle_CONNECT(self, cmd):
		try:
			self.socket = SocketIO(cmd.data[0], cmd.data[1], LoggingNamespace)
			self.socket
			self.reply_q.put(self._success_reply())
		except IOError as e:
			self.reply_q.put(self._error_reply(str(e)))

	def _handle_CLOSE(self, cmd):
		self.socket.wait(cmd.data)
		reply = ClientReply(ClientReply.SUCCESS)
		self.reply_q.put(reply)

	def _handle_SEND(self, cmd):
		try:
			self.socket.emit(cmd.data[0], cmd.data[1])
			self.reply_q.put(self._success_reply())
		except IOError as e:
			self.reply_q.put(self._error_reply(str(e)))

	def _handle_RECEIVE(self, cmd):

		def callback(*args):
			self.reply_q.put(self._success_reply(args[0]))
		try:
			self.socket.on(cmd.data[1], callback)
			self.socket.wait(cmd.data[0])
			
		except IOError as e:
			self.reply_q.put(self._error_reply(str(e)))

	def _error_reply(self, errstr):
		return ClientReply(ClientReply.ERROR, errstr)

	def _success_reply(self, data=None):
		return ClientReply(ClientReply.SUCCESS, data)

if __name__ == "__main__":
	x = 0
	start = time.time()
	sct = SocketClientThread()
	sct.start()
	sct.cmd_q.put(ClientCommand(ClientCommand.CONNECT, ('localhost', 5001)))
	reply = sct.reply_q.get(True)
	print(reply.type, reply.data)
	sct.cmd_q.put(ClientCommand(ClientCommand.SEND, ("test", {"hellothere":1})))
	reply = sct.reply_q.get(True)
	print(reply.type, reply.data)
	sct.cmd_q.put(ClientCommand(ClientCommand.RECEIVE, (.5, "test2")))
	reply = sct.reply_q.get(True)
	print(reply.type, reply.data)
	sct.cmd_q.put(ClientCommand(ClientCommand.SEND, ("test", {"hellothere":1})))
	reply = sct.reply_q.get(True)
	print(reply.type, reply.data)
	sct.cmd_q.put(ClientCommand(ClientCommand.RECEIVE, (.5, "test2")))
	reply = sct.reply_q.get(True)
	print(reply.type, reply.data)
	sct.cmd_q.put(ClientCommand(ClientCommand.SEND, ("test", {"hellothere":1})))
	reply = sct.reply_q.get(True)
	print(reply.type, reply.data)
	sct.cmd_q.put(ClientCommand(ClientCommand.RECEIVE, (.5, "test2")))
	reply = sct.reply_q.get(True)
	print(reply.type, reply.data)
	sct.cmd_q.put(ClientCommand(ClientCommand.CLOSE, .5))
	reply = sct.reply_q.get(True)
	print(reply.type, reply.data)
	sct.cmd_q.put(ClientCommand(ClientCommand.CONNECT, ('localhost', 5001)))
	reply = sct.reply_q.get(True)
	end = time.time()

	print(end - start)
