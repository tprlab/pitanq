import label_map_util


NUM_CLASSES = 90
category_index = None

def initLabels(path):
    global category_index
    label_map = label_map_util.load_labelmap(path)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)   


def getLabel(id):
    if category_index is None:
        return "Not initialized"
    e = category_index[id]
    return e["name"] if e is not None else ""
