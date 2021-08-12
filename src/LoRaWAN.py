import Device


class LoRaWAN(Device.ClassC):
    """ Class to unify LoRaWAN Stack """

    def __init__(self, *args):
        super(LoRaWAN, self).__init__(*args)

    def on_rx_done(self):
        super(LoRaWAN, self).on_rx_done()

    def on_tx_done(self):
        super(LoRaWAN, self).on_tx_done()
