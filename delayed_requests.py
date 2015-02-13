import defines as d
from common import echo,csvecho,is_number
import os
import time
from polly_reg import send_request

test_url = "http://128.2.208.191/wa/DBScripts/createMissedCall.php?ph=0019543679247&syslang=AmerEnglish&msglang=AmerEnglish&ch=GuinDongle&iccid=892246501005604963FF"

def send_delayed_requests():
	if not os.path.isfile(d.log_dir + d.pending_reqs):
		delayed_reqs = open(d.log_dir + d.pending_reqs,"w")
		delayed_reqs.write(test_url+"\n")
		delayed_reqs.close()
	
	delayed_reqs = [l.strip() for l in open(d.log_dir + d.pending_reqs).readlines()]
	if not delayed_reqs:
		echo("Started up, found no delayed requests! All clear...")
		
	else: echo("Attempting to send delayed requests...")
		
	requests_left = []
	
	for req in delayed_reqs:
		echo("Sending request: "+req)
		time.sleep(d.wait_time)
		response = send_request(req)
		
		if d.REGISTER_FAILED in response:
			echo("Request failed again: "+req)
			requests_left.append(req)
		
		elif d.REQUEST_PENDING in response or is_number(response): 
			# call vector:
			# [rssi,carrier,state]+[request_id,com,phone_num,phno,lang,destination]
			echo("Delayed request successfully sent! Logging request...")
			open(d.log_dir + d.pending_reqs_fulfilled, "a").write(req)
			
			# ------ HUGE HACK ----- #
			request = {}
			request["rssi"] = "0"
			request["carrier"] = "DELAYED"
			request["state"] = "DELAYED"
			request["request_id"] = response
			request["com"] = "COM?"
			req = req.split("?")[-1].split("&")
			for item in req:
				item = item.split("=")
				key = item[0]
				value = item[1]
				if key == "ph":
					request["phone_num"] = value
					request["phno"] = value
				elif key == "syslang":
					request["lang"] = value
				elif key == "iccid":
					if value == d.POLLY_BROWSE_ICCID:
						request["destination"] = d.POLLY_BROWSE
					else: request["destination"] = d.POLLY_GAME
			
			return_request = [request["request_id"],request["com"],request["phone_num"],\
							request["phno"],request["lang"],request["destination"],\
							request["rssi"],request["carrier"],request["state"]]
			
			# ------ END HUGE HACK ----- #
			# log the request!
			csvecho(return_request, retval=False)
			
		else: # Some other shit happened... log again
			echo("Cannot verify that request was successfully sent. Re-queueing the request...")
			requests_left.append(req)
			
	# all finished!
	if requests_left:
		for request_left in requests_left:
			open(d.log_dir + d.pending_reqs, "w").write(request_left + "\n")
			echo("Request is now back in " + d.log_dir + d.pending_reqs)
			
	else: # only if everything was successful... 
		os.remove(d.log_dir + d.pending_reqs)
				
				
# ====================================================== #	
if __name__ == "__main__":
	send_delayed_requests()