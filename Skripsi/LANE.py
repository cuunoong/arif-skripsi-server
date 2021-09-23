import cv2 as cv
import math
import PIL.Image as Image
import io
import numpy as np
import calendar
import time


def pangkat(x, n = 2):
    return x**n
def akar(x, n = 2):
    return pangkat(x, 1 / n)

class LANE:

    __image = None
    __tengah  = 200
    __kiri    = 30
    __kanan   = 370
    __baris   = 200
    __posisiKiri = []
    __posisiKanan = []
    __rataKiri = 30
    __rataKanan = 370
    
    def setImage(self, image):
        pil_image = Image.open(io.BytesIO(image))
        opencv_image = np.array(pil_image)
        self.__image = cv.cvtColor(opencv_image, cv.COLOR_BGR2RGB)
        self.__image = cv.rotate(self.__image, cv.ROTATE_180)
    
    def grayscale(self):
        self.__image = cv.cvtColor(self.__image, cv.COLOR_BGRA2GRAY)

    def threshold(self):
        _, threshold = cv.threshold(self.__image, 120, 255, cv.THRESH_BINARY)
        self.__image = threshold

    def checkLane(self):
        self.__posisiKanan = []

    def countRate(self):
        return self

    def getDegree(self):
        posisi = (self.__rataKiri + self.__rataKanan) / 2
        garisMiring = akar(pangkat(posisi - self.__tengah) + pangkat(100))

        E = (posisi - self.__tengah) / garisMiring
        angle = math.asin(E)
        degree = math.degrees(angle)
        
        return math.floor(degree)

    def save(self):
        ts = calendar.timegm(time.gmtime())
        cv.imwrite('capture/' + str(ts) + ".jpg", self.__image)

    def getImage(self):
        _, im =cv.imencode('.jpg', self.__image)
        return im.tobytes()