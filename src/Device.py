# from SX127x import LoRa
from constants import DEVCLASS, MODE
from LoRaMAC import LoRaMAC
from Radio import Radio, SX127X


class Device():
    """ Base Class of LoRaWAN Device """

    def __init__(self, mac, radio=SX127X()):
        # super(Device, self).__init__()
        self.__device_class = None
        self.__mac = None
        self.__radio = None
        self.__rx1_timeout_mode = None
        self.__rx2_timeout_mode = None

        self.rx1_timeout = False
        self.rx2_timeout = False
        self.mac = mac
        self.radio = radio

    def on_rx_done(self):
        self.rx1_timeout = False
        self.rx2_timeout = False

    def on_rx_timeout(self):
        if not self.rx1_timeout:
            self.rx1_timeout = True
            self.rx2_timeout = False
        elif not self.rx2_timeout:
            self.rx1_timeout = True
            self.rx2_timeout = True

    def on_tx_done(self):
        pass

    def tx(self):
        pass

    def rx(self):
        pass

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

    @property
    def rx1_timeout_mode(self) -> MODE:
        return self.__rx1_timeout_mode

    @rx1_timeout_mode.setter
    def rx1_timeout_mode(self, rx1_timeout_mode):
        if isinstance(rx1_timeout_mode, MODE):
            if rx1_timeout_mode in [MODE.RXCONT, MODE.STDBY]:
                self.__rx1_timeout_mode = rx1_timeout_mode
            else:
                raise ValueError(f'{rx1_timeout_mode} is not a supported mode')
        else:
            raise TypeError

    @property
    def rx2_timeout_mode(self) -> MODE:
        return self.__rx2_timeout_mode

    @rx2_timeout_mode.setter
    def rx2_timeout_mode(self, rx2_timeout_mode):
        if isinstance(rx2_timeout_mode, MODE):
            if rx2_timeout_mode in [MODE.RXCONT, MODE.SLEEP]:
                self.__rx2_timeout_mode = rx2_timeout_mode
            else:
                raise ValueError(f'{rx2_timeout_mode} is not a supported mode')
        else:
            raise TypeError


class ClassA(Device):
    """ Class to define LoRaWAN Class A Device """

    def __init__(self, *args):
        super(ClassA, self).__init__(*args)
        self.device_class = DEVCLASS.CLASS_A
        self.rx1_timeout_mode = MODE.STDBY
        self.rx2_timeout_mode = MODE.SLEEP


if __name__ == '__main__':
    loramac = LoRaMAC()
    device = ClassA(loramac)
