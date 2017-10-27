import csv
import json
import os.path
import sys, getopt
import subprocess
import shutil

def main(argv):
  inputfile = ''
  jsonfile = ''
  try:
    opts, args = getopt.getopt(argv,"hi:j:",["ifile=","jfile="])
  except getopt.GetoptError:
    print 'split_pages.py -i <inputfile> -j <json>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'split_pages.py -i <inputfile> -j <js>'
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-j", "--jfile"):
      jsonfile = arg
  print 'Input file is "', inputfile
  print 'json file is "', jsonfile 

  paths = '/tmp/pages'
  if os.path.isdir(paths) :
    shutil.rmtree(paths)
  print 'not found'
  os.mkdir( paths, 0755 );

  targetFilesList = []

  with open(jsonfile, 'rb') as data_file:    
    data = json.load(data_file)
    pageList = data['pageList']
    count = 1
    for page in pageList :
      startTime = page['start']
      duration = page['duration']
      print 'startTime ', startTime, ' duration ', duration
      targetFile = paths + '/page' + str(count) + '.mp4'
      subprocess.call('ffmpeg -v error -y -ss ' +  str(startTime) + ' -i ' + inputfile +
          ' -t ' + str(duration) + ' -acodec copy -vcodec copy ' + targetFile, shell=True)
      targetFilesList.append(targetFile)
      count += 1
  strTargetFileList = ''
  for pageFile in targetFilesList:
    strTargetFileList += ' ' + pageFile
  subprocess.call('./merge_fade.sh -o fade_output.mp4' + strTargetFileList, shell=True)

if __name__ == "__main__":
  main(sys.argv[1:])
