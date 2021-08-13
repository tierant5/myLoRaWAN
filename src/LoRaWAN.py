import Device


class LoRaWAN(Device.ClassC):
    """ Class to unify LoRaWAN Stack """

    def __init__(self, *args):
        super(LoRaWAN, self).__init__(*args)
        self.__devaddr = None
        self.__nwkskey = None
        self.__appskey = None
        self.__devnonce = None
        self.__appeui = None
        self.__deveui = None
        self.__join_type = None
        self.__frame_cnt = None

    def on_rx_done(self):
        super(LoRaWAN, self).on_rx_done()

    def on_tx_done(self):
        super(LoRaWAN, self).on_tx_done()
