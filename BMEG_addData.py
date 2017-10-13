#! /usr/bin/env python3
#Name: Ioannis Anastopoulos

import BMEG_pb2
import sys
from google.protobuf.json_format import MessageToJson


"""CommandLine class to import args from commandline."""
class CommandLine() :

	def __init__(self, inOpts=None) :
		import argparse

		self.parser = argparse.ArgumentParser("This program accepts metadata file input, cluster files, etc, and writes a JSON message")
		'''First argument is metadatafile.'''
		self.parser.add_argument('-metadataFile', '--metadata_file')
		'''Second argument is the clusterfile'''
		self.parser.add_argument('-clusterFile', '--clusters_file')

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
				data.metadata.clustering_method_parameters_JSON = v
			if k == 'method_input_datatypes_JSON':
				data.clustering_method_input_datatypes_JSON  = v
			if k =='method_name':
				data.metadata.clustering_method = v
			if k == 'cluster_member_type':
				data.metadata.membertype = v 


			for k,v in self.clusterFile_dict.items():
				group = data.groups.add()
				group = v #a list of sample names
				for name in v:
					group.name = name # cluster_ID

			#change to JSON format
			return MessageToJson(data)

def main():
	command_line = CommandLine()
	cluster_fn = command_line.args.clusters_file
	metadata_fn = command_line.args.metadata_file

	#MAIN PROCEDURE - adding data
	cluster_data = BMEG_pb2.BMEG_Clustering()


	res = writeMessage()
	res.clusterFileParser(cluster_fn)
	res.metadataFileParser(metadata_fn)
	res.AddData(cluster_data)

	



	# for i in range(1): #this range can be the number of lines in the file
	# 	'''OPTION 1: Write the new data to a new file named test.txt'''
	# 	# with open('test.txt', "wb") as f:
	# 	# 	f.write(MessageToJson(cluster_data))


	# 	'''OPTION 2: Print in command line'''
	# 	print(AddData(cluster_data))

if __name__ == "__main__":
	main()
