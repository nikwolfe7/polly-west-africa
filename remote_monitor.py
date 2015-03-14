import base64
import traceback
import defines as d
import http
import socket
import os
from common import xprint
try: import urllib.request as urllib2
except ImportError: import urllib2
from multiprocessing import Process

def send_request(http_request):
	#xprint("HTTP Request Generated: " + http_request)
	try:
		wp = urllib2.urlopen(str(http_request), timeout=d.web_request_timeout)
		wp = wp.read().decode('utf-8').lower()
		#xprint("HTTP Response:\n\n"+wp+"\n")
		return d.REQUEST_SUCCESS.lower() in wp
	
	except http.client.BadStatusLine as e:
		xprint("An Exception occurred!\n" + str(e))
		xprint(traceback.format_exc())
		xprint("Moving on... Tired of getting SMSs about this... ")
		backup_failed_logging_request(http_request)
		return False
	
	except socket.timeout:
		xprint("Socket timeout! Current timeout: " + str(socket.getdefaulttimeout()))
		backup_failed_logging_request(http_request)
		return False
	
	except urllib2.URLError as e:
		xprint("URL Error... Timeout?\n" + str(e))
		xprint(traceback.format_exc())
		backup_failed_logging_request(http_request)
		return False

	except urllib2.UnknownHandler as e:
		xprint("Unknown URL type!\n" + str(e))
		xprint(traceback.format_exc())
		xprint("Here it is: " + http_request)
		backup_failed_logging_request(http_request)
		return False

	except ValueError as e:
		xprint("Unknown URL type!\n" + str(e))
		xprint(traceback.format_exc())
		xprint("Here it is: " + http_request)
		backup_failed_logging_request(http_request)
		return False
		
	except Exception as e:
		xprint("An Exception occurred!\n" + str(e))
		xprint(traceback.format_exc())
		if str(e) != '' and http_request.startswith("http://"): # hack!!
			tropo_remote_sms(d.sms_alert_number, d.sms_alert_message+str(e))
		xprint("Moving on...")
		backup_failed_logging_request(http_request)
		return False

def backup_failed_logging_request(http_request):
	if http_request.startswith("http://"):
		open(d.log_dir + d.remote_logging_backup_queue,'a').write(http_request+"\n")

def retry_backup_logging_queue():
	if os.path.isfile(d.log_dir + d.remote_logging_backup_queue): 
		failed_logs = [x.strip() for x in open(d.log_dir + d.remote_logging_backup_queue).readlines()]
		if len(failed_logs) > d.backup_logging_requests_batch_retry_size:
			open(d.log_dir + d.remote_logging_backup_queue,'w')
			while failed_logs:
				message = failed_logs.pop(0)
				xprint(">>>> Retrying request: "+message)
				send_request(message)

def get_encoding(message):
	msg = message.encode('utf-8')
	return base64.b64encode(msg).decode('utf-8')
	
def spin_register_process(http_request):	
	Q = []
	# we don't care about doing this quickly, so maintain a backup queue
	backup = Process(target=retry_backup_logging_queue)
	Q.append(backup)
	proc = Process(target=send_request, args=(http_request,))
	Q.append(proc)
	for p in Q:
		p.start()

def clean_msg_for_url(msg):
	return urllib2.quote(msg)
	
def tropo_remote_sms(recipient, msg):
	xprint("Sending SMS to Tropo...")
	recipient = clean_msg_for_url(recipient.lstrip('0'))
	msg = clean_msg_for_url(msg)
	tropo_request = d.tropo_request_polly_sante.replace(d.tropo_recipient,recipient).replace(d.tropo_message,msg)
	spin_register_process(str(tropo_request))
	
def update(update, retval=False):
	#xprint("Sending update to remote monitoring system...")
	update = get_encoding(update)
	http_request = "http://" + d.ip_optiplex + "/" + d.app + d.monitor_script + update
	if retval:
		return send_request(http_request)
	else:
		spin_register_process(http_request)
		

# ====================================================== #			
if __name__ == "__main__":
	update("+1927593134,34,223.56,CellComGN,AT+CNUM")
	
	
