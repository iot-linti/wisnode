from secrets_abp import devADDR, nwksKEY, appsKEY
import time
from serial import SerialException
from wisnode import rak, STATUS_JOINED_SUCCESS


try:
	wisnode = rak('ttyUSB0')
except SerialException as e:
	print e.strerror
else:
	print 'Get version:'
	print wisnode.rk_getVersion()
	print 'Seteando modo:'
	print wisnode.rk_setWorkingMode(0) # Lora mode
	time.sleep(0.1)
	print 'Seteando otaa:'
	print wisnode.rk_initABP(devADDR,nwksKEY,appsKEY)
	time.sleep(0.1)
	print 'joining:'
	print wisnode.rk_joinLoRaNetwork(1) # ABP mode

	while 1:
		time.sleep(5)
		print 'Leyendo de wisnode:'
		print wisnode.read()
		time.sleep(0.1)
		print 'Sending data'
		print wisnode.rk_sendData(0,2,'Hola Emilio')
	
		
