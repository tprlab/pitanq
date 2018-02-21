import cv2
import sys
import os

#cascade = sys.argv[1]
#path = sys.argv[2]

def handleFile(f, cascade):
    image = cv2.imread(f)
    if image is None:
        print "File", f, "not found"
        return None, None
    rects = findObj(cascade, image)

    print f, rects
    return image, rects
    #if rects is not None:
    #    drawRects(image, rects)



def findObj(cascade, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
    #detector = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
    detector = cv2.CascadeClassifier(cascade)
    if detector.empty():
        return None
    rects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=10, minSize=(75, 75))
    return rects

def drawRects(image, rects):

    for (i, (x, y, w, h)) in enumerate(rects):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #cv2.putText(image, "Cat #{}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

def showPic(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)


if __name__ == '__main__':
    path = "test.jpg"
    cascade = "haarcascade_frontalcatface.xml"
    img, rects = handleFile(path, cascade)
    #print rects
    #drawRects(img, rects)
    #showPic("TestCV", img)
    
