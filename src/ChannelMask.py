from constants import KEYS, CHMASK, get_enum


class ChannelMaskCntl(object):
    """Class to define LoRaWAN Channel Mask Control Type"""

    def __init__(self, cntl: CHMASK, params: dict):
        self.__cntl = None
        self.__cntl_type = None
        self.__min_channel = None
        self.__max_channel = None
        self.__channel_list = None

        self.cntl = cntl
        for key, value in params.items():
            if key == KEYS.CHMASK_TYPE.value:
                self.cntl_type = value
            elif key == KEYS.CHMASK_MIN.value:
                self.min_channel = value
            elif key == KEYS.CHMASK_MAX.value:
                self.max_channel = value
            else:
                raise KeyError

        if self.min_channel is not None and self.max_channel is not None:
            self.__channel_list = [
                ch for ch in range(self.min_channel, self.max_channel + 1)
            ]

    @property
    def cntl(self) -> CHMASK:
        return self.__cntl

    @cntl.setter
    def cntl(self, cntl):
        if isinstance(cntl, CHMASK):
            self.__cntl = cntl
        elif isinstance(cntl, str):
            self.__cntl = get_enum(CHMASK, cntl)
        else:
            raise TypeError

    @property
    def cntl_type(self) -> CHMASK:
        return self.__cntl_type

    @cntl_type.setter
    def cntl_type(self, cntl_type):
        if isinstance(cntl_type, CHMASK):
            if cntl_type in [
                CHMASK.TYPE_ALL_OFF,
                CHMASK.TYPE_ALL_ON,
                CHMASK.TYPE_BLOCK,
                CHMASK.TYPE_INDIVIDUAL,
            ]:
                self.__cntl_type = cntl_type
            else:
                raise ValueError
        elif isinstance(cntl_type, str):
            self.__cntl_type = get_enum(CHMASK, f"TYPE_{cntl_type.upper()}")
        else:
            raise TypeError

    @property
    def min_channel(self) -> int:
        return self.__min_channel

    @min_channel.setter
    def min_channel(self, min_channel):
        if isinstance(min_channel, int):
            self.__min_channel = min_channel
        else:
            raise TypeError

    @property
    def max_channel(self) -> int:
        return self.__max_channel

    @max_channel.setter
    def max_channel(self, max_channel):
        if isinstance(max_channel, int):
            self.__max_channel = max_channel
        else:
            raise TypeError

    @property
    def channel_list(self) -> list:
        return self.__channel_list
