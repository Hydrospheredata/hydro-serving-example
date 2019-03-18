import grpc;
import hydro_serving_grpc as hs;
import json;

cfg_file = open("config.json", "r");
cfg = json.loads(cfg_file.read());
cfg_file.close();

def getData(filename, size = 5):
	data_file = open(filename, "r+");
	data_list = data_file.readlines();
	data_file.close();

	data = [];

	for i in range(0, size):
		data.append(data_list[i].replace('"', '\\"').encode("utf-8"));

	return data;

def main():
	channel = grpc.insecure_channel(cfg["url"]); 
	stub = hs.PredictionServiceStub(channel); 

	data = getData("samples.json");
	dim_size = len(data);

	model_spec = hs.ModelSpec(name="favorita", signature_name="favorita");

	tensor_shape = hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=dim_size)]);

	tensor = hs.TensorProto(dtype=hs.DT_STRING, tensor_shape=tensor_shape, string_val=data)

	request = hs.PredictRequest(model_spec=model_spec, inputs={"input_data": tensor}) 

	result = stub.Predict(request)

	return result;

if __name__ == "__main__":
	main();