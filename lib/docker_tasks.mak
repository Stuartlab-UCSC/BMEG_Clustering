THIS_DIR=$(shell pwd)

DATA_DIR=/data/data
LIB_DIR=/bmeg_lib

test:protograph_edges

protograph_edges:

protobuf_messages:
	mkdir -p $@ ;
	\
	for clustering in `find $(DATA_DIR) -name "*_for_bmeg.txt" | sed -e 's/_for_bmeg.txt$$//' ` ; do \
		echo $${clustering} ; \
		\
		python3 $(LIB_DIR)/BMEG_addData.py \
			-metadataFile $${clustering}_metadata.txt \
			-clusterFile $${clustering}_for_bmeg.txt \
		; \
		\
		cat JSONMethodMessage.txt \
		>> 1.tmp ; \
		\
		cat JSONClustersMessage.txt \
		>> 2.tmp ; \
		\
	done ;
	\
	mv 1.tmp $@/protobuf_method.jsonl ;
	\
	mv 2.tmp $@/protobuf_clusters.jsonl ;
	\
	rm -rf $(DATA_DIR)/$@ ;
	\
	mv $@ $(DATA_DIR)/. ;
	\
	rm -f 1.tmp 2.tmp JSONMethodMessage.txt JSONClustersMessage.txt ;
	\

