from constants import BW, KEYS, SF, MODE, CR, RADIO
from helpers import load_radio_json, get_enum


class Radio(object):
    """ Class to define a LoRa Radio """

    def __init__(self, **kwargs):
        self.__radio = None
        self.__min_tx_power = None
        self.__max_tx_power = None
        self.__bw_table = None
        self.__sf_table = None
        self.__mode_table = None
        self.__coding_rate_table = None

        for key, value in kwargs.items():
            if key == 'min_tx_power':
                self.min_tx_power = value
            elif key == 'max_tx_power':
                self.max_tx_power = value
            else:
                raise KeyError

    def load_parameters(self):
        json_data = load_radio_json(self.radio)
        self.bw_table = json_data[KEYS.RADIO_BW.value]
        self.sf_table = json_data[KEYS.RADIO_SF.value]
        self.mode_table = json_data[KEYS.RADIO_MODE.value]
        self.coding_rate_table = json_data[KEYS.RADIO_CODING_RATE.value]

    def dbm2code(self, dbm):
        pass

    def code2dbm(self, code):
        pass

    @property
    def radio(self) -> RADIO:
        return self.__radio

    @radio.setter
    def radio(self, radio):
        if isinstance(radio, RADIO):
            self.__radio = radio
        else:
            raise TypeError

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

    @property
    def bw_table(self) -> dict:
        return self.__bw_table

    @bw_table.setter
    def bw_table(self, bw_table):
        if isinstance(bw_table, dict):
            if self.__bw_table is None:
                self.__bw_table = {}
            else:
                raise ValueError
            for key, value in bw_table.items():
                bw = get_enum(BW, key)
                self.__bw_table[bw] = value
        else:
            raise TypeError

    @property
    def sf_table(self) -> dict:
        return self.__sf_table

    @sf_table.setter
    def sf_table(self, sf_table):
        if isinstance(sf_table, dict):
            if self.__sf_table is None:
                self.__sf_table = {}
            else:
                raise ValueError
            for key, value in sf_table.items():
                bw = get_enum(SF, key)
                self.__sf_table[bw] = value
        else:
            raise TypeError

    @property
    def mode_table(self) -> dict:
        return self.__mode_table

    @mode_table.setter
    def mode_table(self, mode_table):
        if isinstance(mode_table, dict):
            if self.__mode_table is None:
                self.__mode_table = {}
            else:
                raise ValueError
            for key, value in mode_table.items():
                bw = get_enum(MODE, key)
                self.__mode_table[bw] = value
        else:
            raise TypeError

    @property
    def coding_rate_table(self) -> dict:
        return self.__coding_rate_table

    @coding_rate_table.setter
    def coding_rate_table(self, coding_rate_table):
        if isinstance(coding_rate_table, dict):
            if self.__coding_rate_table is None:
                self.__coding_rate_table = {}
            else:
                raise ValueError
            for key, value in coding_rate_table.items():
                bw = get_enum(CR, key)
                self.__coding_rate_table[bw] = value
        else:
            raise TypeError


class SX127X(Radio):
    """ Class to define SX127X Radio """

    def __init__(self):
        super(SX127X, self).__init__(
            min_tx_power=5,
            max_tx_power=20
        )
        self.radio = RADIO.SX127X
        self.offset = 10.8
        self.step = 0.6
        self.freq_scale = 1e6

        self.load_parameters()

    def code2dbm(self, code):
        return (code*self.step) + self.offset

    def dbm2code(self, dbm):
        return round((dbm - self.offset) / self.step)
