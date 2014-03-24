import psutil

# kill any cudaminer processes that are currently running
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
                                		#p.kill()
						killed = True
        return killed
