import requests;
import json;

cfg_file = open("config.json", "r");
cfg = json.loads(cfg_file.read());
cfg_file.close();

def getData(filename, slice_start = 0, slice_end = 5):
	data_file = open(filename, "r+");
	data_list = data_file.readlines();
	data_file.close();

	raw_data = [];

	for i in range(slice_start, slice_end):
		clear_str = data_list[i].replace("NaN", "0.00");
		raw_data.append(json.loads(clear_str));

	keys = [];
	data = {};

	for key in raw_data[0]:
		keys.append(key);
		data[key] = [];


	for sample in raw_data:
		for key in keys:
			data[key].append(sample[key]);

	return data;

def main():

	data = getData("samples.json");
	http_headers = {"content-type": "application/json", "accept": "application/json"};

	post_data = json.dumps(data).encode("utf-8");
	result = requests.post(cfg["rest_url"], data = post_data, headers = http_headers);

	return result;


if __name__ == "__main__":
	result = main();
	print(result.text);