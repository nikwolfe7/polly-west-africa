import base64
import traceback
import defines as d
import http
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
	
	except http.client.BadStatusLine as e:
		print("An Exception occurred!\n" + str(e))
		print(traceback.format_exc())
		print("Moving on... Tired of getting SMSs about this... ")
		return False
		
	except Exception as e:
		print("An Exception occurred!\n" + str(e))
		print(traceback.format_exc())
		if str(e) is not '': # hack!!
			tropo_remote_sms(d.sms_alert_number, d.sms_alert_message+str(e))
		print("Moving on...")
		return False

def get_encoding(message):
	msg = message.encode('utf-8')
	return base64.b64encode(msg).decode('utf-8')
	
def spin_register_process(http_request):	
	Q = []
	proc = Process(target=send_request, args=(http_request,))
	Q.append(proc)
	proc.start()

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
	
	
