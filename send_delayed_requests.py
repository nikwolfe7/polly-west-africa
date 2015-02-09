import defines as d
from common import echo
import os

def main():
	delayed_reqs = ""
	if not os.path.isfile(d.log_dir + d.pending_reqs):
		delayed_reqs = open(d.log_dir + d.pending_reqs,"w")
	delayed_reqs = [l.strip() for l in open(d.log_dir + d.pending_reqs).readlines()]
	if delayed_reqs:
		echo("Attempting to send delayed requests...")
	
	
		


# ====================================================== #	
if __name__ == "__main__":
	main()