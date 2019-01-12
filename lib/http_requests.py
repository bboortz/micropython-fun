import usocket as socket


#
# functions
#

def test_connection():
	http_get('http://blog.fefe.de/')


def http_get(url):
	logger.print_cmd('Sending HTTP GET request: {}'.format(url))

	_, _, host, path = url.split('/', 3)
	logger.print_cmd('Retrieving IP for Host: {}'.format(host))
	addr_info = socket.getaddrinfo(host, 80)
	addr = addr_info[0][-1]
	host = addr[0]

	print('Preparing Socket ...')
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	s = socket.socket()
	print('Setting Timeout ...')
	#set_timeout(s)
	logger.print_cmd('Sending HTTP GET to addr: {}'.format(addr))
	s.connect(addr)
	s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
	while True:
		data = s.recv(100)
		if data:
			print(str(data, 'utf8'), end='')
		else:
			break
	s.close()
