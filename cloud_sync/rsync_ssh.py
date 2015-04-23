#rsync --partial --progress --rsh=ssh bryant@cambslogic.com:"/mnt/kinners_cloud/Shared\ Software/matlab_install_unix.iso" ./matlab_install_unix.iso

import subprocess 
import os
import argparse

# Variables
folder_name = 'Shared Videos' # 'Shared Videos' | 'SelfBuild' | 'Shared Music' | 'Backup' | 'Shared Pictures'
ssh_server = 'cambslogic.com'
ssh_user = 'bryant'
ssh_pass = 'tango224'
verbose_level = 1
mode = 'bi-directional' # reverse | mirror | bi-directional

# should make it run a little quicker by dismissing file not required for sync.
exclude = ['.svn/','.shareport/','.*'] # .* tries to remove all hidden files


def rsync(args):
  folder_name_=folder_name.replace(' ','\ ')
  print folder_name_
  if verbose_level==0:
	verbose = ''
  else:
	verbose = ' -v'
  string = 'rsync --partial --ignore-existing --progress'+verbose+' --recursive --rsh=ssh '+ssh_user+'@'+ssh_server+':"/mnt/kinners_cloud/'+folder_name_+'/" /mnt/cambs_cloud/'+folder_name_+'/'
  print string
  subprocess.call(string, shell=True)

def parseinputs():
  folder_name_choices =  ['Shared Videos', 'SelfBuild', 'Shared Music', 'Backup', 'Shared Pictures']
  parser = argparse.ArgumentParser(description='variables')
  parser.add_argument( '-f','--folder_name', 
                       default=folder_name, type=str, 
                       choices=folder_name_choices,
                       help='folder name to be syncronised')
  parser.add_argument( '-s','--ssh_server',
                       default=ssh_server, type=str, 
                       help='url address of remote ftp server')
  parser.add_argument( '-u','--ssh_user',
                       default=ssh_user, type=str, 
                       help='username for ftp login')
  parser.add_argument( '-p','--ssh_pass',
                       default=ssh_pass, type=str, 
                       help='password for ftp login')
  parser.add_argument( '-v','--verbose_level',
                       default=verbose_level, type=int, 
                       help='verbose logging level')
  parser.add_argument( '-m','--mode',
                       default=mode, type=str, 
                       help='mode reverse/mirror/bi-direction')
  args = parser.parse_args()
  return args

def run():
  args = parseinputs()
  rsync(args)

if __name__ == "__main__":
  run()


