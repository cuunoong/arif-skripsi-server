from Skripsi.PID import PID
from Skripsi.LANE import LANE


def pid(setPoint = 0):
    return PID(setPoint)

def lane():
    return LANE()