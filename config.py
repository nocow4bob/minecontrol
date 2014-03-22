#!/usr/bin/python

import sys
import argparse

# Get GPU information
def getGPU():
	gpu_count = raw_input("Number of GPU: ")
        gpu_split = raw_input("Hash split (0=NONE, 1=50/50): ")
	gpu_info = [gpu_count,gpu_split]
	return gpu_info

def getPoolInfo(num):
	pool_info = []
	while int(num) > 0:
		pool_name = raw_input("Pool name: ")
		pool_addr = raw_input("Pool address: ")
		pool_worker = raw_input("Pool worker name: ")
		pool_worker_pw = raw_input("Pool worker password: ")
		pool_info.append([pool_name,pool_addr,pool_worker,pool_worker_pw])
		num = int(num) - 1
	return pool_info

# print pool information
def printPoolInfo(pools):
	for pool in pools:
		print "Pool name: %s" % pool[0]
		print "Pool address: %s" % pool[1]
		print "Pool worker: %s" % pool[2]
		print "Pool worker pw: %s" % pool[3]
		print "----------------------"
		

def main(config):
	print "[*] Minecontrol config builder\n"
	gpu_info = getGPU()
	num = raw_input("How many pools to configure? ")
	pool_info = getPoolInfo(num)
	print "GPU Info"
	print "--------"
	for info in gpu_info:
		print info
	printPoolInfo(pool_info)	

# Start here
if __name__ == "__main__":
        pool = ""
        config = 'conf/mining.conf'
        parser = argparse.ArgumentParser(version="1.0",description="Minecontrol config builder")
        parser.add_argument('config', help='Config file with pool lists; default: conf/mining.conf', metavar='CONFIG')
        args = parser.parse_args()
        config = args.config
        main(config)
