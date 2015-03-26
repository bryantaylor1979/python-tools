import subprocess 
import os
import time

# Variables
enable_sub_folder = True
folder_name = 'Shared Videos' # 'Shared Videos' | 'SelfBuild' | 'Shared Music' | 'Backup' 
ftp_server = 'cambslogic.com'
ftp_user = 'bryan'
ftp_pass = 'tango224'
protocol = 'ftp' # sftp or ftp
verbose_level = 0
mode = 'bi-directional' # reverse | mirror | bi-directional
dryrun = False
loop = True # will be force disable if dry-run is enabled as it may go into a continuous loop.

# You can play with values for --use-pget-n and/or -P to achieve maximum speed depending on the particular network.
use_pget_n = 3  #  transfer each file with 3 independent parallel TCP connections
filesinparallel = 2 # transfer 2 files in parallel (totalling 6 TCP connections)


# will be force disable if dry-run is enabled as it may go into a continuous loop.
if dryrun == True:
  loop = False

def mirror(reverse_mirror):
  # Main Code
  t = time.time()
  if enable_sub_folder == True:
     dest_folder_on_ftp_server = os.path.join('/mnt/cambs_cloud',folder_name)
     src_local_folder = os.path.join('/Public',folder_name)
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
  if verbose_level == 0:
     verbose_string = '-v'
  else: 
     verbose_string = '--verbose='+str(verbose_level)

  # dry run string
  if dryrun == True:
     dryrun_string = '  --dry-run'
  else:
     dryrun_string = ''

  if loop == True:
     loop_string = ' --loop'
  else: 
     loop_string = ''

  string = 'lftp '+protocol+'://'+ftp_user+':'+ftp_pass+'@'+ftp_server+' -e "mirror '+verbose_string+r_string+dryrun_string+' --parallel='+str(filesinparallel)+' --use-pget-n='+str(use_pget_n)+' -c'+loop_string+' --only-newer --ignore-time '+"'"+src_local_folder+"'"+' '+"'"+dest_folder_on_ftp_server+"'"+' ; quit"'

  print string
  subprocess.call(string, shell=True)

  elapsed = time.time() - t
  print elapsed

def 
  parser = argparse.ArgumentParser(description='variables')
  parser.add_argument('--foldername', metavar='N', type=int, nargs='+',
                       help='an integer for the accumulator')
  parser.add_argument('--sum', dest='accumulate', action='store_const',
                       const=sum, default=max,
                       help='sum the integers (default: find the max)')

args = parser.parse_args()

def run():
  if mode == 'reverse':
     mirror(True)
  elif mode == 'mirror':
     mirror(False)
  else: # bi-directional
     print "mirror"
     mirror(False)
     print "reverse-mirror"
     mirror(True)

if __name__ == "__main__":
  run()


