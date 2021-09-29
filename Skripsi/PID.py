class PID:

    __logs = "pid.logs"

    # Konstanta Proposional
    __Kp = 0.9

    # Konstanta Integral
    __Ki = 0.5

    # Konstanta Derivatif
    __Kd = 0.00000000001

    __Tc = 0.001

    __LastError = 0
    __LastI = 0
    __SetPoint = 0

    def __init__(self, setPoint) -> None:
        self.setSetPoint(setPoint)

    def write(self, msg):
        f = open(self.__logs, 'w')
        f.write(msg  + "\n")
        f.close()
    
    def log(self, log):
        f = open(self.__logs, 'a')
        f.write(log + "\n")
        f.close()

    def reset(self) -> None:
        self.__LastError = 0
        self.__LastI = 0
        self.__SetPoint = 0

    def setSetPoint(self, sp) -> None:
        self.__SetPoint = sp
        self.write("setPoint=" + str(self.__SetPoint))

    def getSetPoint(self) -> float:
        return self.__SetPoint

    def run(self, dg) -> float:
        Error = self.__SetPoint - dg
        I = self.__LastI + Error
        pid = (self.__Kp * Error) + (self.__Ki * I * self.__Tc) + (self.__Kd * (Error - self.__LastError) / self.__Tc)

        self.__LastError = Error
        self.__LastI = I

        self.log("pid=" + str(pid) + ";Dg=" + str(dg) + ";lE=" + str(Error) + ";lI=" + str(I))
        return pid

    def getLastError(self):
        return self.__LastError
    
    def getI(self):
        return self.__LastI

