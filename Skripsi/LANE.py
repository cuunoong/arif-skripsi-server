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
    __tengah  = 320
    __kiri    = 30
    __kanan   = 370
    __baris   = 200
    __posisiKiri = []
    __posisiKanan = []
    __rataKiri = 30
    __rataKanan = 370
    
    def setImage(self, image):
        pil_image = Image.open(io.BytesIO(image))
        W,H = pil_image.size
        self.__tengah = W / 2
        opencv_image = np.array(pil_image)
        self.__image = opencv_image
        # self.__image = cv.cvtColor(opencv_image, cv.COLOR_BGR2RGB)
        # self.__image = cv.rotate(self.__image, cv.ROTATE_180)
        return self.__image
    
    def colorSelection(self, image = None):
        if(image is None):
            image = self.__image
        lower_threshold = np.uint8([0, 150, 0])
        upper_threshold = np.uint8([255, 255, 255])
        mask = cv.inRange(image, lower_threshold, upper_threshold)

        color = cv.bitwise_and(image, image, mask = mask)
        return color


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
        top_left     = [cols * 0.25, rows * 0.4]
        bottom_right = [cols*1, rows * 1]
        top_right    = [cols * 0.75, rows * 0.4]
        vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
        cv.fillPoly(mask, vertices, ignore_mask_color)
        masked_image = cv.bitwise_and(img, mask)
        return masked_image

    def houghTransform(self, image):
        rho = .5
        theta = np.pi/180
        threshold = 30
        minLineLength = 20
        maxLineGap = 300 
        return cv.HoughLinesP(image, rho = rho, theta = theta, threshold = threshold,
                           minLineLength = minLineLength, maxLineGap = maxLineGap)

    def average_slope_intercept(self, lines):
        left_lines    = [] #(slope, intercept)
        left_weights  = [] #(length,)
        right_lines   = [] #(slope, intercept)
        right_weights = [] #(length,)
        

        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == x2:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - (slope * x1)
                length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
                if slope < 0:
                    left_lines.append((slope, intercept))
                    left_weights.append((length))
                else:
                    right_lines.append((slope, intercept))
                    right_weights.append((length))

        left_lane  = np.dot(left_weights,  left_lines) / np.sum(left_weights)  if len(left_weights) > 0 else None
        right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
        return left_lane, right_lane

    def pixel_points(self, y1, y2, line):
        if line is None:
            return None
        slope, intercept = line
        x1 = 0
        x2 = 0
        if(slope > 0):
            x1 = int((y1 - intercept)/slope)
            x2 = int((y2 - intercept)/slope)
        y1 = int(y1)
        y2 = int(y2)
        return ((x1, y1), (x2, y2))

    def lane_lines(self, image, lines):
        left_lane, right_lane = self.average_slope_intercept(lines)
        y1 = image.shape[0]
        y2 = y1 * 0.4
        left_line  = self.pixel_points(y1, y2, left_lane)
        right_line = self.pixel_points(y1, y2, right_lane)
        return left_line, right_line

    def drawLaneLines(self, image, lines, color=[0, 0, 255], thickness=12):
        line_image = np.zeros_like(image)
        for line in lines:
            if line is not None:
                cv.line(line_image, *line,  color, thickness)
        return cv.addWeighted(image, 1.0, line_image, 1.0, 0.0)
        
    def getDegree(self, left, right):
        posisi = (left + right) / 2
        garisMiring = akar(pangkat(posisi - self.__tengah) + pangkat(100))
        E = abs(posisi - self.__tengah) / garisMiring
        angle = math.asin(E)
        degree = math.degrees(angle)
        if(posisi > self.__tengah):
            degree += 90
        else:
            degree = 90 - degree
        return math.floor(degree)

    def save(self, image =  None):
        if(image is not None):
            ts = calendar.timegm(time.gmtime())
            cv.imwrite('capture/' + str(ts) + ".jpg", image)
        elif(self.__image is not None):
            ts = calendar.timegm(time.gmtime())
            cv.imwrite('capture/' + str(ts) + ".jpg", self.__image)

    def getImage(self, image = None):
        if(image is None):
            image = self.__image.copy()
        _, im =cv.imencode('.jpg', image)
        return im.tobytes()