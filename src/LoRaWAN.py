import Device
from Keys import Keys


class LoRaWAN(Device.ClassC):
    """ Class to unify LoRaWAN Stack """

    def __init__(self, *args):
        super(LoRaWAN, self).__init__(*args)
        self.__keys = None
        self.__join_type = None
        self.__frame_cnt = None

    def on_rx_done(self):
        super(LoRaWAN, self).on_rx_done()

    def on_tx_done(self):
        super(LoRaWAN, self).on_tx_done()

    @property
    def keys(self) -> Keys:
        return self.__keys

    @keys.setter
    def keys(self, keys):
        if isinstance(keys, Keys):
            self.__keys = keys
        else:
            raise TypeError
