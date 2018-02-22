#!/bin/bash

DATA_DIR=/data
# DATA_DIR=./example
LIB_DIR=/bmeg_lib
# LIB_DIR=./lib
OUTPUT_DIRECTORY=protograph

mkdir -p $OUTPUT_DIRECTORY ;
\
echo "CONVERT METADATA FILES AND GMT FILES TO PROTOCOL BUFFERS MESSAGES" ;
\
for genesets in `find $DATA_DIR -name "*.gmt" | sed -e 's/\.gmt$//' ` ; do \
	python3 $LIB_DIR/gmt_to_protobuf.py \
		--metadata-file ${genesets}_metadata.txt \
		--gmt-file ${genesets}.gmt \
	; \
	\
	cat gmt_pb.jsonl \
	>> 1.tmp ; \
	\
done ;
\
mv 1.tmp $OUTPUT_DIRECTORY/protobuf_gmt.jsonl ;
\
echo "CONVERT PROTOCOL BUFFERS MESSAGES INTO PROTOGRAPH FILES" ;
\
java -jar $LIB_DIR/protograph.jar \
	--protograph $LIB_DIR/genesets.yml \
	--input $OUTPUT_DIRECTORY/protobuf_gmt.jsonl \
	--output protograph_gmt \
	--label Geneset \
;
\
cp *.Vertex.json $OUTPUT_DIRECTORY/. ;
cp *.Edge.json $OUTPUT_DIRECTORY/. ;
\
echo "COPY RESULTS TO DATA DIRECTORY" ;
\
cp -r $OUTPUT_DIRECTORY $DATA_DIR/. ;
\
