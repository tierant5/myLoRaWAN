import Device
from Keys import Keys
from LoRaPacket import LoRaPacket
from constants import ACTIVATION


class LoRaWAN(Device.ClassC):
    """ Class to unify LoRaWAN Stack """

    def __init__(self, activation=ACTIVATION.OTAA, *args):
        super(LoRaWAN, self).__init__(*args)
        self.__keys = None
        self.__activation = None
        self.__fcnt = None
        self.__rx_packet = None
        self.__tx_packet = None

        self.activation = activation

    def on_rx_done(self):
        super(LoRaWAN, self).on_rx_done()
        self.rx_packet = LoRaPacket(self.rx_payload)
        self.rx_packet.decompose(self.keys)

    def on_tx_done(self):
        super(LoRaWAN, self).on_tx_done()

    def send_packet(self):
        self.tx_packet.compose(self.keys)
        self.tx(self.tx_packet.data_list)

    @property
    def keys(self) -> Keys:
        return self.__keys

    @keys.setter
    def keys(self, keys):
        if isinstance(keys, Keys):
            self.__keys = keys
        else:
            raise TypeError

    @property
    def activation(self) -> ACTIVATION:
        return self.__activation

    @activation.setter
    def activation(self, activation):
        if isinstance(activation, ACTIVATION):
            self.__activation = activation
        else:
            raise TypeError

    @property
    def fcnt(self) -> int:
        return self.__fcnt

    @fcnt.setter
    def fcnt(self, fcnt):
        if isinstance(fcnt, int):
            self.__fcnt = fcnt
        else:
            raise TypeError

    @property
    def rx_packet(self) -> LoRaPacket:
        self.__rx_packet

    @rx_packet.setter
    def rx_packet(self, rx_packet):
        if isinstance(rx_packet, LoRaPacket):
            self.__packet = rx_packet
        else:
            raise TypeError

    @property
    def tx_packet(self) -> LoRaPacket:
        self.__tx_packet

    @tx_packet.setter
    def tx_packet(self, tx_packet):
        if isinstance(tx_packet, LoRaPacket):
            self.__packet = tx_packet
        else:
            raise TypeError
