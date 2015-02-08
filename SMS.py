import time
import sys
from common import new_log_file,connect,update_log
	
class SendSMS:
	def __init__(self,com_port):
		self.com = com_port
		self.phone = None
		self.wait = 0.3
		self.log_file = new_log_file("AT-log")
		
	def send_message(self,recipient,message):
		self.phone = connect(self.com)
		self.send('ATZ')
		self.send('AT+CMGF=1')
		self.send('AT+CMGS="' + recipient + '"')
		self.send(message)
		self.phone.write(bytes([26]))
		time.sleep(self.wait)
		self.close_sms()
	
	def send(self,msg):
		update_log(self.log_file,msg)
		self.phone.write(bytearray(msg,'utf8') + b'\r')
		time.sleep(self.wait)
		
	def close_sms(self):
		time.sleep(self.wait)
		self.phone.close()
		time.sleep(self.wait)


if __name__ == "__main__":
	com = sys.argv[1] # COM port the dongle is connected to, e.g. COM11
	recipient = "+19543679247"
	message = "I've finally made this shit work!"
	sender = SendSMS(com)
	sender.send_message(recipient,message)
	sender.send_message(recipient,"fresh one!")
	sender.send_message(recipient,"another!")
