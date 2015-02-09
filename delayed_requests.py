import defines as d
from common import echo,csvecho
import os
from polly_reg import send_request

test_url = "http://128.2.208.191/wa/DBScripts/createMissedCall.php?ph=0019543679247&syslang=AmerEnglish&msglang=AmerEnglish&ch=GuinDongle&iccid=892246501005604963FF"

def send_delayed_requests():
	if not os.path.isfile(d.log_dir + d.pending_reqs):
		delayed_reqs = open(d.log_dir + d.pending_reqs,"w")
		#delayed_reqs.write(test_url+"\n")
		delayed_reqs.close()
	
	delayed_reqs = [l.strip() for l in open(d.log_dir + d.pending_reqs).readlines()]
	if not delayed_reqs:
		echo("Started up, found no delayed requests! All clear...")
		
	else: echo("Attempting to send delayed requests...")
		
	os.remove(d.log_dir + d.pending_reqs)
	
	for req in delayed_reqs:
		echo("Sending request: "+req)
		response = send_request(req)
		
		if "REGISTER_FAILED" in response:
			echo("Request failed again: "+req)
		
		else: 
			# call vector:
			# [rssi,carrier,state]+[request_id,com,phone_num,phno,lang,destination]
			echo("Delayed request successfully sent! Logging request...")
			
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
			csvecho(return_request)
						
					
			
			
			
		
# ====================================================== #	
if __name__ == "__main__":
	send_delayed_requests()