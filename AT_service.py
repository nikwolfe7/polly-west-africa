import time
import traceback
from AT import AT
from remote_monitor import tropo_remote_sms
from common import echo,csvecho,prefix
import defines as d

# ====================================================== #
# These are some helpful implemented AT command/response funcs...
# ====================================================== #
# check OK
def send_ok(AT):
	return AT.send_at(d.CHECK_OK)
	
# ====================================================== #
# Initialize device for voice calls
def init_for_voice(AT):
	echo(prefix(AT.com) + "Initializing "+AT.com+" for voice calls...")
	reset(AT)
	AT.send_at(d.SHOW_OUTPUT)
	AT.send_at(d.ENABLE_EXTENDED_FORMAT)
	AT.send_at(d.ENABLE_CALL_LINE_ID)
	AT.send_at(d.DISABLE_AUTO_ANSWER)
	AT.send_at(d.DISABLE_PERIODIC_STATUS_MESSAGES)

# ====================================================== #
# resets the AT device	
def reset(AT):
	AT.send_at(d.RESET)
	
# ====================================================== #	
# ask for the device SIM number
def get_sim_number(AT):
	return AT.send_at(d.ASK_SIM_NUMBER)
	
# ====================================================== #	
# makes a call to a specified number	
def call(AT,phone_number):
	AT.send_at(d.DIAL+phone_number+";")

# ====================================================== #	
# hangs up an incoming call
def hang_up(AT):
	hangups = [d.HANG_UP_0,d.HANG_UP_1,d.HANG_UP_2,d.HANG_UP_3,d.HANG_UP_4]
	for hangup in hangups:
		echo(prefix(AT.com) + "Trying: " + hangup)
		response = AT.send_at(hangup)[0]
		echo(prefix(AT.com) + "Response: "+response)
		send_ok(AT)
		time.sleep(1)
		if d.CALL_END_SIGNAL in response:
			echo("Call terminated!")
			return True
	echo(prefix(AT.com) + "\nCould not terminate call using any known AT commands...\nGoogle Voice and Skype are known to have this problem. \nIs the caller using a VOIP service?\n\nAttempting to restart connection...")
	AT.close_connection()
	send_ok(AT)
	return False

# ====================================================== #
# send an SMS, return to voice mode afterwards
def send_sms(AT,recipient,message,from_dongle=False):
	try:
		tropo_remote_sms(recipient,message)
	except Exception as e: 
		echo(prefix(AT.com) + "An Exception occurred while sending SMS!\n" + str(e))
		echo(prefix(AT.com) +  traceback.format_exc())
		echo(prefix(AT.com) + "Attempting to send regular SMS through dongle...\n")
		time.sleep(d.sms_wait_time)
		send_ok(AT)
		send_ok(AT)
		AT.clear_buffers()
		echo(prefix(AT.com) + "Initializing "+AT.com+" for SMS...")
		AT.send_at(d.HIDE_OUTPUT, log=True)
		AT.send_at(d.ENABLE_SMS_MODE, log=True)
		AT.send_at(d.DEFINE_SMS_RECIPIENT + '"' + recipient + '"', log=True)
		AT.send_at(message, log=True)
		AT.phone.write(bytes([26]))
		time.sleep(d.sms_wait_time)
		echo(prefix(AT.com) + "SMS sent! All clear!")
		send_ok(AT)
		send_ok(AT)
		init_for_voice(AT)
		send_ok(AT)
		
	if from_dongle:
		echo(prefix(AT.com) + "Attempting to send regular SMS through dongle...\n")
		time.sleep(d.sms_wait_time)
		send_ok(AT)
		send_ok(AT)
		AT.clear_buffers()
		echo(prefix(AT.com) + "Initializing "+AT.com+" for SMS...")
		AT.send_at(d.HIDE_OUTPUT, log=True)
		AT.send_at(d.ENABLE_SMS_MODE, log=True)
		AT.send_at(d.DEFINE_SMS_RECIPIENT + '"' + recipient + '"', log=True)
		AT.send_at(message, log=True)
		AT.phone.write(bytes([26]))
		time.sleep(d.sms_wait_time)
		echo(prefix(AT.com) + "SMS sent! All clear!")
		send_ok(AT)
		send_ok(AT)
		init_for_voice(AT)
		send_ok(AT)

# ====================================================== #
# keep alive 
def keep_alive(AT):
	echo(prefix(AT.com) + "Sending keep-alive message to server...")
	dongle_alive = "0"
	diag = get_diagnostics(AT)
	if int(diag[0]) > 0: dongle_alive = "1"
	dongle_alive = [dongle_alive] + diag + [AT.com]
	csvecho(msg=dongle_alive, pre="ALIVE", retval=False)
		
# ====================================================== #
# PROCESS AT RESPONSES
# ====================================================== #
def check_matches_expected_response(at_response, delim, splitter):
	echo(delim + " Response: " + at_response)
	if delim in at_response:
		at = [a.strip() for a in at_response.split(splitter)]
		return (at, True)
	else: return ("",False)
	
# ====================================================== #
# Get diagnostic vector
def get_diagnostics(AT):
	rssi = get_rssi(AT)[0]
	carrier = get_carrier(AT)[0]
	state = get_device_state(AT)[0]
	return [rssi,carrier,state]

# ====================================================== #
# Extract the RSSI
def get_rssi(AT): 
	resp = AT.send_at(d.GET_SIGNAL_STRENGTH)[0]
	at = check_matches_expected_response(resp, d.RESP_GET_SIGNAL_STRENGTH, ":")
	if at[1]: 
		RSSI = at[0][-1].split(',')[0]
		echo("RSSI: "+RSSI)
		return (RSSI,True)
	else: return ("NO_RSSI",False)
	
# ====================================================== #
# Extract the Carrier name
def get_carrier(AT):
	AT.send_at(d.CARRIER_TEXT_DISPLAY, log=True)
	resp = AT.send_at(d.GET_CARRIER_NAME)[0]
	at = check_matches_expected_response(resp, d.CARRIER_RETURN, '"')
	if at[1]:
		carrier = at[0][1].strip()
		echo("CARRIER: "+carrier)
		return (carrier,True)
	else: return ("NO_CARRIER",False)
	
# ====================================================== #
# Extract the Device State
def get_device_state(AT):
	resp = AT.send_at(d.GET_DEVICE_STATE)[0]
	at = check_matches_expected_response(resp, d.DEVICE_STATE, ":")
	vals = ['READY','UNAVAILABLE','UNKNOWN','RINGING','CALL_IN_PROGRESS','ASLEEP']
	if at[1]:
		try:
			i = int(at[0][-1].replace('"','').split(',')[0].split('\n')[0])
			state = vals[i]
			echo("DEVICE STATE: " + state)
			return (state,True)
		except Exception:
			echo("Exception occurred! Call interrupted!")
			return (vals[4],True) # in case an incoming call comes while reading this...
	else: return (vals[2],False)

# ====================================================== #
# Extract the ICCID / APPLICATION
def get_application(AT):
	resp = AT.send_at(d.GET_ICCID)[0]
	at = check_matches_expected_response(resp, d.ICCID, ":")
	app = d.POLLY_GAME
	if at[1]:
		iccid = at[0][-1].split("\n")[0].strip()
		echo("ICCID: " + iccid)
		if iccid == d.POLLY_GAME_ICCID:
			app = d.POLLY_GAME
		elif iccid == d.POLLY_BROWSE_ICCID:
			app = d.POLLY_BROWSE
		echo("APPLICATION: "+app)
		return (app,True)
	else: return (app,False)

# ====================================================== #	
def check_at_response_is_incoming_call(at_response):
	at = check_matches_expected_response(at_response, d.CALL_ID, '"')
	if at[1]:
		echo("\n========================="
			"\nOh Boy! An Incoming Call!"
			"\n=========================\n")
		phone_num = at[0][1].strip()
		if len(phone_num):
			echo("Incoming Phone Number is : "+phone_num)
		else:
			echo("Looks like a Skype call. Number is blank.")
			phone_num = d.skype
		return (phone_num, True)
	else: return at

# ====================================================== #	
# checks if the AT string is the response to a AT+CNUM command...	
def extract_phone_number(at_response):
	at = check_matches_expected_response(at_response, d.ASK_SIM_NUMBER, d.ASK_SIM_NUMBER)
	if at[1]:
		nums = ("",)
		flag = False
		for num in at[0]:
			for n in num.split(","):
				n = n.strip('"+')
				# cuz phone numbers are 7 or more digits...
				if n.isdigit() and len(n) >= 7: 
					nums = ()
					flag = True
					nums += (n.strip('"+'),)
		if flag: return nums + (flag,)
		elif check_ok(at[0]): return (d.no_num, True)
		else: return at 
	else: return at
	
# ====================================================== #		
# makes sure AT response was OK
def check_ok(at_response):
	return "OK" in at_response