import sys
import SMS
import time
import defines
from common import echo,new_log_file,update_log,connect

class AT:
	def __init__(self,com_port):
		self.com = com_port
		self.phone = None
		self.wait = defines.wait_time
		self.sms_module = SMS.SendSMS(self.com)
		self.log_file = new_log_file(defines.at_log)	
		
	def initialize_connection(self):
		if self.phone is None:
			self.phone = connect(self.com)
			self.send('ATE1V1')
			if("OK" not in self.read()):
				echo("Couldn't connect to "+self.com+" or port already in use!")
				return False
		return True
		
	def send_at(self,at_command, log=False):
		if self.initialize_connection():
			self.send(at_command, log)
			response = self.read()
			# no need to close connection...
			#self.close_connection() 
			return (response,True)
		else:
			return ("",False)
		
	def send(self, msg, log=False):
		if self.initialize_connection():
			if log: update_log(self.log_file, msg)
			self.phone.write(bytearray(msg,'utf8') + b'\r')
			time.sleep(self.wait)
	
	def poll(self):
		# intentionally leaves connection open...
		if self.initialize_connection():
			return self.read()
	
	def read(self):
		self.phone.flush() # wait until all chars are written
		chars = self.phone.inWaiting()
		msg = self.phone.read(chars).decode('utf-8')
		if msg.strip() != "":
			update_log(self.log_file, msg)		
		return msg
		
	def send_sms(self,recipient,message):
		self.sms_module.send_message(recipient,message);
		
	def clear_buffers(self):
		if self.phone is not None:
			self.phone.flushInput()
			self.phone.flushOutput()
		
	def close_connection(self):
		if self.phone is not None:
			time.sleep(self.wait)
			self.clear_buffers()	
			self.phone.close()
			self.phone = None
			time.sleep(self.wait)		
			
# ====================================================== #			
if __name__ == "__main__":
	phone_num = "+19543679247"
	#phone_num = "+14123133585" # Rahul, lol
	com = sys.argv[1] # COM port the dongle is connected to, e.g. COM11
	at_module = AT(com)
	echo(at_module.send_at('ATD'+phone_num+';'))
	time.sleep(10)
	echo(at_module.send_at('AT+CHUP'))
	echo(at_module.send_at('AT'))
	echo(at_module.send_at('AT+CNUM'))
	at_module.send_sms(phone_num,'hello!')
	at_module.send_sms(phone_num,'hey!')
	
