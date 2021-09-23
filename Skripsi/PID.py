class PID:

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
        self.__SetPoint = setPoint

    def reset(self) -> None:
        self.__LastError = 0
        self.__LastI = 0
        self.__SetPoint = 0

    def setPoint(self, sp) -> None:
        self.__SetPoint = sp

    def getSetPoint(self) -> float:
        return self.__SetPoint

    def run(self, error) -> float:
        Error = self.__SetPoint - error
        I = self.__LastI + Error
        pid = (self.__Kp * Error) + (self.__Ki * I * self.__Tc) + (self.__Kd * (Error - self.__LastError) / self.__Tc)

        self.__LastError = Error
        self.__LastI = I

        return pid

