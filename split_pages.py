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


'''
data = []

folder = "./data"

for filename in os.listdir(folder):
	f = open(folder+ '/' + filename , 'rb')
	csvReader = csv.DictReader(f)

	h_264_mimeType = 'H_264'
	h_265_mimeType = 'H_265'

	connection = pm.MongoClient("mongodb://localhost:27017")
	db = connection.testDB
	codecConnection = db.codec

	count = 0

	for row in csvReader:
		data.append(row) 

  		#Codec Capability of json
		index = row['body'].find(',')
		org_str = row['body']
		#fix body msg to json format
		codec_capa = '{' + org_str[index+1:] +'}'

		codec_json = json.loads(codec_capa)

		h_264_decoderInfoList = []
		h_265_decoderInfoList = []
		h_264_decoderInfoJson = {}
		h_265_decoderInfoJson = {}

		full_json = {}
		full_json["deviceModel"] = row['DeviceModel']
		full_json["carrier"] = row['Carrier']
		full_json["osv"] = row['Platform']

		deviceModel = row['DeviceModel']
		carrier = row['Carrier']
		osv = row['Platform']

		print(deviceModel)

		for name, mimeType in codec_json.items():
			if mimeType == h_264_mimeType:
				decoderName = name[:name.find('_'+ h_264_mimeType)]
				h_264_dict = {}
				h_264_dict["decoder"] = decoderName
				h_264_dict["capabilities"] =  codec_json["profileLevels_" + decoderName]
				h_264_decoderInfoList.append(h_264_dict)
			elif mimeType == h_265_mimeType:
				decoderName = name[:name.find('_'+ h_265_mimeType)]
				h_265_dict = {}
				h_265_dict["decoder"] = decoderName
				h_265_dict["capabilities"] =  codec_json["profileLevels_" + decoderName]
				h_265_decoderInfoList.append(h_265_dict)

		print(count)
		h_264_decoderInfoJson["h264"] = h_264_decoderInfoList
		h_265_decoderInfoJson["h265"] = h_265_decoderInfoList
		codecList = [h_264_decoderInfoJson, h_265_decoderInfoJson]

		full_json["codec"] = codecList
		try: 
			if codecConnection.find({'deviceModel': deviceModel, 'osv' : osv}).count() > 0 :
				print("found")
			else :
				codecConnection.insert(full_json)
		except: 
			print("insert failed!", sys.exc_info()[0])
		count += 1
'''
