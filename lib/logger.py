#
# functions
#

def print_cmd(msg):
	print('->', msg, "...")


def print_info(msg):
	print('-I', msg)

def print_error(msg):
	print('-E', msg)


def board_info():
	import sys
	import uos
	import machine
	sw_impl = sys.implementation[0]
	sw_ver = sys.implementation[1]
	uname = uos.uname()
	freq = machine.freq() / 1000000

	print('')
	print('Software: {} {}'.format(sw_impl, sw_ver) )
	print('Uname: {}'.format(uname) )
	print('Frequency: {} Mhz'.format(freq) )
	print('WAKE Reason:', machine.reset_cause())
	print('')


def disable_debug():
	print_cmd('Disable HW Debug')

	import esp
	esp.osdebug(None)
