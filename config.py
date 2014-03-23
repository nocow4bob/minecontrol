#!/usr/bin/python

import sys
import argparse

# Get GPU information
def getGPU():
	try:
		gpu_count = int(raw_input("Number of GPU: "))
	except ValueError:
		print "[D] Not an integer"
		return
        try:
		gpu_split = int(raw_input("Hash split (0=NONE, 1=50/50): "))
	except ValueError:
		print "[D] Not an integer"
		return
	gpu_info = [gpu_count,gpu_split]
	return gpu_info

def getPoolInfo(pool_num):
	pool_info = []
	pool = 'Primary'
	while int(pool_num) > 0:
		print "\n[*] Get %s pool info" % pool
		pool_name = raw_input("Pool name: ")
		pool_addr = raw_input("Pool address (no port): ")
		pool_port = raw_input("Pool port: ")
		pool_worker = raw_input("Pool worker name: ")
		pool_worker_pw = raw_input("Pool worker password: ")
		pool_info.append([pool,pool_name,pool_addr,pool_port,pool_worker,pool_worker_pw])
		if pool == 'Primary':
			pool = 'Secondary'
		elif pool == 'Secondary':
			pool = 'Tertiary'
		elif pool == 'Tertiary':
			pool = 'Other'
		else:
			pool = 'Other'
		pool_num = int(pool_num) - 1
	return pool_info

# print pool information
def writePoolInfo(pools,conf_file):
	outfile = file(conf_file,'a+')
	for pool in pools:
		outfile.write("\n[%s]" % pool[0])
		outfile.write("\nname=%s" % pool[1])
		outfile.write("\npool=%s" % pool[2])
		outfile.write("\nport=%s" % pool[3])
		outfile.write("\nworker=%s" % pool[4])
		outfile.write("\npassword=%s\n" % pool[5])
	outfile.close()	
		
def writeGPUInfo(gpu_info,conf_file):
	outfile = file(conf_file, 'a+')
	outfile.write("[Main]\n")
	outfile.write("gpu_num=%s\n" % gpu_info[0])
	outfile.write("gpu_split=%s\n" % gpu_info[1])
	outfile.close()
	


def main(config):
	print "[*] Minecontrol config builder\n"
	config = 'conf/' + config
	config_file = open(config, 'w')
	config_file.close()
	gpu_info = getGPU()
	if gpu_info:
		writeGPUInfo(gpu_info,config)
		try:
			num = int(raw_input("How many pools to configure?[1-4] "))
		except ValueError:
			print "[D] Not an integer...bailing out"
			return	
		pool_info = getPoolInfo(num)
		writePoolInfo(pool_info,config)	
	else:
		print "[D] Input errors...bailing out"

# Start here
if __name__ == "__main__":
        pool = ""
        config = 'conf/mining.conf'
        parser = argparse.ArgumentParser(version="1.0",description="Minecontrol config builder")
        parser.add_argument('config', help='Config file to build (placed in conf dir); default: conf/mining.conf', metavar='CONFIG')
        args = parser.parse_args()
        config = args.config
        main(config)
