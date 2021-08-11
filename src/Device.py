# from SX127x import LoRa
from constants import DEVCLASS
from LoRaMAC import LoRaMAC
from Radio import Radio, SX127X


class Device():
    """ Base Class of LoRaWAN Device """

    def __init__(self, mac, radio=SX127X()):
        # super(Device, self).__init__()
        self.__device_class = None
        self.__mac = None
        self.__radio = None

        self.mac = mac
        self.radio = radio

    @property
    def device_class(self) -> DEVCLASS:
        return self.__device_class

    @device_class.setter
    def device_class(self, device_class: DEVCLASS):
        if self.__device_class is None:
            if isinstance(device_class, DEVCLASS):
                self.__device_class = device_class
            else:
                raise TypeError
        else:
            raise ValueError(f'{self}.__device_class already exists!')

    @property
    def mac(self) -> LoRaMAC:
        return self.__mac

    @mac.setter
    def mac(self, mac):
        if isinstance(mac, LoRaMAC):
            self.__mac = mac
        else:
            raise TypeError

    @property
    def radio(self) -> Radio:
        return self.__radio

    @radio.setter
    def radio(self, radio):
        if isinstance(radio, Radio):
            self.__radio = radio
        else:
            raise TypeError


class ClassA(Device):
    """ Class to define LoRaWAN Class A Device """

    def __init__(self, *args):
        super(ClassA, self).__init__(*args)
        self.device_class = DEVCLASS.CLASS_A


if __name__ == '__main__':
    loramac = LoRaMAC()
    device = ClassA(loramac)
