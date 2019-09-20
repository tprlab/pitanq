def init_labels(path):
    ret = {}
    with open(path, "r") as f:
        line = f.readline()
        while line:
            s = line.strip().split(":")
            if len(s) == 2:
                ret[int(s[0])] = s[1]    
            line = f.readline()
    return ret
        