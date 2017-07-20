import urllib.request
import json
import os
import tensorflow as tf


class MLRepository:
    def __init__(self, addr, port):
        self.host = "http://{0}:{1}".format(addr, port)

    def get_metadata(self, model_name):
        jss = urllib.request.urlopen("{0}/metadata/{1}".format(self.host, model_name)).read().decode('utf8')
        return json.loads(jss)

    def get_files(self, model_name):
        jss = urllib.request.urlopen("{0}/files/{1}".format(self.host, model_name)).read().decode('utf8')
        return json.loads(jss)

    def download_file(self, model_name, file_name):
        url = "{0}/download/{1}/{2}".format(self.host, model_name, file_name)
        save_path = "models/{0}/{1}".format(model_name, file_name)

        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        urllib.request.urlretrieve(url, save_path)

        return save_path

    def load_model(self, sess, model_name):
        model_path = "models/{0}/{0}".format(model_name)
        meta_graph = tf.train.import_meta_graph("{0}.meta".format(model_path))
        meta_graph.restore(sess, model_path)
        return sess
