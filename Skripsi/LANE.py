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
    __logs = "lane.logs"
    __image = None
    __tinggi = 0
    __lebar = 0
    __tengah  = 320
    def __init__(self) -> None:
        self.write("")

    def setImage(self, image):
        pil_image = Image.open(io.BytesIO(image))
        self.__lebar,self.__tinggi = pil_image.size
        self.__tengah = self.__lebar / 2
        opencv_image = np.array(pil_image)
        self.__image = opencv_image
        # self.__image = cv.cvtColor(opencv_image, cv.COLOR_BGR2RGB)
        # self.__image = cv.rotate(self.__image, cv.ROTATE_180)
        return self.__image

    def grayscale(self, img):
        return cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    def gaussianBlur(self, img, kernel = 5):
        return cv.GaussianBlur(img, (kernel, kernel), 0)

    def cannyEdgeDetection(self, img):
        return cv.Canny(img, 50, 150)

    def regionSelection(self, img):
        mask = np.zeros_like(img)
        if len(img.shape) > 2:
            channel_count = img.shape[2]
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255
        rows, cols = img.shape[:2]
        
        bottom_left  = [0, rows * 1]
        top_left     = [cols * 0.2, rows * 0.4]
        bottom_right = [cols*1, rows * 1]
        top_right    = [cols * 0.7, rows * 0.4]
        vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
        cv.fillPoly(mask, vertices, ignore_mask_color)
        masked_image = cv.bitwise_and(img, mask)
        return masked_image

    def getLanes(self, img):
        left = 0
        right = self.__lebar

        bottom = self.__tinggi - 100
        
        row, col  = np.where(img == 255)
        white_row = np.where(row == bottom - 1)
        for _row in white_row[0]:
            if col[_row] < self.__lebar / 2:
                if left < col[_row]:
                    left = col[_row]
            else:
                if right > col[_row]:
                    right = col[_row]
        return (((left, bottom + 10), (left, bottom - 10)), ((right, bottom + 10), (right, bottom - 10)))

    def drawLaneLines(self, image, lines, color=[0, 0, 255], thickness=12):
        line_image = np.zeros_like(image)
        for line in lines:
            if line is not None:
                cv.line(line_image, *line,  color, thickness)
        return cv.addWeighted(image, 1.0, line_image, 1.0, 0.0)
        
        
    def getDegree(self, lines):
        left_line, right_line = lines
        left = left_line[0][0]
        right = right_line[0][0] 
        
        posisi = (left + right) / 2

        garisMiring = akar(pangkat(posisi - self.__tengah) + pangkat(100))
        E = abs(posisi - self.__tengah) / garisMiring
        angle = math.asin(E)
        degree = math.degrees(angle)
        if(posisi > self.__tengah):
            degree += 90
        else:
            degree = 90 - degree
        
        self.log("left=" + str(left) + ";right=" + str(right) + ";deg=" + str(degree))

        return math.floor(degree)

    def save(self, image =  None):
        if(image is not None):
            ts = calendar.timegm(time.gmtime())
            cv.imwrite('capture/' + str(ts) + ".jpg", image)
        elif(self.__image is not None):
            ts = calendar.timegm(time.gmtime())
            cv.imwrite('capture/' + str(ts) + ".jpg", self.__image)

    def write(self, msg):
        f = open(self.__logs, 'w')
        f.write(msg  + "\n")
        f.close()
    
    def log(self, log):
        f = open(self.__logs, 'a')
        f.write(log + "\n")
        f.close()
        
    def getImage(self, image = None):
        if(image is None):
            image = self.__image.copy()
        _, im =cv.imencode('.jpg', image)
        return im.tobytes()