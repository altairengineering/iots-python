.PHONY: all

all: anythingdb

anythingdb:
	datamodel-codegen  --input openapi/anythingdb.yaml --input-file-type openapi --output models/anythingdb.py --base-class models.basemodel.IterBaseModel
