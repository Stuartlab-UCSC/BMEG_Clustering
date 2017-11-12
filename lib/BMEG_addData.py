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
		'''Fourth argument is the Method  output file'''
		self.parser.add_argument('-outputMethodFile', '--output_method_file', default='JSONMethodMessage.txt')
		'''Fifth argument is the Cluster output file'''

		self.parser.add_argument('-outputClusterFile', '--output_clusters_file', default='JSONClustersMessage.txt')


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


	def MethodData(self, data):
		#Converting metadata JSON format for Method clustering was done
		for k,v in self.metadataFile_dict.items():
			if k == 'clustering_name':
				data.clustering_name =v

			if k == 'cluster_member_type':
				data.cluster_member_type = v

			if k =='method_name':
				data.method_name = v

			if k == 'method_description':
				data.method_description = v

			if k == 'method_parameters_JSON':
				# check valid json
				paramsDict = json.loads(str(v))
				data.clustering_method_parameters_JSON = json.dumps(paramsDict)

			if k == 'method_input_datatypes_JSON':
				datatypes = json.loads(str(v))
				for datatype in datatypes:
					data.clustering_method_input_datatypes.append(datatype)

		for k in self.clusterFile_dict:
			data.cluster_names.append(k)
		
		#change to JSON format
		# MessageToJson does not have option to output compact JSON !!!
		strJson = MessageToJson(data)
		objJson = json.loads(strJson)
		strJson = json.dumps(objJson, separators=(',', ':'))
		return strJson

	def ClusterData(self, data, clusterName, samples):
		for k,v in self.metadataFile_dict.items():
			if k =='method_name':
				data.method_name = v

		data.cluster_name = clusterName
		data.samples.extend(samples)

		#change to JSON format
		# MessageToJson does not have option to output compact JSON !!!
		strJson = MessageToJson(data)
		objJson = json.loads(strJson)
		strJson = json.dumps(objJson, separators=(',', ':'))
		return strJson



def main():
	command_line = CommandLine()
	#clustering file from command line - clustering file, can be either cluster samples, of genes in gene panels
	cluster_fn = command_line.args.clusters_file
	#metadata file from command line
	metadata_fn = command_line.args.metadata_file

	#MAIN PROCEDURE - writing message
	method_data = BMEG_pb2.Method() #information about clustering method used
	cluster_data = BMEG_pb2.Cluster() #members in the cluster beloging in Method


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
		with open(command_line.args.output_method_file, "w") as f:
			strJson = res.MethodData(method_data)
			f.write("%s\n" % (strJson))
		with open(command_line.args.output_clusters_file, "w") as f:
			for k,v in res.clusterFile_dict.items():
				strJson = res.ClusterData(cluster_data, k, v)
				f.write("%s\n" % (strJson))

if __name__ == "__main__":
	main()
