#PollyLogger
import serial
import time
import os
import defines

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
def web_request_timestamp(): return nice_date_time().strip("][").replace("|","%20").replace(":","%3A")

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
	print(msg)
	import remote_monitor
	time_stamp()
	remote_monitor.update(pre + defines.file_delim + msg, retval)
	update_log(polly_log_full,msg)

# ====================================================== #	
# logging for events in CSV format
# msg is expected to be an array...
def csvecho(msg, pre="CSV", retval=True):
	print(msg)
	import remote_monitor
	stamp = [nice_date_time()]
	msg = stamp + msg
	msg =  defines.file_delim.join(msg)
	if retval:
		if not remote_monitor.update(pre + defines.file_delim + msg, retval):
			raise Exception("Database INSERT failed!")
	else:
		remote_monitor.update(pre + defines.file_delim + msg, retval)
	update_log(polly_log,msg)
	
# ====================================================== #
def connect(com):
	return serial.Serial(port=com,baudrate=defines.baudrate,timeout=None)
	
# ====================================================== #	
def is_number(var):
	try:
		float(var)
		return True
	except ValueError:
		pass
	try:
		import unicodedata
		unicodedata.numeric(var)
		return True
	except (TypeError,ValueError):
		pass
	return False

# ====================================================== #	
def xprint(msg): 
	exfile = new_log_file(defines.exception_log)
	update_log(exfile, prefix("EXCEPTION") + msg)
	print(msg)

# ====================================================== #	
def new_pending_requests_log():
	if not os.path.isfile(defines.log_dir + defines.pending_reqs):
		echo("No pending requests file found... Creating placeholder...")
		delayed_reqs = open(defines.log_dir + defines.pending_reqs,"w")
		delayed_reqs.close()
	
# ====================================================== #
def backup_failed_request(http_request):
	new_pending_requests_log()
	if http_request.startswith("http://"):
		existing_reqs = [l.strip() for l in open(defines.log_dir + defines.pending_reqs).readlines()]
		if not http_request in existing_reqs: 
			open(defines.log_dir + defines.pending_reqs,"a").write(http_request + "\n")
			echo("Successfully backed up failed request: " + http_request)
		else: 
			echo("This request has already been queued. No need to back up.")	
