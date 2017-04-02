import websocket
# import thread
import simplejson as json
 
SOCKET_IO_HOST = "localhost"
SOCKET_IO_PORT = 5000
socket_io_url = 'http://' + SOCKET_IO_HOST + ':' + str(SOCKET_IO_PORT) + '/socket.io/websocket'
def encode_for_socketio(message):
    """
   Encode 'message' string or dictionary to be able
   to be transported via a Python WebSocket client to
   a Socket.IO server (which is capable of receiving
   WebSocket communications). This method taken from
   gevent-socketio.
   """
    MSG_FRAME = "~m~"
    HEARTBEAT_FRAME = "~h~"
    JSON_FRAME = "~j~"
 
    if isinstance(message, basestring):
            encoded_msg = message
    elif isinstance(message, (object, dict)):
            return encode_for_socketio(JSON_FRAME + json.dumps(message))
    else:
            raise ValueError("Can't encode message.")
 
    return MSG_FRAME + str(len(encoded_msg)) + MSG_FRAME + encoded_msg
ws = None
 
def sendMsg(m=''):
        global ws
        if ws == None:
                ws = websocket.create_connection(socket_io_url)
        ws.send(encode_for_socketio({'message':m}))

sendMsg("Test")