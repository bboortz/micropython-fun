import uselect



# 
# global constants
#

TIMEOUT            = 3000				# in milliseconds



#
# functions
#

def set_timeout(s):
	poller = uselect.poll()
	poller.register(s, uselect.POLLIN)
	res = poller.poll(TIMEOUT)  # time in milliseconds
	if not res:
		print("timed out!")
		s.close()
