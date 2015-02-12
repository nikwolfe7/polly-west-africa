from multiprocessing import Process
import sys
import time
import traceback

from AT import AT
from AT_service import reset, init_for_voice, get_application, \
	check_at_response_is_incoming_call, hang_up, send_sms, get_diagnostics, \
	send_ok, keep_alive, check_ok
from common import echo, csvecho, prefix
import defines
from find_dongle import find_connected_dongle_ports
from polly_reg import polly_register
from process_number import process_for_guinea
from delayed_requests import send_delayed_requests


# ====================================================== #	
def listen_on_com_port(com):
	echo("\n" + prefix(com) + "\nProcess started... Listening on "+com+"...\n")
	at_module = AT(com)
	echo(prefix(com) + "Setting up dongle for voice calls...")
	reset(at_module)
	init_for_voice(at_module)
	echo(prefix(com) + "Waiting for a call from Godot... Nothing to be done...\n") 
	counter = 0;
	destination = get_application(at_module)[0]
	
	# INFINITE LOOP TIME
	while True:
	
		# ALGORITHM FOR POLLY DONGLE
		try:
			# 1.) Poll the Dongle
			at_response = at_module.poll()
			
			# 2.) Check that the response is not empty...
			if at_response.strip() != "":
			
				# 3.) If it's not empty, check if it's from incoming call
				resp = check_at_response_is_incoming_call(at_response)
				
				# 4.) If it's from an incoming call, process number
				if(resp[1]): 
				
					# 5.) Set language and country code 
					phone_num = resp[0]
					processed_phone_num = process_for_guinea(phone_num)
					phno = processed_phone_num[0]
					lang = processed_phone_num[1]
					
					# 6.) Hang up the call without answering
					echo(prefix(com) + "Hanging up call from " + phno + "...")
					if(hang_up(at_module)): echo(prefix(com) + "Hang up successful!")
					else: echo(prefix(com) + "Hang up unsuccessful! Trying to register caller anyway...")
					
					# 7.) Register this number for a callback from Polly
					request_id = "NONE"
					if not phno == defines.skype:
						# ------------------------------------------- #
						return_for_sms = False # hack!!! change if necessary...
						# ------------------------------------------- # 
						request_id = polly_register(phno, syslang=lang, msglang=lang, dest=destination, return_request=return_for_sms, retval=True)
						
						# huge hack!!!
						if return_for_sms:
							echo("Sending SMS to " + defines.sms_backup_number)
							echo("Request to send: " + request_id)
							send_sms(at_module, defines.sms_backup_number, request_id, from_dongle=True)
							echo("Waiting an extra 2 seconds for SMS to complete...")
							time.sleep(2)
						
					else: echo(prefix(com) + "Will not register this call due to blank number...")
					
					# 8.) text the caller to confirm
					if defines.sms_confirm and not phno == defines.skype:
						got_call_msg = defines.got_call_sms[destination][lang]
						echo(prefix(com) + "Texting caller: " + got_call_msg)
						send_sms(at_module, phno, got_call_msg)
						
					# 8a.) Remote Monitor... send update to CMU
					print("ID: "+str(request_id))
					call_vector = get_diagnostics(at_module)
					extras = [request_id,com,phone_num,phno,lang,destination]
					call_vector = extras + call_vector
					echo(prefix(com) + "Logging diagnostic vector...")
					csvecho(call_vector)
					
			# 9.) Delay a bit, check that dongle is still functioning, repeat
			time.sleep(defines.refresh_rate)
			counter += 1
			if counter % 1000 == 0:
				if counter >= 3000:
					counter = 0
					send_ok(at_module)
					keep_alive(at_module)
				check = send_ok(at_module)[0]
				if check_ok(check):
					# do NOT echo this to logging... 
					print(prefix(com) + "Yup. Still monitoring port "+com+" for incoming calls...")
				else:
					echo(prefix(com) + "Something seems to be wrong... Check OK returned: "+check)
			
		
		# 10.) If an exception occurs, say fuck it for now, keep going...
		# Also, send an alert SMS!
		except Exception as e: 
			echo(prefix(com) + "An Exception occurred!\n" + str(e))
			echo(prefix(com) +  traceback.format_exc())
			echo(defines.sms_alert_number + " " + defines.sms_alert_message)
			send_sms(at_module, defines.sms_alert_number, defines.sms_alert_message+str(e))
			echo(prefix(com) + "Moving on...")
			continue
			
		

# ====================================================== #	
if __name__ == "__main__":
	
	ports = find_connected_dongle_ports()
	
	# hack!!!
	#ports = {'COM17' : '115200'}
	
	if len(ports.keys()) < 1:
		echo("No detected COM ports. Try inserting/reinserting the dongle.")
		sys.exit(0)
	else:
		echo("We in business... There's COM ports here!")
	
	# Process queue
	Q = []
	
	# Process delayed requests
	dreqs = Process(target=send_delayed_requests)
	Q.append(dreqs)
	dreqs.start()
	
	# Spin processes off on the dongle ports
	for p in ports.keys():
		proc = Process(target=listen_on_com_port, args=(p,))
		Q.append(proc)
		proc.start()
	
	for proc in Q: proc.join()
	sys.exit(0)
	
	
	
	

