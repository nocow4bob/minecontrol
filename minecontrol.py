#! /usr/bin/env python

# This python program was designed to maintain my mining rig utilizing cudaminer. It will check
#  to see if the miner is running and if not, start up the new cudaminer process.

import httplib
import urllib2
import sys
import base64
import argparse
import threading
import Queue
import subprocess
import psutil
import time
from time import localtime, strftime
from ConfigParser import SafeConfigParser

# kill any cudaminer processes that are currently running
def killCuda():
	killed = False
	PROCNAME = "cudaminer"
	for proc in psutil.process_iter():
		try:
        		pinfo = proc.as_dict(attrs=['pid', 'name'])
    		except psutil.NoSuchProcess:
        		pass
    		else:
        		if pinfo['name'] == PROCNAME:
				p = psutil.Process(pinfo['pid'])
				p.kill()
				killed = True
	return killed	
	

# Check if cudaminer is running
def checkCuda():
	running = False
	PROCNAME = "cudaminer"
	for proc in psutil.process_iter():
        	try:
                	pinfo = proc.as_dict(attrs=['pid', 'name'])
        	except psutil.NoSuchProcess:
                	pass
                else:
                        if pinfo['name'] == PROCNAME:
                                running = True
	return running



# Main function
def main(config,pool):
	outfile = open('/home/miner/mining/miner.log','a')
	outfile.write("\n[*] Running minecontrol.py at %s\n" % (strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())))
	
	# kill all cuda processes running before continuing
	outfile.write("[*] Killing cudaminer processes: %s\n" % str(killCuda()))
	
	if pool:
		print "[D] Manual pool set: " + pool
	else:
		print "[D] Using config to pull pool data: " + config
		cp = SafeConfigParser()
        	cp.optionxform = str # Preserves case sensitivity
        	cp.readfp(open(config, 'r'))
		main_section = 'Main'
                gpu_split = int(cp.get(main_section,'gpu_split'))
                if gpu_split == 0:
                        print "[D] Hash split = 100% (or ZERO split)"
                elif gpu_split == 1:
                        print "[D] Hash split = 50/50"
                else:
                        print "[D] Hash split = unknown (using 100%)"
        	
		# Primary pool config
		primary_section = 'Primary'
        	primary_name = cp.get(primary_section,'name')
		primary_pool = cp.get(primary_section,'pool')
        	primary_port = cp.get(primary_section,'port')
		primary_worker = cp.get(primary_section,'worker')
		pri_worker_pw = cp.get(primary_section,'password')
		primary_connection = "stratum+tcp://%s:%s" % (primary_pool,primary_port)	

		# Secondary pool config
		secondary_section = 'Secondary'
                secondary_name = cp.get(secondary_section,'name')
                secondary_pool = cp.get(secondary_section,'pool')
                secondary_port = cp.get(secondary_section,'port')
		secondary_worker = cp.get(secondary_section,'worker')
                sec_worker_pw = cp.get(secondary_section,'password')
		secondary_connection = "stratum+tcp://%s:%s" % (secondary_pool,secondary_port)
	
		# Tertiary pool config
                tert_section = 'Tertiary'
                tert_name = cp.get(tert_section,'name')
                tert_pool = cp.get(tert_section,'pool')
                worker_name = cp.get(tert_section,'worker')
                worker_pw = cp.get(tert_section,'password')
		
		# Start the cudaminer process
		if gpu_split == 0:
			while True:
				if not checkCuda():
					outfile.write(" [*] Cudaminer starting at ZERO split\n")
					subprocess.Popen(["cudaminer", "-S", "-o", primary_connection,"-u", primary_worker, "-p", pri_worker_pw], stdout=subprocess.PIPE)
				else:
					time.sleep(10)
		elif gpu_split == 1:
			while True:
				if not checkCuda():
					outfile.write(" [*] Cudaminer starting at 50/50 split\n")
					subprocess.Popen(["cudaminer", "-S", "-d0", "-o", primary_connection,"-u", primary_worker, "-p", pri_worker_pw], stdout=subprocess.PIPE)
					subprocess.Popen(["cudaminer", "-S", "-d1", "-o", secondary_connection,"-u", secondary_worker, "-p", sec_worker_pw], stdout=subprocess.PIPE)			
				else:
					#outfile.write("[D] Cuda already running...\n")
					time.sleep(10)
		else: 
			outfile.write(" [X] No split found. Cudaminer not started\n")

# Start here
if __name__ == "__main__":
	pool = ""
        config = '/home/miner/mining/minecontrol/conf/mining.conf'
	parser = argparse.ArgumentParser(version="1.0",description="A cudaminer healthcheck and management script.")
        parser.add_argument('-p', help='Pool name', metavar='POOL',dest='pool')
        parser.add_argument('-c', help='Config file with pool lists; default: mining.conf', metavar='CONFIG',dest='config')
        args = parser.parse_args()
        if args.pool:
		pool = args.pool
	if args.config:
		config = args.config
	main(config, pool)
