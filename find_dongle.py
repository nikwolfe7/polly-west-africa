import subprocess
import defines
from AT import AT
from AT_service import get_sim_number,extract_phone_number
from common import echo

# ====================================================== #	
def port_has_phone_number(port):
	echo("Examining port "+port+"...")
	at_mod = AT(port)
	number = get_sim_number(at_mod)
	if (number[1]):
		resp = extract_phone_number(number[0])
		if(resp[1]):
			echo("PORT "+port+" is valid!")
			echo("PHONE NUMBER: "+str(resp[0]))
			return True
		else: return False
	else:
		return False

# ====================================================== #	
def find_connected_dongle_ports():
	proc = subprocess.Popen([defines.cmd_root+defines.cmd_mode],stdout=subprocess.PIPE,shell=True)
	(out, err) = proc.communicate()
	out = out.decode('utf-8')
	ports = {}
	echo("Searching for COM ports...")
	echo(out)
	out = out.split("\n")
	for i in range(len(out)-1):
		line = out[i]
		if "COM" in line:
			com = line.split()[-1].strip(":")
			ports[com] = []
			while line.strip() != "":
				i += 1
				line = out[i]
				if ":" in line:
					l = [x.strip() for x in line.split(":")]
					ports[com].append((l[0],l[1]))
					
	# check that the ports point to SIM cards...
	valid_ports = {}
	for port in ports.keys():
		if port_has_phone_number(port):
			valid_ports[port] = ports[port]
	
	# return the ports map...		
	return valid_ports			
			
# ====================================================== #	
if __name__ == "__main__":
	ports = find_connected_dongle_ports()
