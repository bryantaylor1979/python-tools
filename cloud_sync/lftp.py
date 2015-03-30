import subprocess 
import os
import time
import argparse

# Variables
disable_sub_folder = False
folder_name = 'Shared Videos' # 'Shared Videos' | 'SelfBuild' | 'Shared Music' | 'Backup'
ftp_server = 'cambslogic.com'
ftp_user = 'bryan'
ftp_pass = 'tango224'
protocol = 'ftp' # sftp or ftp
verbose_level = 0
mode = 'bi-directional' # reverse | mirror | bi-directional
dryrun = False
loop = False # will be force disable if dry-run is enabled as it may go into a continuous loop.

# You can play with values for --use-pget-n and/or -P to achieve maximum speed depending on the particular network.
use_pget_n = 3  #  transfer each file with 3 independent parallel TCP connections
filesinparallel = 2 # transfer 2 files in parallel (totalling 6 TCP connections)

# should make it run a little quicker by dismissing file not required for sync.
exclude = ['.svn/','.shareport/']


# will be force disable if dry-run is enabled as it may go into a continuous loop.
if dryrun == True:
  loop = False

def mirror(reverse_mirror,args):
  # Main Code
  t = time.time()
  if args.disable_sub_folder == False:
     dest_folder_on_ftp_server = os.path.join('/mnt/cambs_cloud',args.folder_name)
     src_local_folder = os.path.join('/Public',args.folder_name)
  else:
     dest_folder_on_ftp_server = '/mnt/cambs_cloud'
     src_local_folder = '/Public'


  if reverse_mirror == True:
     r_string = ' -R'
     src = dest_folder_on_ftp_server
     dest_folder_on_ftp_server = src_local_folder
     src_local_folder = src
  else:
     r_string = ''
  
  # verbose string
  if args.verbose_level == 0:
     verbose_string = ' -v'
  else: 
     verbose_string = ' --verbose='+str(args.verbose_level)

  exclude_string = ''
  for string in exclude: 
     exclude_string = exclude_string+' --exclude-glob '+string

  # dry run string
  if args.dryrun == True:
     dryrun_string = '  --dry-run'
  else:
     dryrun_string = ''

  if args.loop == True:
     loop_string = ' --loop'
  else: 
     loop_string = ''

  string = 'lftp '+protocol+'://'+ftp_user+':'+ftp_pass+'@'+ftp_server+' -e "mirror '+exclude_string+verbose_string+r_string+dryrun_string+' --parallel='+str(filesinparallel)+' --use-pget-n='+str(use_pget_n)+' -c'+loop_string+' --only-newer --ignore-time '+"'"+src_local_folder+"'"+' '+"'"+dest_folder_on_ftp_server+"'"+' ; quit"'

  print string
  subprocess.call(string, shell=True)

  elapsed = time.time() - t
  print elapsed

def parseinputs():
  folder_name_choices =  ['Shared Videos', 'SelfBuild', 'Shared Music', 'Backup', 'Shared Pictures']
  parser = argparse.ArgumentParser(description='variables')
  parser.add_argument( '-f','--folder_name', 
                       default=folder_name, type=str, 
                       choices=folder_name_choices,
                       help='folder name to be syncronised')
  parser.add_argument( '-e','--disable_sub_folder',
                       default=disable_sub_folder, action='store_true', 
                       help='disable to sync everything in one shot')
  parser.add_argument( '-s','--ftp_server',
                       default=ftp_server, type=str, 
                       help='url address of remote ftp server')
  parser.add_argument( '-u','--ftp_user',
                       default=ftp_user, type=str, 
                       help='username for ftp login')
  parser.add_argument( '-p','--ftp_pass',
                       default=ftp_pass, type=str, 
                       help='password for ftp login')
  parser.add_argument( '-c','--protocol',
                       default=protocol, type=str, 
                       help='password for ftp login')
  parser.add_argument( '-v','--verbose_level',
                       default=verbose_level, type=int, 
                       help='verbose logging level')
  parser.add_argument( '-m','--mode',
                       default=mode, type=str, 
                       help='mode reverse/mirror/bi-direction')
  parser.add_argument( '-d','--dryrun',
                       default=dryrun, action='store_true',
                       help='will not transfer any files but will have logging as if it was trying')
  parser.add_argument( '-l','--loop',
                       default=loop, action='store_true',
                       help='ill be force disable if dry-run is enabled as it may go into a continuous loop.')
  parser.add_argument( '-t','--use_pget_n',
                       default=use_pget_n, type=int, 
                       help='transfer each file with 3 independent parallel TCP connections')
  parser.add_argument( '-i','--filesinparallel',
                       default=filesinparallel, type=int, 
                       help='transfer 2 files in parallel (totalling 6 TCP connections)')
  args = parser.parse_args()
  return args

def run():
  args = parseinputs()
  if args.mode == 'reverse':
     mirror(True,args)
  elif args.mode == 'mirror':
     mirror(False,args)
  else: # bi-directional
     print "mirror"
     mirror(False,args)
     print "reverse-mirror"
     mirror(True,args)

if __name__ == "__main__":
  run()


