import serial
from serial import SerialException
import binascii
#import time

STATUS_RECV_DATA = "at+recv=0,0,0"
STATUS_TX_COMFIRMED = "at+recv=1,0,0"
STATUS_TX_UNCOMFIRMED = "at+recv=2,0,0"
STATUS_JOINED_SUCCESS = "at+recv=3,0,0"
STATUS_JOINED_FAILED = "at+recv=4,0,0"
STATUS_TX_TIMEOUT = "at+recv=5,0,0"
STATUS_RX2_TIMEOUT = "at+recv=6,0,0"
STATUS_DOWNLINK_REPEATED = "at+recv=7,0,0"
STATUS_WAKE_UP = "at+recv=8,0,0"
STATUS_P2PTX_COMPLETE = "at+recv=9,0,0"
STATUS_UNKNOWN = "at+recv=100,0,0"

class rak:
	def __init__(self, port):
			self.ser = serial.Serial('/dev/{}'.format(port),115200,timeout=20)
	def rk_getVersion(self):
		return self.sendCommand('at+version')

	def rk_getBand(self):
		return self.sendCommand('at+band')

	def rk_sleep(self):
		return self.sendCommand('at+sleep')

	def rk_reset(self, mode):
		if mode == 0 or mode == 1:
			return self.sendCommand('at+reset={}'.format(mode))
		else:
			print 'Incorrect mode, must be 1 or 0'

	def rk_reload(self):
		return self.sendCommand('at+reload')
	
	# Modifica el data rate de la siguiente transmision si
	# ADR no esta activado
	# Para banda us915 valores entre 0 y 4
	def rk_setRate(self,rate):
		return self.sendCommand('at+dr={}'.format(rate))

	def rk_getSignal(self):
		return self.sendCommand('at+signal')


	# mode = 0 para Lorawan
	# mode = 1 para P2P
	def rk_setWorkingMode(self,mode):
		if mode == 0 or mode == 1:
			return self.sendCommand('at+mode={}'.format(mode))
		else:
			print 'Incorrect mode, must be 1 or 0'


	def rk_initOTAA(self, devEUI, appEUI, appKEY):
		return self.sendCommand('at+set_config=dev_eui:{}&app_eui:{}&app_key:{}'.format(devEUI,appEUI,appKEY))
		

	def rk_initABP(self,devADDR, nwksKEY, appsKEY):
		return self.sendCommand('at+set_config=dev_addr:{}&nwks_key:{}&apps_key:{}'.format(devADDR,nwksKEY,appsKEY))


	# Inicia el modo de activacion y se conecta a la red
	# rk_initOTAA y rk_initABP deben llamarse antes

	def rk_joinLoRaNetwork(self, mode):
		if mode == 0:
			return self.sendCommand('at+join=otaa')
		elif mode == 1:
			return self.sendCommand('at+join=abp')
		else:
			print 'Incorrect mode, must be 1 or 0'	

	def rk_setConfig(self, key, value):
			return self.sendCommand('at+set_config={}:{}'.format(key,value))

	def rk_getConfig(self,key):
		return self.sendCommand('at+get_config={}'.format(key))

	def rk_sendData(self,sendType,port,data):
		datahex = binascii.hexlify(data)
		return self.sendCommand('at+send={},{},{}'.format(sendType,port,datahex))

    #def rk_recvData(self):
    #	pass
    

	#######################################################
	def read(self):
	    line = self.ser.readline()
	    return line

	def sendCommand(self, command):
		self.ser.write('{}\r\n'.format(command))     # write a string
		return self.read()
	#######################################################

'''
try:
	wisnode = rak('ttyUSB0')
except SerialException as e:
	print e.strerror
else:
	print 'Get version:'
	print wisnode.rk_getVersion()
	time.sleep(0.1)
	print 'Band'
	print (wisnode.rk_getBand())
	# time.sleep(0.1)
	# print (wisnode.rk_sleep())
	# time.sleep(0.1)
	# print (wisnode.rk_reset(0))
	# time.sleep(0.1)
	# print (wisnode.rk_reload())
	# time.sleep(0.1)
	# print (wisnode.rk_setRate(5))
	#time.sleep(0.1)
	#print (wisnode.rk_getSignal())
	# time.sleep(0.1)
'''
