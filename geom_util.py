import numpy as np
import math


def calc_line(x1, y1, x2, y2):
    a = float(y2 - y1) / (x2 - x1) if x2 != x1 else 0
    b = y1 - a * x1
    return a, b

def calc_line_length(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)

def get_horz_shift(x, w):
    hw = w / 2
    return 100 * (x - hw) / hw


def calc_rect_area(rect_points):
    a = calc_line_length(rect_points[0], rect_points[1])
    b = calc_line_length(rect_points[1], rect_points[2])
    return a * b

def get_vert_angle(p1, p2, w, h):
    px1 = p1[0] - w/2
    px2 = p2[0] - w/2
    
    py1 = h - p1[1]
    py2 = h - p2[1]

    angle = 90
    if px1 != px2:
        a, b = calc_line(px1, py1, px2, py2)
        angle = 0
        if a != 0:
            x0 = -b/a
            y1 = 1.0
            x1 = (y1 - b) / a
            dx = x1 - x0
            tg = y1 * y1 / dx / dx
            angle = 180 * np.arctan(tg) / np.pi
            if a < 0:
                angle = 180 - angle
    return angle


def order_box(box):
    srt = np.argsort(box[:, 1])
    btm1 = box[srt[0]]
    btm2 = box[srt[1]]

    top1 = box[srt[2]]
    top2 = box[srt[3]]

    bc = btm1[0] < btm2[0]
    btm_l = btm1 if bc else btm2
    btm_r = btm2 if bc else btm1

    tc = top1[0] < top2[0]
    top_l = top1 if tc else top2
    top_r = top2 if tc else top1

    return np.array([top_l, top_r, btm_r, btm_l])

def calc_box_vector(box):
    v_side = calc_line_length(box[0], box[3])
    h_side = calc_line_length(box[0], box[1])
    idx = [0, 1, 2, 3]
    if v_side < h_side:
        idx = [0, 3, 1, 2]
    return ((box[idx[0]][0] + box[idx[1]][0]) / 2, (box[idx[0]][1] + box[idx[1]][1]) / 2), ((box[idx[2]][0] + box[idx[3]][0]) / 2, (box[idx[2]][1]  +box[idx[3]][1]) / 2)
