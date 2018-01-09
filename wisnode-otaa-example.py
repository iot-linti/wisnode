import time
from serial import SerialException
from wisnode import rak, STATUS_JOINED_SUCCESS
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--usb', type=int,help='usb number. Default 0', default=0)
parser.add_argument('--network', type=int,help='1 for ttn, 0 for dass. Default ttn', default=1)
#parser.print_help()

args = parser.parse_args()
usb_num = args.usb
TTN = args.network

if TTN:
	from secrets_otaa import TTN_devEUI as devEUI , TTN_appEUI as appEUI, TTN_appKEY as appKEY
	print 'Usando TTN' 
else:
	print 'Usando DASS'
	from secrets_otaa import DASS_devEUI as devEUI , DASS_appEUI as appEUI, DASS_appKEY as appKEY  
 
try:
	wisnode = rak('ttyUSB{}'.format(usb_num))
except SerialException as e:
	print e.strerror
else:
	print 'Iniciando wisnode'
	print wisnode.rk_reload()
	time.sleep(0.1)
	print wisnode.rk_reset(0)
	time.sleep(1)
	print wisnode.read()
	print 'Get version:'
	print wisnode.rk_getVersion()
	time.sleep(0.1)
	print 'Seteando modo:'
	print wisnode.rk_setWorkingMode(0) # Lora mode
	time.sleep(0.1)

	if TTN:
		print 'Seteando otaa:'
		print wisnode.rk_initOTAA(devEUI,appEUI,appKEY)
	else:
		print 'Seteando dev_eui'
		print wisnode.rk_setConfig('dev_eui', devEUI)
		time.sleep(0.1)
		print 'Seteando app_eui'
		print wisnode.rk_setConfig('app_eui', appEUI)
		time.sleep(0.1)
		print 'Seteando app_key'
		print wisnode.rk_setConfig('app_key', appKEY)

	time.sleep(0.1)
	print 'joining:'
	print wisnode.rk_joinLoRaNetwork(0) # Otaa mode

	recv = wisnode.read()
	print recv
	while recv != '{}\r\n'.format(STATUS_JOINED_SUCCESS):
		print 'joining again:'
		print wisnode.rk_joinLoRaNetwork(0) # Otaa mode
		recv = wisnode.read()
		print recv

	while 1:
		time.sleep(10)
		print 'Sending data:'
		print wisnode.rk_sendData(0,2,str(int(random.random() * 1000)))
		print 'Leyendo de wisnode:'
		print wisnode.read()
		
		#print (wisnode.rk_getSignal())