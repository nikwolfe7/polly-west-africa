import base64
import traceback
import defines as d
import http
import socket
import os
try: import urllib.request as urllib2
except ImportError: import urllib2
from multiprocessing import Process

def send_request(http_request):
	#print("HTTP Request Generated: " + http_request)
	try:
		wp = urllib2.urlopen(http_request, timeout=d.web_request_timeout)
		wp = wp.read().decode('utf-8')
		#print("HTTP Response:\n\n"+wp+"\n")
		return "SUCCESS" in wp
	
	except ValueError as e:
		print("Unknown URL type! But fuck it, right?\n" + str(e))
		print("Here it is: " + http_request)
		backup_failed_request(http_request)
		return False
	
	except http.client.BadStatusLine as e:
		print("An Exception occurred!\n" + str(e))
		print(traceback.format_exc())
		print("Moving on... Tired of getting SMSs about this... ")
		backup_failed_request(http_request)
		return False
	
	except socket.timeout:
		print("Socket timeout! Current timeout: " + socket.getdefaulttimeout())
		backup_failed_request(http_request)
		return False
	
	except urllib2.URLError as e:
		print("URL Error... Timeout?")
		print(str(e))
		backup_failed_request(http_request)
		return False

	except (urllib2.UnknownHandler,urllib2.ValueError) as e:
		print("Unknown URL type! But fuck it, right?\n" + str(e))
		print("Here it is: " + http_request)
		backup_failed_request(http_request)
		return False
		
	except Exception as e:
		print("An Exception occurred!\n" + str(e))
		print(traceback.format_exc())
		if str(e) is not '' and http_request.startswith("http://"): # hack!!
			tropo_remote_sms(d.sms_alert_number, d.sms_alert_message+str(e))
		print("Moving on...")
		backup_failed_request(http_request)
		return False

def backup_failed_request(http_request):
	if http_request.startswith("http://"):
		open(d.remote_logging_backup_queue,'a').write(http_request+"\n")

def retry_backup_queue():
	if os.path.isfile(d.remote_logging_backup_queue): 
		failed_logs = [x.strip() for x in open(d.remote_logging_backup_queue).readlines()]
		open(d.remote_logging_backup_queue,'w')
		while failed_logs:
			message = failed_logs.pop(0)
			print(">>>> Retrying request: "+message)
			send_request(message)

def get_encoding(message):
	msg = message.encode('utf-8')
	return base64.b64encode(msg).decode('utf-8')
	
def spin_register_process(http_request):	
	Q = []
	# we don't care about doing this quickly, so maintain a backup queue
	backup = Process(target=retry_backup_queue)
	Q.append(backup)
	proc = Process(target=send_request, args=(http_request,))
	Q.append(proc)
	for p in Q:
		p.start()

def clean_msg_for_url(msg):
	return msg.replace(" ","%20").replace("+", "%2B")
	
def tropo_remote_sms(recipient, msg):
	print("Sending SMS to Tropo...")
	recipient = clean_msg_for_url(recipient.lstrip('0'))
	msg = clean_msg_for_url(msg)
	tropo_request = d.tropo_request.replace(d.tropo_recipient,recipient).replace(d.tropo_message,msg)
	spin_register_process(str(tropo_request))
	
def update(update, retval=False):
	#print("Sending update to remote monitoring system...")
	update = get_encoding(update)
	http_request = "http://" + d.ip_optiplex + "/" + d.app + d.monitor_script + update
	if retval:
		return send_request(http_request)
	else:
		spin_register_process(http_request)
		

# ====================================================== #			
if __name__ == "__main__":
	update("+1927593134,34,223.56,CellComGN,AT+CNUM")
	
	
