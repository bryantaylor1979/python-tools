import subprocess 
import os
import time

# Variables
EnableForwarding = True
password = "tango224"
username = "bryant"
server = "cambslogic.com"
host = "192.168.0.17"
command = "hostname"

def run():
  string = "sshpass -p "+password+" ssh -t "+username+"@"+server+" -C 'sshpass -p "+password+" ssh "+username+"@"+host+" "+command+"'"
  print string
  # login through ssh
  process = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
  return process
  
if __name__ == "__main__":
  process = run();
  print "Wait for process to end"
  process.wait();
  out, err = process.communicate()
  print "std out: "+out
  print "std error: "+err
  print "finish"
