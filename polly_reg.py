import defines as d
from common import echo,web_request_timestamp
import traceback
try: import urllib.request as urllib2
except ImportError: import urllib2
from multiprocessing import Process

def send_request(http_request, return_request=False):
	echo("HTTP Request Generated: " + http_request)
	if return_request:
		echo("Returning HTTP request to main script for SMS...")
		return http_request
	
	try:
		wp = urllib2.urlopen(http_request, timeout=d.web_request_timeout).read().decode('utf-8').replace("<br>","\n")
		request_id = "REQUEST_PENDING"
		if "ID =" in wp: request_id = wp.split("=")[-1].strip()
		echo("HTTP Response:\n\n"+wp+"\n")
		echo("ID: "+request_id)
		return request_id
	
	except Exception as e:
		echo("An Exception occurred!\n" + str(e))
		echo(traceback.format_exc())
		echo("Moving on...")
		
		# log the failed request
		echo("Failed to register request! Logging the request to try later...")
		pending = open(d.log_dir+d.pending_reqs, "a")
		pending.write(http_request + "\n")
		pending.close()
		echo("Failed request logged!")
		return "REGISTER_FAILED"

def polly_request(phno, syslang, msglang, channel, iccid, app_ip, return_request=False):
	echo("Registering phno="+phno+" and iccid="+iccid+" with Polly...")
	ip = "http://" + app_ip
	app = "/" + d.app
	timeofreq = web_request_timestamp()
	http_request = ip + app + d.script + phno + d.syslang_prefix + syslang + \
		d.msglang_prefix + msglang + d.channel_prefix + channel + d.iccid_prefix + iccid + \
		d.timeofreq_prefix + timeofreq
	return send_request(http_request, return_request)

def spin_register_process(phno, syslang, msglang, channel, iccid, app_ip, return_request=False):	
	Q = []
	proc = Process(target=polly_request, args=(phno,syslang,msglang,channel,iccid,app_ip,return_request))
	Q.append(proc)
	proc.start()
	
def polly_register(phno, syslang=d.fr, msglang=d.fr, channel=d.channel, dest=d.POLLY_GAME, return_request=False, retval=False):
	echo("\nRegister Parameters:\n\nSystem Language:\t"+syslang+"\nMessage Language:\t"+msglang+"\nChannel:\t\t"+channel+"\n")
	if retval:
		if dest == d.POLLY_GAME:
			return polly_request(phno,syslang,msglang,channel,d.POLLY_GAME_ICCID,d.polly_game_ip,return_request)
		elif dest == d.POLLY_BROWSE:
			return polly_request(phno,syslang,msglang,channel,d.POLLY_BROWSE_ICCID,d.polly_browse_ip,return_request)
	
	else:
		if dest == d.POLLY_GAME:
			spin_register_process(phno,syslang,msglang,channel,d.POLLY_GAME_ICCID,d.polly_game_ip,return_request)
		if dest == d.POLLY_BROWSE:
			spin_register_process(phno,syslang,msglang,channel,d.POLLY_BROWSE_ICCID,d.polly_browse_ip,return_request)
			
			
			
if __name__ == '__main__':
	result = polly_request("0019543679247", "AmerEnglish", "AmerEnglish", "NotTheDongle", d.POLLY_BROWSE_ICCID, d.polly_browse_ip, return_request=True)
	print(result)
