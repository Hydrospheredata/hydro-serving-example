import re
import pickle
from keras.preprocessing import sequence

max_features = 20000
maxlen = 100
with open('/model/files/tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)


def tokenize(sentence):
    if 'www.' in sentence or 'http:' in sentence or 'https:' in sentence or '.com' in sentence:
        sentence = re.sub(r"([^ ]+(?<=\.[a-z]{3}))", "<url>", sentence)

    tok_sentence = tokenizer.texts_to_sequences([sentence])
    pad_sentence = sequence.pad_sequences(tok_sentence, maxlen=maxlen)[0]
    return {
        "tokenized": pad_sentence.astype("int64"),
    }
