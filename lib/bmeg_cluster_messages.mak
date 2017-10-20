
LIB_DIR=./lib
PROTO_FILE=$(LIB_DIR)/BMEG.proto

TEST_DIR=./test
# DATA_DIR=./data
DATA_DIR=$(TEST_DIR)
TEST_METADATA_FILE=$(TEST_DIR)/test_clusters_metadata.txt
CLUSTER_ASSIGNMENT_FILE=$(TEST_DIR)/test_clusters_for_bmeg.txt

TARGETS=clusters.jsonl JSONmessage.txt

test:clusters.jsonl

clusters.jsonl: compile_pb
	rm -f 1.tmp ;
	\
	for clustering in `find $(DATA_DIR) -name "*_for_bmeg.txt" | sed -e 's,$(DATA_DIR)/,,' -e 's/_for_bmeg.txt//' ` ; do \
		echo $${clustering} ; \
		\
		python3 $(LIB_DIR)/BMEG_addData.py \
			--metadata_file $(DATA_DIR)/$${clustering}_metadata.txt \
			--clusters_file $(DATA_DIR)/$${clustering}_for_bmeg.txt \
			; \
		\
		cat JSONmessage.txt \
		>> 1.tmp ; \
	done ;
	\
	mv 1.tmp $@ ;
	\
	rm -f 1.tmp JSONmessage.txt ;
	\

JSONmessage.txt: compile_pb
	python3 $(LIB_DIR)/BMEG_addData.py \
		--metadata_file $(TEST_METADATA_FILE) \
		--clusters_file $(CLUSTER_ASSIGNMENT_FILE) \
		;

compile_pb:
	protoc --python_out=. $(PROTO_FILE) ;
	\

clean:
	rm -f $(TARGETS) ;
	\
	rm -f `find $(LIB_DIR) -name "*_pb2.py"` ;
	\
	rm -f $(wildcard *.tmp) ;
	\
