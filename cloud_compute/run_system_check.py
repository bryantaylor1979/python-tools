# TODO: Try polling so you can get other tasks running quicker
# TODO: Try polling so you can add a time out
# TODO: Add AWS node
# TODO: Add cambridge laptop as a node. 
# TODO: Get the upbeat machine running in kinross. 
# TODO: try using stdin to keep ssh open a write more commands. e.g proc.stdin.write('%d\n' % i) look at the repeater script http://pymotw.com/2/subprocess/

# create nodes
import run_slave_command as configured_node
from collections import namedtuple

# Define class
NodeList = [];
ProcessList = [];
ErrorCodeList = [];
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

if __name__ == "__main__":
   for node in NodeList:
      process = run_slave_node(node)
      ProcessList.append(process)

   # wait for nodes to finish
   for single_process in ProcessList:
      	error_code = single_process.wait();
      	out, err = single_process.communicate();
      	#print "std out: "+out
   	if error_code == 0: 
      		print out.replace("\r\n", "")+": Success"
   	else:
      		print out.replace("\r\n", "")+": Failed"

#retcode = p.poll()
#if retcode is not None:
   # process has terminated
