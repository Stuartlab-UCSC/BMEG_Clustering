#! /usr/bin/env python3
#Name: Ioannis Nikolaos Anastopoulos

import BMEG_pb2
import sys
from google.protobuf.json_format import MessageToJson
import json


"""CommandLine class to import args from commandline."""
class CommandLine() :

	def __init__(self, inOpts=None) :
		import argparse

		self.parser = argparse.ArgumentParser("This program accepts metadata file input, cluster files, and outpout file, and writes a JSON message")
		'''First argument is metadatafile.'''
		self.parser.add_argument('-metadataFile', '--metadata_file')
		'''Second argument is the clusterfile'''
		self.parser.add_argument('-clusterFile', '--clusters_file')
		'''Third argument is the output file'''
		self.parser.add_argument('-outputFile', '--output_file', default='JSONmessage.txt')


		if inOpts is None :
			self.args = self.parser.parse_args()
		else :
			self.args = self.parser.parse_args(inOpts)

class writeMessage():

	def __init__(self):
		self.clusterFile_dict = {}
		self.metadataFile_dict = {}

	def clusterFileParser(self, clusterdata):
		with open(clusterdata) as fn:
			lines = (fn.readlines())

			#list of tuples of (cluster, sample_ID)
			cluster_list = list()
			for k in lines[1:]: #excluding headers
				end = k.find('\t')+1 #index of last sample_ID char

				sample = (k[0:end]).rstrip() #substring of sample_ID
				cluster_id = (k[end:]).rstrip() #substring of cluster_ID
				cluster_list.append((cluster_id, sample)) #creating list of tuples(cluster_ID, sample_ID)

			#iterating throught the tuples
			for cluster, sample in cluster_list:
				try:
					check = self.clusterFile_dict[cluster] #checking if cluster_ID in dict
				except:
					self.clusterFile_dict[cluster] = [] #creating list as a value for each cluster_ID
				self.clusterFile_dict[cluster].append(sample) #appending sample_IDs for each cluster_IDa

	def metadataFileParser(self, metadata):
		with open(metadata) as fn:
			lines = (fn.readlines())

			for line in lines:
				end = line.find('\t')+1


				key = line[0:end].rstrip()
				value = line[end:].rstrip()


				key = line[0:end].rstrip() #key is the label of each line
				value = line[end:].rstrip() #value is the description provided for the key
				#building dicitionary
				self.metadataFile_dict[key]=value


	def AddData(self, data):
		#Adding PanCancerAtlas
		for k,v in self.metadataFile_dict.items():
			if k == 'clustering_name':
				data.name =v

			#Adding metadata
			if k == 'method_description':
				data.metadata.description = v
			if k == 'method_parameters_JSON':
				# check valid json
				paramsDict = json.loads(str(v))
				data.metadata.clustering_method_parameters_JSON = json.dumps(paramsDict)

			if k == 'method_input_datatypes_JSON':
				datatypes = json.loads(str(v))
				for datatype in datatypes:
					data.metadata.clustering_method_input_datatypes.append(datatype)

			if k =='method_name':
				data.metadata.clustering_method = v
			if k == 'cluster_member_type':
				data.metadata.member_type = v


			for k,v in self.clusterFile_dict.items():
				group = data.groups.add()
				group.name = k
				group.members.extend(v)


		#change to JSON format
		# MessageToJson does not have option to output compact JSON !!!
		strJson = MessageToJson(data)
		objJson = json.loads(strJson)
		strJson = json.dumps(objJson, separators=(',', ':'))
		return strJson

def main():
	command_line = CommandLine()
	#clustering file from command line
	cluster_fn = command_line.args.clusters_file
	#metadata file from command line
	metadata_fn = command_line.args.metadata_file

	#MAIN PROCEDURE - writing message
	cluster_data = BMEG_pb2.BMEG_Clustering()

	#calling methods from writeMessage class
	res = writeMessage()
	res.clusterFileParser(cluster_fn)
	res.metadataFileParser(metadata_fn)
	# res.AddData(cluster_data)

	if len(sys.argv) != 5:
		print("Usage:", sys.argv[0], "REQUIRED: -clusterFile -metadaFile, OPTIONAL: -outputFile")
		sys.exit(-1)
	else:
		#Writing message to output file
		with open(command_line.args.output_file, "w") as f:
			strJson = res.AddData(cluster_data)
			f.write("%s\n" % (strJson))

if __name__ == "__main__":
	main()
