from constants import BW, DR, KEYS, SF
from helpers import get_enum


class DataRate(object):
    """ Class to define a DataRate for a region. """

    def __init__(self, data_rate: DR, params: dict):
        self.__data_rate = None
        self.__dr_type = None
        self.__spreading_factor = None
        self.__bandwidth = None
        self.__bit_rate = None
        self.__dr_next = None
        self.__max_m_payload = None
        self.__max_n_payload = None

        self.data_rate = data_rate
        for key, value in params.items():
            if key == KEYS.DR_TYPE.value:
                self.dr_type = value
            elif key == KEYS.DR_SF.value:
                self.spreading_factor = value
            elif key == KEYS.DR_BW.value:
                self.bandwidth = value
            elif key == KEYS.DR_BR.value:
                self.bit_rate = value
            elif key == KEYS.DR_NEXT.value:
                self.dr_next = value
            elif key == KEYS.DR_MAX_M_PAYLOAD.value:
                self.max_m_payload = value
            elif key == KEYS.DR_MAX_N_PAYLOAD.value:
                self.max_n_payload = value
            else:
                raise KeyError

    @property
    def data_rate(self) -> DR:
        return self.__data_rate

    @data_rate.setter
    def data_rate(self, data_rate):
        if isinstance(data_rate, DR):
            self.__data_rate = data_rate
        elif isinstance(data_rate, str):
            self.__data_rate = get_enum(DR, data_rate)
        else:
            raise TypeError

    @property
    def dr_type(self) -> DR:
        return self.__dr_type

    @dr_type.setter
    def dr_type(self, dr_type):
        if isinstance(dr_type, DR):
            if dr_type in [DR.TYPE_LORA, DR.TYPE_LRFHSS, DR.TYPE_RFU]:
                self.__dr_type = dr_type
            else:
                raise ValueError
        elif isinstance(dr_type, str):
            self.__dr_type = get_enum(DR, f'TYPE_{dr_type.upper()}')
        else:
            raise TypeError

    @property
    def spreading_factor(self) -> SF:
        return self.__spreading_factor

    @spreading_factor.setter
    def spreading_factor(self, spreading_factor):
        if isinstance(spreading_factor, SF):
            self.__spreading_factor = spreading_factor
        elif isinstance(spreading_factor, str):
            self.__spreading_factor = get_enum(SF, spreading_factor)
        else:
            raise TypeError

    @property
    def bandwidth(self) -> BW:
        return self.__bandwidth

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        if isinstance(bandwidth, BW):
            self.__bandwidth = bandwidth
        elif isinstance(bandwidth, str):
            self.__bandwidth = get_enum(BW, bandwidth)
        else:
            raise TypeError

    @property
    def bit_rate(self) -> int:
        return self.__bit_rate

    @bit_rate.setter
    def bit_rate(self, bit_rate):
        if isinstance(bit_rate, int):
            self.__bit_rate = bit_rate
        else:
            raise TypeError

    @property
    def dr_next(self) -> DR:
        return self.__dr_next

    @dr_next.setter
    def dr_next(self, dr_next):
        if isinstance(dr_next, DR):
            self.__dr_next = dr_next
        elif isinstance(dr_next, str):
            if dr_next == 'NA':
                self.__dr_next = None
            else:
                self.__dr_next = get_enum(DR, dr_next)
        else:
            raise TypeError

    @property
    def max_m_payload(self) -> int:
        return self.__max_m_payload

    @max_m_payload.setter
    def max_m_payload(self, max_m_payload):
        if isinstance(max_m_payload, int):
            self.__max_m_payload = max_m_payload
        else:
            raise TypeError

    @property
    def max_n_payload(self) -> int:
        return self.__max_n_payload

    @max_n_payload.setter
    def max_n_payload(self, max_n_payload):
        if isinstance(max_n_payload, int):
            self.__max_n_payload = max_n_payload
        else:
            raise TypeError
