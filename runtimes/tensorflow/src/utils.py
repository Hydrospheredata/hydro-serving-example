import numpy as np

def convert_to_python(data):
    if isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    else:
        print("{0} isn't convertible to python".format(type(data)))
        return data
