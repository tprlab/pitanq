import label_map_util
import PiConf

PATH_TO_LABELS = PiConf.DNN_LABELS_PATH

NUM_CLASSES = 90
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def getLabel(id):
    e = category_index[id]
    return e["name"] if e is not None else ""
