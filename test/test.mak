PROTO_FILE=BMEG.proto

TEST_DIR=./test
TEST_METADATA_FILE=$(TEST_DIR)/test_metadata.txt
CLUSTER_ASSIGNMENT_FILE=$(TEST_DIR)/test_clusters.txt

TARGETS=message.json

message.json:
	python BMEG_addData.py \
		--metadata_file $(TEST_METADATA_FILE) \
		--cluster_assignment_file $(CLUSTER_ASSIGNMENT_FILE) \
	> message.json ;

compile_pb:
	protoc --python_out=. $(PROTO_FILE) ;
	\

clean:
	rm -f $(TARGETS) ;
	\
	rm -f $(wildcard *_pb2.py) ;
	\
