from common import echo
import defines

def is_phone_number(phno):
	return phno.strip("+").isdigit() and len(phno) >= 7

def process_for_guinea(phno):
	if is_phone_number(phno):
		phno = phno.replace("+","")
		if phno.startswith(defines.usa_cc) or phno.startswith("1"):
			if phno.startswith("1"): phno = defines.usa_cc + phno.lstrip("1")
			echo("Looks like a U.S. number... Returning " + phno)
			return (phno, defines.eng)
		else:
			phno = defines.guinea_cc + phno.lstrip("0") # guinea local
			echo("Looks like a Guinea number... Returning " + phno)
			return (phno, defines.fr)
	else:
		echo("Could not process number.")
		return (phno, defines.eng)
		
