import defines as d
from common import echo
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
		
		else: echo("Delayed request successfully sent!")
		
# ====================================================== #	
if __name__ == "__main__":
	send_delayed_requests()