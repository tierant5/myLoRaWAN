

class Radio(object):
    """ Class to define a LoRa Radio """

    def __init__(self, **kwargs):
        self.__min_tx_power = None
        self.__max_tx_power = None

        for key, value in kwargs.items():
            if key == 'min_tx_power':
                self.min_tx_power = value
            elif key == 'max_tx_power':
                self.max_tx_power = value
            else:
                raise KeyError

    def dbm2code(self, dbm):
        pass

    def code2dbm(self, code):
        pass

    @property
    def min_tx_power(self) -> int:
        return self.__min_tx_power

    @min_tx_power.setter
    def min_tx_power(self, min_tx_power):
        if isinstance(min_tx_power, int):
            self.__min_tx_power = min_tx_power
        else:
            return TypeError

    @property
    def max_tx_power(self) -> int:
        return self.__max_tx_power

    @max_tx_power.setter
    def max_tx_power(self, max_tx_power):
        if isinstance(max_tx_power, int):
            self.__max_tx_power = max_tx_power
        else:
            return TypeError


class SX127X(Radio):
    """ Class to define SX127X Radio """

    def __init__(self):
        super(SX127X, self).__init__(
            min_tx_power=5,
            max_tx_power=20
        )
        self.offset = 10.8
        self.step = 0.6

    def code2dbm(self, code):
        return (code*self.step) + self.offset

    def dbm2code(self, dbm):
        return round((dbm - self.offset) / self.step)
