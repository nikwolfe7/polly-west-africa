#PollyLogger
import serial
import time
import os
import defines
import remote_monitor

# ====================================================== #
# Useful stuff...
# ====================================================== #
class Tstamp:
	def __init__(self): self.timestamp_update = 0
	def increment(self): self.timestamp_update += 1
	def clear(self): self.timestamp_update = 0
		
t = Tstamp()
# ====================================================== #		
def nice_date(): return "["+time.strftime('%Y-%m-%d')+"]"

# ====================================================== #		
def nice_date_time(): return "["+time.strftime('%Y-%m-%d|%H:%M:%S')+"]"

# ====================================================== #	
def update_log(log_file,msg):
	at_log = open(defines.log_dir+log_file,"a")
	at_log.write(str(msg).strip()+"\n")
	at_log.close()

# ====================================================== #	
def new_log_file(name):
	new_file = name+"-"+nice_date().strip("[]")+".txt"
	if not os.path.isfile(defines.log_dir+new_file): # initialize file...
		update_log(new_file,"STARTED:"+nice_date_time())
	return new_file

# ====================================================== #	
def prefix(com_port):
	return "[" + com_port + "] " + nice_date_time() + " "

# ====================================================== #
polly_log = new_log_file(defines.logfile)
polly_log_full = new_log_file(defines.logfile_full)
# ====================================================== #	
def time_stamp():
	# every 10 echo calls, we output a timestamp
	t.increment()
	if t.timestamp_update % 10 == 0:
		t.clear()
		timestamp = nice_date_time().replace("[","[DATE|TIME : ")
		print(timestamp)
		update_log(polly_log_full,timestamp)

# ====================================================== #	
# simple logging... the default
def echo(msg, pre="LOG", retval=False):
	time_stamp()
	remote_monitor.update(pre + defines.file_delim + msg, retval)
	update_log(polly_log_full,msg)
	print(msg)

# ====================================================== #	
# logging for events in CSV format
# msg is expected to be an array...
def csvecho(msg, pre="CSV", retval=True):
	stamp = [nice_date_time()]
	msg = stamp + msg
	msg =  defines.file_delim.join(msg)
	if retval:
		if not remote_monitor.update(pre + defines.file_delim + msg, retval):
			raise Exception("Database INSERT failed!")
	else:
		remote_monitor.update(pre + defines.file_delim + msg, retval)
	update_log(polly_log,msg)
	print(msg)
	
# ====================================================== #
def connect(com):
	return serial.Serial(port=com,baudrate=defines.baudrate,timeout=None)
	
