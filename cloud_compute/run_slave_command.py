import subprocess 
import os
import time

# Variables
hostname = 'bryant-HP-Compaq-2510p-Notebook-PC'
EnableForwarding = True
password = "tango224"
username = "bryant"
server = "cambslogic.com"
host = "192.168.0.17"
command = "hostname1"

def run():
  if EnableForwarding == True: 
     string = "sshpass -p "+password+" ssh -t "+username+"@"+server+" -C 'sshpass -p "+password+" ssh "+username+"@"+host+" "+command+"'"
  else: 
     string = "sshpass -p "+password+" ssh -t "+username+"@"+host+" -C '"+command+"'"
  print string
  # login through ssh
  process = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  return process

def runCmd(cmd, timeout=None):
    '''
    Will execute a command, read the output and return it back.

    @param cmd: command to execute
    @param timeout: process timeout in seconds
    @return: a tuple of three: first stdout, then stderr, then exit code
    @raise OSError: on missing command or if a timeout was reached
    '''

    ph_out = None # process output
    ph_err = None # stderr
    ph_ret = None # return code

    p = subprocess.Popen(cmd, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    # if timeout is not set wait for process to complete
    if not timeout:
        ph_ret = p.wait()
    else:
        fin_time = time.time() + timeout
        while p.poll() == None and fin_time > time.time():
            time.sleep(1)

        # if timeout reached, raise an exception
        if fin_time < time.time():

            # starting 2.6 subprocess has a kill() method which is preferable
            # p.kill()
            os.kill(p.pid, signal.SIGKILL)
            raise OSError("Process timeout has been reached")

        ph_ret = p.returncode


    ph_out, ph_err = p.communicate()

    return (ph_out, ph_err, ph_ret)
  
if __name__ == "__main__":
  process = run();
  error_code = process.wait();
  if error_code == 0: 
     print "Success"
  else:
     print "Failed"
     out, err = process.communicate()
     print "std out: "+out

