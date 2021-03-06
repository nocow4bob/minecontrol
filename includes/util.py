import socket
import sys
import json
import urllib2
import tempfile
import os
import psutil
import logging
from ConfigParser import SafeConfigParser


# kill any cudaminer processes that are currently running matching the cmdline arguments given
def killCuda(instance):
        killed = False
        PROCNAME = "cudaminer"
        for proc in psutil.process_iter():
                try:
                        #pinfo = proc.as_dict(attrs=['pid', 'name'])
                        pinfo = proc.as_dict()
                except psutil.NoSuchProcess:
                        pass
                else:
                        if pinfo['name'] == PROCNAME:
                                for obj in pinfo['cmdline']:
                                        if instance in obj:
                                                p = psutil.Process(pinfo['pid'])
                                                p.kill()
                                                killed = True
        return killed


# check stratum connections
def checkStratum(address,port,worker,password):
        response = []
	MESSAGE = "{\"id\": 1, \"method\": \"mining.subscribe\", \"params\": [\"healthcheck\"]}\n"
	TCP_IP = address
	TCP_PORT = int(port)
	BUFFER_SIZE = 1024 
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))
	except Exception, e:
		print e
		return False
	
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	for line in data.splitlines():
		response.append(line)
	s.close()
	
	try:
		with tempfile.NamedTemporaryFile() as temp:
			temp.write(response[0])
			temp.flush()
			resp = json.load(open(temp.name))
			ans = resp.get('error')
			if not ans:
				temp.close()
				return True
			else:
				temp.close()
				return False
	except Exception, e:
		print e
		return False

# Check if cudaminer is running
def checkCuda(instance):
        PROCNAME = "cudaminer"
        for proc in psutil.process_iter():
                try:
                        #pinfo = proc.as_dict(attrs=['pid', 'name'])
			pinfo = proc.as_dict()
                except psutil.NoSuchProcess:
                        pass
                else:
        		if pinfo['name'] == PROCNAME:
                                for obj in pinfo['cmdline']:
                                        if instance in obj:
                                        	return True
	return False


# Get pool configuration
def getConfig(config):
	cp = SafeConfigParser()
        cp.optionxform = str # Preserves case sensitivity
        cp.readfp(open(config, 'r'))
        
	pools = []
	sections = ['Primary','Secondary','Tertiary','Other']
	
	main_section = 'Main'
        gpu_split = int(cp.get(main_section,'gpu_split'))
	pools.append([main_section,gpu_split])
	# Primary pool config
        for section in sections:
		try:	
			name = cp.get(section,'name')
        		pool = cp.get(section,'pool')
        		port = cp.get(section,'port')
        		worker = cp.get(section,'worker')
        		worker_pw = cp.get(section,'password')
        		connection = "stratum+tcp://%s:%s" % (pool,port)
			pools.append([section,name,pool,port,worker,worker_pw,connection])
		except Exception, e:
			print e
	
	return pools
