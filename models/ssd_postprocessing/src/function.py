import numpy as np
from nets import ssd_vgg_300, ssd_common, np_methods
from preprocessing import ssd_vgg_preprocessing

NET_SHAPE = (300, 300)
SELECT_TRESHOLD=0.5
NMS_TRESHOLD=0.45

ssd_net = ssd_vgg_300.SSDNet()
ssd_anchors = ssd_net.anchors(NET_SHAPE)

def execute(data: list, **kwargs):
    for row in data:
        rpredictions = [
            np.array(row['ssd_300_vgg/softmax/Reshape_1:0']),
            np.array(row['ssd_300_vgg/softmax_1/Reshape_1:0']),
            np.array(row['ssd_300_vgg/softmax_2/Reshape_1:0']),
            np.array(row['ssd_300_vgg/softmax_3/Reshape_1:0']),
            np.array(row['ssd_300_vgg/softmax_4/Reshape_1:0']),
            np.array(row['ssd_300_vgg/softmax_5/Reshape_1:0'])
        ]
        rlocalisations = [
            np.array(row['ssd_300_vgg/block4_box/Reshape:0']),
            np.array(row['ssd_300_vgg/block7_box/Reshape:0']),
            np.array(row['ssd_300_vgg/block8_box/Reshape:0']),
            np.array(row['ssd_300_vgg/block9_box/Reshape:0']),
            np.array(row['ssd_300_vgg/block10_box/Reshape:0']),
            np.array(row['ssd_300_vgg/block11_box/Reshape:0'])
        ]
        rbbox_img = row['bbox_img']

        # Get classes and bboxes from the net outputs.
        rclasses, rscores, rbboxes = np_methods.ssd_bboxes_select(
            rpredictions, rlocalisations, ssd_anchors,
            select_threshold=SELECT_TRESHOLD, img_shape=NET_SHAPE, num_classes=21, decode=True)

        rbboxes = np_methods.bboxes_clip(rbbox_img, rbboxes)
        rclasses, rscores, rbboxes = np_methods.bboxes_sort(rclasses, rscores, rbboxes, top_k=400)
        rclasses, rscores, rbboxes = np_methods.bboxes_nms(rclasses, rscores, rbboxes, nms_threshold=NMS_TRESHOLD)
        # Resize bboxes to original image shape. Note: useless for Resize.WARP!
        rbboxes = np_methods.bboxes_resize(rbbox_img, rbboxes)

        row["classes"] = rclasses.tolist()
        row["scores"] = rscores.tolist()
        row["boxes"] = rbboxes.tolist()

    return data
