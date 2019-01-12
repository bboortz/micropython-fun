import logger
import socket as socket
import ujson as json
import http_timeouts


# 
# global constants
#

SERVER_PORT   = 80
SERVER_ADDRESS     = ('0.0.0.0', SERVER_PORT)
REQUEST_QUEUE_SIZE = 1



#
# functions
#

def web_page():
	json_data = {
		"status": {
			"healthy": True,
			"connected": True
		},
		"data": {
			"temperature": 20,
			"humidity": 10
		}
	}
	return json_data


def run_webserver():
	logger.print_cmd('Starting Webserver')

	s = socket.socket()
#	http_timeouts.set_timeout(s)
#	s.settimeout(TIMEOUT)
	s.bind(SERVER_ADDRESS)
	s.listen(REQUEST_QUEUE_SIZE)

	print('Serving HTTP on port {port} ...'.format(port=SERVER_PORT))

	while True:
		conn, addr = s.accept()
		request = conn.recv(1024)
		request = str(request)
		print('%s - %s' % (addr[0], request))
		json_str = json.dumps(web_page())
		response = json_str + '\r\n'
		conn.send(response)
		conn.close()
