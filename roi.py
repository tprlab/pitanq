import numpy as np
import cv2 as cv


class ROI:
    area = 0
    vertices = None


    def init_roi(self, width, height):
        vertices = [(0, height), (width / 4, 3 * height / 4),(3 * width / 4, 3 * height / 4), (width, height),]
        self.vertices = np.array([vertices], np.int32)
        
        blank = np.zeros((height, width, 3), np.uint8)
        blank[:] = (255, 255, 255)
        blank_gray = cv.cvtColor(blank, cv.COLOR_BGR2GRAY)
        blank_cropped = self.crop_roi(blank_gray)
        self.area = cv.countNonZero(blank_cropped)



    def crop_roi(self, img):
        mask = np.zeros_like(img)
        match_mask_color = 255
        
        cv.fillPoly(mask, self.vertices, match_mask_color)
        masked_image = cv.bitwise_and(img, mask)
        return masked_image

    def get_area(self):
        return self.area

    def get_vertices(self):
        return self.vertices

