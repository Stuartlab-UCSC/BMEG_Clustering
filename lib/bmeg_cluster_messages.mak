
LIB_DIR=./lib
PROTO_FILE=$(LIB_DIR)/BMEG.proto

TEST_DIR=./test
DATA_DIR=./data
# DATA_DIR=$(TEST_DIR)
TEST_METADATA_FILE=$(TEST_DIR)/test_clusters_metadata.txt
CLUSTER_ASSIGNMENT_FILE=$(TEST_DIR)/test_clusters_for_bmeg.txt

PROTOGRAPH_JAR=$(LIB_DIR)/protograph.jar
PROTOGRAPH_YML_FILE=$(LIB_DIR)/protograph.yml
PROTOGRAPH_OUTPUT_FILE_PREFIX=protograph_out

TARGETS=clusters.jsonl JSONmessage.txt

test:clusters.jsonl
	head -n 1 $< \
	> 1.tmp ;
	\
	java -jar $(PROTOGRAPH_JAR) \
		--protograph $(PROTOGRAPH_YML_FILE) \
		--input 1.tmp \
		--output $(PROTOGRAPH_OUTPUT_FILE_PREFIX) \
	;
	\

clusters.jsonl: compile_pb.done
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

JSONmessage.txt: compile_pb.done
	python3 $(LIB_DIR)/BMEG_addData.py \
		--metadata_file $(TEST_METADATA_FILE) \
		--clusters_file $(CLUSTER_ASSIGNMENT_FILE) \
		;

compile_pb.done:
	protoc --python_out=. $(PROTO_FILE) ;
	\
	touch $@ ;
	\

clean:
	rm -f $(wildcard $(PROTOGRAPH_OUTPUT_FILE_PREFIX)*) ;
	\
	rm -f $(TARGETS) ;
	\
	rm -f `find $(LIB_DIR) -name "*_pb2.py"` ;
	\
	rm -f compile_pb.done ;
	\
	rm -f $(wildcard *.tmp) ;
	\