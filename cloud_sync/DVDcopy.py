import subprocess 
import os
import time
import argparse
import shutil

temp_dir = '/home/local/ANT/bryantay/DVD_Temp/'
local_share = '/home/local/ANT/bryantay/Videos/'
network_share = '/mnt/cambs_cloud/Shared Videos/Copied DVD/'

# Variables
disable_sub_folder = False

def MakeDir(dir_in):
  try:
      os.stat(dir_in)
  except:
      os.mkdir(dir_in) 

def vodcopy(temp_dir):
  subprocess.call(['vobcopy -l -o '+temp_dir+' -m'], shell=True)

def compress(input_path,output_file):
  command = 'HandBrakeCLI -i '+input_path+' -o '+output_file+' -e x264 -q 20 -B 160 -t 1'
  print command
  subprocess.call(command,shell=True)

def parseinputs():
  parser = argparse.ArgumentParser(description='variables')
  parser.add_argument( '-f','--folder_name', 
                       default=folder_name, type=str, 
                       help='folder name to be syncronised')
  args = parser.parse_args()
  return args

def run():
  args = parseinputs()

def getDVDname(temp_dir):
  names = os.listdir(temp_dir)
  if len(names) == 0:
     name = names[0]
  else:
     name = names[len(names)-1]
  return name

def copyfile2share(source,destination):
  print 'copying '+source+' to '+destination
  print 'please wait'
  shutil.copyfile(source, destination)

if __name__ == "__main__":
  try:
      shutil.rmtree(temp_dir)
  except:
      print "dir already removed"
  MakeDir(temp_dir)
  vodcopy(temp_dir)
  title = getDVDname(temp_dir)
  print "The Title is Called: "+title
  
  # COMPRESS
  input_path = os.path.join(temp_dir,title,'VIDEO_TS')
  output_file = os.path.join(temp_dir,title+'.mp4')
  compress(input_path ,output_file)

  # COPY FILES TO LOCATIONS
  copyfile2share(output_file,os.path.join(local_share,title+'.mp4'))
  copyfile2share(output_file,os.path.join(network_share,title+'.mp4'))
  shutil.rmtree(temp_dir)


