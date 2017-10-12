TEST_DIR=./test
TEST_METADATA_FILE=$(TEST_DIR)/test_metadata.txt
CLUSTER_ASSIGNMENT_FILE=$(TEST_DIR)/test_clusters.txt

TARGETS=message.json

message.json:
	python BMEG_addData.py \
		--metadata_file $(TEST_METADATA_FILE) \
		--cluster_assignment_file $(CLUSTER_ASSIGNMENT_FILE) \
	> message.json ;

clean:
	rm -f $(TARGETS) ;
	\
