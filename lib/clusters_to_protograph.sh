#!/bin/bash

DATA_DIR=/data
LIB_DIR=/bmeg_lib
OUTPUT_DIRECTORY=protograph

mkdir -p $OUTPUT_DIRECTORY ;
\
echo "CONVERT METADATA FILES AND CLUSTER FILES TO PROTOCOL BUFFERS MESSAGES" ;
\
for clustering in `find $DATA_DIR -name "*_for_bmeg.txt" | grep -v "example" | sed -e 's/_for_bmeg.txt$//' ` ; do \
	python3 $LIB_DIR/BMEG_addData.py \
		-metadataFile ${clustering}_metadata.txt \
		-clusterFile ${clustering}_for_bmeg.txt \
	; \
	\
	cat JSONMethodMessage.txt \
	>> 1.tmp ; \
	\
	cat JSONClustersMessage.txt \
	>> 2.tmp ; \
done ;
\
mv 1.tmp $OUTPUT_DIRECTORY/protobuf_method.jsonl ;
\
mv 2.tmp $OUTPUT_DIRECTORY/protobuf_clusters.jsonl ;
\
echo "CONVERT PROTOCOL BUFFERS MESSAGES INTO PROTOGRAPH FILES" ;
\
java -jar $LIB_DIR/protograph.jar \
	--protograph $LIB_DIR/cluster.yml \
	--input $OUTPUT_DIRECTORY/protobuf_method.jsonl \
	--output protograph_method \
	--label Method \
;
\
java -jar $LIB_DIR/protograph.jar \
	--protograph $LIB_DIR/cluster.yml \
	--input $OUTPUT_DIRECTORY/protobuf_clusters.jsonl \
	--output protograph_clusters \
	--label Cluster \
;
\
cp *.Vertex.json $OUTPUT_DIRECTORY/. ;
cp *.Edge.json $OUTPUT_DIRECTORY/. ;
\
echo "COPY RESULTS TO DATA DIRECTORY" ;
\
cp -r $OUTPUT_DIRECTORY $DATA_DIR/. ;
\
