#! /usr/bin/env python3
#Name: Ioannis Anastopoulos

import BMEG_pb2
import sys


def AddData(data):
	#Adding PanCancerAtlas
	data.name = ("Enter Cluster name: PanCancerAtlas")

	#Adding metadata
	data.metadata.description = 'Metadata Description: ' + str(input("Enter metadata description: "))
	data.metadata.clustering_method = 'Clustering Method: ' + str(input('Enter clustering method: '))
	data.metadata.clustering_method_parameters_JSON = 'JSON parameters: ' + str(input("Enter JSON stuff: "))
	

	data.metadata.membertype = int(input('Enter number of samples')) #WHY does the enumerator variables have to be int?
	data.metadata.membertype = BMEG_pb2.BMEG_Clustering.SAMPLES

	data.metadata.membertype = int(input('Enter Gene: '))
	data.metadata.membertype = BMEG_pb2.BMEG_Clustering.GENES

	'''NOT sure why AttributeError here???'''
	# data.clustering_method_input_datatypes_JSON  = 'JSON input: ' + str(input("Enter JSON input stuff: "))
	
	#adding cluster names. E.g. ic01 ic02 etc.
	while True:
		name = str(input('enter cluster name: '))
		if name =='':
			break
		name_cool = 'Cluster name: ' +name

		group = data.groups.add()
		group.name = name_cool
	return data.SerializeToString()


#MAIN PROCEDURE - adding data
cluster_data = BMEG_pb2.BMEG_Clustering()

for i in range(1): #this range can be the number of lines in the file
	'''OPTION 1: Write the new data to a new file named test.txt'''
	# with open('test.txt', "wb") as f:
	# 	f.write(cluster_data.SerializeToString())


	'''OPTION 2: Print in command line'''
	print(AddData(cluster_data))







