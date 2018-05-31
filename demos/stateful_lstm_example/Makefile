HOST=localhost
PORT=8080

upload-all: upload-lstm upload-postprocessing upload-preprocessing

upload-%:
	cd pipeline/$* && hs upload --host $(HOST) --port $(PORT)