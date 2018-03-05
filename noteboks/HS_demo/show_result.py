from visualization import plt_bboxes
import numpy as np
import matplotlib.image as mpimg

VOC_MAP = {
    0: 'none',
    1: 'aeroplane',
    2: 'bicycle',
    3: 'bird',
    4: 'boat',
    5: 'bottle',
    6: 'bus',
    7: 'car',
    8: 'cat',
    9: 'chair',
    10: 'cow',
    11: 'diningtable',
    12: 'dog',
    13: 'horse',
    14: 'motorbike',
    15: 'person',
    16: 'pottedplant',
    17: 'sheep',
    18: 'sofa',
    19: 'train',
    20: 'tvmonitor'
}

def convert_class(class_name):
    for idx, c_name in VOC_MAP.items():
        if c_name == class_name:
            print("Class: {} -> {}".format(class_name, idx))
            return idx
    return None

def double_tensor_to_list(tensor):
    shape = [x.size for x in tensor.tensor_shape.dim ] 
    doubles = np.array(tensor.double_val)
    return doubles.reshape(shape)

def string_tensor_to_list(tensor):
    shape = [x.size for x in tensor.tensor_shape.dim ] 
    strings = [s.decode("UTF-8") for s in tensor.string_val]
    return np.reshape(strings, shape)

def show_result(img_path, result):
    outputs_dict = result.outputs
    classes_tensor = string_tensor_to_list(outputs_dict["classes"])
    converted_classes = np.array([convert_class(x) for x in classes_tensor])
    bboxes_tensor = outputs_dict["bboxes"]
    scores_tensor = outputs_dict["scores"]
    img = mpimg.imread(img_path)
    plt_bboxes(
        img,
        converted_classes,
        double_tensor_to_list(scores_tensor),
        double_tensor_to_list(bboxes_tensor),
    )