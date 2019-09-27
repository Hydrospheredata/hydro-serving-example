import re
import hydro_serving_grpc as hs
import pickle
from keras.preprocessing import sequence
with open('/model/files/tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

max_features = 20000
maxlen = 100
def tokenize(text):
    sentence = [str.decode() for str in text.string_val][0]

    if 'www.' in sentence or 'http:' in sentence or 'https:' in sentence or '.com' in sentence:
        sentence = re.sub(r"([^ ]+(?<=\.[a-z]{3}))", "<url>", sentence)

    tok_sentence = tokenizer.texts_to_sequences([sentence])
    pad_sentence = sequence.pad_sequences(tok_sentence, maxlen=maxlen)[0]
    tok_tensor = hs.TensorProto(
        int64_val = pad_sentence,
        dtype=hs.DT_INT64,
        tensor_shape=hs.TensorShapeProto(dim=[hs.TensorShapeProto.Dim(size=100)]))
    return hs.PredictResponse(outputs={'tokenized': tok_tensor})

