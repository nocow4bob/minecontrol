import socket
import sys
import json
import urllib2
import tempfile
import os
import psutil

# check stratum connections
def checkStratum(address,port,worker,password):
        MESSAGE = "{\"id\": 1, \"method\": \"mining.subscribe\", \"params\": [\"healthcheck\"]}"
	TCP_IP = address
	TCP_PORT = int(port)
	BUFFER_SIZE = 1024 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	f = tempfile.NamedTemporaryFile(delete=False)
	f.write(data)
	f.close()
	s.close()
	resp = json.load(open(f.name))
	os.unlink(f.name)
	ans = resp.get('error')
	if not ans:
		return True
	else:
		return False

# Check if cudaminer is running
def checkCuda():
        PROCNAME = "cudaminer"
        for proc in psutil.process_iter():
                try:
                        pinfo = proc.as_dict(attrs=['pid', 'name'])
                except psutil.NoSuchProcess:
                        pass
                else:
                        if pinfo['name'] == PROCNAME:
                                return True
        return False
