# coding=utf-8
import os
import socket
# ====================================================== #	
# logging / SMS stuff...
log_dir = "."+os.sep+"logs"+os.sep
logfile = "logfile"
logfile_full = "logfile-full"
exception_log = "exception_log"
pending_reqs = "pending_requests.txt"
pending_reqs_fulfilled = "pending_requests_fulfilled.txt"
remote_logging_backup_queue = "remote_log_backup_queue.txt"
reminder_list = "reminder_list.txt"
at_log = "AT-log"
sms_confirm = False
sms_alert_number = "0019543679247"
sms_backup_number = sms_alert_number
sms_alert_message = "Polly Dongle SOS! An Exception occurred! "
file_delim = ";"
tropo_request = "http://api.tropo.com/1.0/sessions?action=create&token=1950c84caa3aa1489428e3946049fdfa96c92736612b6abb738b004d0c8f12c253ae0bdec48ab3828dd1d89d&msg=[MESSAGE]&calltype=GuinDongleStatusSMS&ph=[RECIPIENT]&callerid=%2B14122677909"
tropo_recipient = "[RECIPIENT]"
tropo_message = "[MESSAGE]"
web_request_timeout = 60
socket.setdefaulttimeout(web_request_timeout)

# ====================================================== #	
# AT constants
wait_time = 0.25 # slower than this seems to screw things up
sms_wait_time = 5
refresh_rate = 0.1

# ====================================================== #	
# AT commands
CHECK_OK = "AT"
SHOW_OUTPUT = "ATE1V1"
HIDE_OUTPUT = "ATE0V0"
ENABLE_EXTENDED_FORMAT = "AT+CRC=1"
ENABLE_CALL_LINE_ID = "AT+CLIP=1"
DISABLE_AUTO_ANSWER = "ATS0=0"
DISABLE_PERIODIC_STATUS_MESSAGES = "AT^CURC=0"
RESET = "ATZ"
ASK_SIM_NUMBER = "AT+CNUM"
DIAL = "ATD"
HANG_UP_0 = "ATH"
HANG_UP_1 = "AT+CHUP"
HANG_UP_2 = "ATH0"
HANG_UP_3 = "AT+CHCCS"
HANG_UP_4 = "AT+CHLD"
CALL_ID = "+CRING"
ENABLE_SMS_MODE = "AT+CMGF=1"
DEFINE_SMS_RECIPIENT = "AT+CMGS="
CALL_END_SIGNAL = "^CEND:"
GET_SIGNAL_STRENGTH = "AT+CSQ"
RESP_GET_SIGNAL_STRENGTH = "+CSQ"
CARRIER_TEXT_DISPLAY = "AT+COPS=3,0"
CARRIER_TEXT_DISPLAY_2 = "AT+COPS=3,1"
CARRIER_TEXT_DISPLAY_3 = "AT+COPS=3,2"
GET_CARRIER_NAME = "AT+COPS?"
CARRIER_RETURN = "+COPS"
GET_DEVICE_STATE = "AT+CPAS"
DEVICE_STATE = "+CPAS"
GET_ICCID = "AT^ICCID?"
ICCID = "^ICCID"

# ====================================================== #	
# serial commands
cmd_root = "C:\\Windows\\System32\\"
cmd_mode = "mode.com"
baudrate = 115200

# ====================================================== #	
# Polly URL stuff...
app = "wa"
polly_game_ip = "128.2.208.191"
polly_browse_ip = "128.2.208.191"
script = "/DBScripts/createMissedCall.php?ph="
syslang_prefix = "&syslang="
msglang_prefix = "&msglang="
channel_prefix = "&ch="
iccid_prefix = "&iccid="
timeofreq_prefix = "&timeofreq="
channel = "GuinDongle"
POLLY_GAME = "polly_game"
POLLY_HEALTH = "polly_health"
POLLY_SPREAD = "polly_spread"
POLLY_BROWSE = "polly_browse"
REQUEST_PENDING = "REQUEST_PENDING"
REGISTER_FAILED = "REGISTER_FAILED"
REQUEST_SUCCESS = "SUCCESS"

# Remote monitor update
ip_optiplex = "128.2.211.183"
monitor_script = "/RemoteMonitor/dongleMontiorUpdate.php?update="

# ====================================================== #	
# phone number stuff...
skype = "SKYPE|BLANK"
no_num = "NO_NUMBER"
guinea_cc = "224"
usa_cc = "001"
eng = "AmerEnglish"
fr = "GuinFrench"
carrier_MTN = "MTN" # because they don't respond to COPS

# SIM card constants
POLLY_GAME_ICCID = "8922404111122610474F"
POLLY_BROWSE_ICCID = "892246501005604963FF"

# ====================================================== #	
testnum = "+19543679247"
game_got_your_call_fr = "Merci! Nous avons reçu votre l'appel! Polly vous rappellera sous peu."
game_got_your_call_eng = "Thanks! We received your flash! Polly will call you back shortly."
game_got_call_sms = {eng : game_got_your_call_eng , fr : game_got_your_call_fr}

health_got_your_call_fr = "Merci! Nous avons reçu votre l'appel! Polly Santé vous rappellera sous peu."
health_got_your_call_eng = "Thanks! We received your flash! Polly Health will call you back shortly."
health_got_call_sms = {eng : health_got_your_call_eng , fr : health_got_your_call_fr}

# access application SMS by keyword
got_call_sms = {POLLY_GAME : game_got_call_sms , POLLY_HEALTH : health_got_call_sms}
