# TODO: Add AWS node
# TODO: Add cambridge laptop as a node. 
# TODO: Get the upbeat machine running in kinross. 
# TODO: try using stdin to keep ssh open a write more commands. e.g proc.stdin.write('%d\n' % i) look at the repeater script http://pymotw.com/2/subprocess/

# create nodes
import run_slave_command as configured_node
from collections import namedtuple
from string import whitespace
import time
import os

# Define class
NodeList = [];
ProcessList = [];
ErrorCodeList = [];
count = 0;
params = namedtuple('params', [ 'hostname', 
                                'EnableForwarding',
			        'password', 
				'username', 
    				'server', 
				'host', 
				'command']);

# Vars
password = "tango224"
user = "bryant"
kinross_server = "cambslogic.com"
command = "hostname"

node  = params( hostname='bryant-HP-Compaq-2510p-Notebook-PC',
		EnableForwarding=True, 
 		password = password, 
		username = user, 
		server = kinross_server, 
		host = "192.168.0.17", 
		command = command);
NodeList.append(node);

node  = params( hostname='ubuntu',
		EnableForwarding=False, 
 		password = password, 
		username = user, 
		server = "", 
		host = kinross_server, 
		command = command);
NodeList.append(node);

def run_slave_node(nodedef):
   configured_node.hostname = nodedef.hostname
   configured_node.EnableForwarding = nodedef.EnableForwarding
   configured_node.password = nodedef.password
   configured_node.username = nodedef.username
   configured_node.server = nodedef.server
   configured_node.host = nodedef.host
   configured_node.command = nodedef.command
   process = configured_node.run();
   return process

def process_communicate(single_process):
   out, err = single_process.communicate();
   out=out.replace("\n\r", "")
   out=out.replace("\n",   "")
   out=out.replace("\r\n", "")
   return out, err


if __name__ == "__main__":
   for node in NodeList:
      process = run_slave_node(node)
      ProcessList.append(process)
   timeout = 10;
   tic = time.time()

   # wait for nodes to finish
   NumberOfProcesses = len(ProcessList)
   print "NumberOfProcesses: "+str(NumberOfProcesses)
   while True:
      for single_process in ProcessList:
          #error_code = single_process.wait();
          retcode = single_process.poll()
          time.sleep(1)
          if retcode is not None:
             # process has terminated
             count=count+1
             out, err = process_communicate(single_process);
             print "Computer Name: "+out
             if retcode == 0: 
	        print "Test Result: PASS\n\r"
             else:
                print "Test Result: FAIL\n\r"
          toc = time.time();
          time_elasped = toc-tic;
          if timeout < time_elasped:
	     print "Test Result: FAIL (timeout)\n\r"
             count=count+1
             try:
                single_process.kill();
             except:
                print "could not kill process"
          if count==NumberOfProcesses:
	     break
      if count==NumberOfProcesses:
          print "all tasks finished"
	  break
