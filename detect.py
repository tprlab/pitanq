import cv2
import sys
import os
import logging


def handleFile(f, cascade):
    image = cv2.imread(f)
    if image is None:
        logging.debug("File %s not found" % f)
        return None, None
    rects = findObj(cascade, image)

    print (f, rects)
    return image, rects



def findObj(cascade, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    detector = cv2.CascadeClassifier(cascade)
    if detector.empty():
        logging.debug("No cascade loaded: " + cascade)
        return None
    rects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(75, 75))
    return rects

def drawRects(image, rects):
    for (i, (x, y, w, h)) in enumerate(rects):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)


def showPic(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)


if __name__ == '__main__':
    path = sys.argv[1]
    cascade = "haarcascade_frontalcatface.xml"
    img, rects = handleFile(path, cascade)
    print (rects)
    
