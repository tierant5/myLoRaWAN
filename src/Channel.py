from constants import KEYS, CHMASK, UPLINK, DOWNLINK, DR, BW, BAND, get_enum


class ChannelMaskCntl(object):
    """Class to define LoRaWAN Channel Mask Control Type"""

    def __init__(self, cntl: CHMASK, **kwargs):
        self.__cntl = None
        self.__cntl_type = None
        self.__min_channel = None
        self.__max_channel = None
        self.__min_band = None
        self.__max_band = None
        self.__channel_list = None
        self.__band_list = None

        self.cntl = cntl
        for key, value in kwargs.items():
            if key == KEYS.CHMASK_TYPE.value:
                self.cntl_type = value
            elif key == KEYS.CHMASK_MIN_CH.value:
                self.min_channel = value
            elif key == KEYS.CHMASK_MAX_CH.value:
                self.max_channel = value
            elif key == KEYS.CHMASK_MIN_BAND.value:
                self.min_band = value
            elif key == KEYS.CHMASK_MAX_BAND.value:
                self.max_band = value
            else:
                raise KeyError

        if self.min_channel is not None and self.max_channel is not None:
            self.__channel_list = [
                UPLINK(ch) for ch in range(
                    self.min_channel.value, self.max_channel.value + 1
                )
            ]
        elif self.min_band is not None and self.max_band is not None:
            self.__band_list = [
                BAND(band) for band in range(
                    self.min_band.value, self.max_band.value + 1
                )
            ]
        else:
            raise ValueError

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
                CHMASK.TYPE_BAND,
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
    def min_channel(self) -> UPLINK:
        return self.__min_channel

    @min_channel.setter
    def min_channel(self, min_channel):
        if isinstance(min_channel, UPLINK):
            self.__min_channel = min_channel
        elif isinstance(min_channel, str):
            self.__min_channel = get_enum(UPLINK, min_channel)
        else:
            raise TypeError

    @property
    def max_channel(self) -> UPLINK:
        return self.__max_channel

    @max_channel.setter
    def max_channel(self, max_channel):
        if isinstance(max_channel, UPLINK):
            self.__max_channel = max_channel
        elif isinstance(max_channel, str):
            self.__max_channel = get_enum(UPLINK, max_channel)
        else:
            raise TypeError

    @property
    def channel_list(self) -> list:
        return self.__channel_list

    @property
    def min_band(self) -> BAND:
        return self.__min_band

    @min_band.setter
    def min_band(self, min_band):
        if isinstance(min_band, BAND):
            self.__min_band = min_band
        elif isinstance(min_band, str):
            self.__min_band = get_enum(BAND, min_band)
        else:
            raise TypeError

    @property
    def max_band(self) -> BAND:
        return self.__max_band

    @max_band.setter
    def max_band(self, max_band):
        if isinstance(max_band, BAND):
            self.__max_band = max_band
        elif isinstance(max_band, str):
            self.__max_band = get_enum(BAND, max_band)
        else:
            raise TypeError

    @property
    def band_list(self) -> list:
        return self.__band_list


class Channel(object):
    """ Class to define a LoRa Channel """

    def __init__(self, channel, **kwargs):
        self.__channel = None
        self.__frequency = None
        self.__min_data_rate = None
        self.__max_data_rate = None
        self.__bandwidth = None
        self.__data_rates = None

        self.channel = channel

        for key, value in kwargs.items():
            if key == KEYS.CH_FREQ.value:
                self.frequency = value
            elif key == KEYS.CH_MIN_DR.value:
                self.min_data_rate = value
            elif key == KEYS.CH_MAX_DR.value:
                self.max_data_rate = value
            elif key == KEYS.CH_BW.value:
                self.bandwidth = value
            else:
                raise KeyError

        if self.min_data_rate is not None and self.max_data_rate is not None:
            self.__data_rates = [
                DR(dr) for dr in range(
                    self.min_data_rate.value, self.max_data_rate.value + 1)
            ]
        else:
            raise ValueError

    @property
    def channel(self):
        return self.__channel

    @channel.setter
    def channel(self, channel):
        if isinstance(channel, (UPLINK, DOWNLINK)):
            self.__channel = channel
        else:
            raise TypeError(f'Type {type(channel)} is not allowed!')

    @property
    def frequency(self) -> int:
        return self.__frequency

    @frequency.setter
    def frequency(self, frequency):
        if isinstance(frequency, int):
            self.__frequency = frequency
        else:
            raise TypeError

    @property
    def min_data_rate(self) -> DR:
        return self.__min_data_rate

    @min_data_rate.setter
    def min_data_rate(self, min_data_rate):
        if isinstance(min_data_rate, DR):
            self.__min_data_rate = min_data_rate
        elif isinstance(min_data_rate, str):
            self.__min_data_rate = get_enum(DR, min_data_rate)
        else:
            raise TypeError

    @property
    def max_data_rate(self) -> DR:
        return self.__max_data_rate

    @max_data_rate.setter
    def max_data_rate(self, max_data_rate):
        if isinstance(max_data_rate, DR):
            self.__max_data_rate = max_data_rate
        elif isinstance(max_data_rate, str):
            self.__max_data_rate = get_enum(DR, max_data_rate)
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
    def data_rates(self) -> list:
        return self.__data_rates


class Band(object):
    """" Class to define a LoRa Band """

    def __init__(self, band, **kwargs):
        self.__band = None
        self.__min_channel = None
        self.__max_channel = None
        self.__channel_list = None

        self.band = band

        for key, value in kwargs.items():
            if key == KEYS.BAND_MIN_CH.value:
                self.min_channel = value
            elif key == KEYS.BAND_MAX_CH.value:
                self.max_channel = value
            else:
                raise KeyError

        if self.min_channel is not None and self.max_channel is not None:
            self.__channel_list = [
                UPLINK(ch) for ch in range(
                    self.min_channel.value, self.max_channel.value + 1
                )
            ]

    @property
    def band(self) -> BAND:
        return self.__band

    @band.setter
    def band(self, band):
        if isinstance(band, BAND):
            self.__band = band
        else:
            raise TypeError

    @property
    def min_channel(self) -> UPLINK:
        return self.__min_channel

    @min_channel.setter
    def min_channel(self, min_channel):
        if isinstance(min_channel, UPLINK):
            self.__min_channel = min_channel
        elif isinstance(min_channel, str):
            self.__min_channel = get_enum(UPLINK, min_channel)
        else:
            raise TypeError

    @property
    def max_channel(self) -> UPLINK:
        return self.__max_channel

    @max_channel.setter
    def max_channel(self, max_channel):
        if isinstance(max_channel, UPLINK):
            self.__max_channel = max_channel
        elif isinstance(max_channel, str):
            self.__max_channel = get_enum(UPLINK, max_channel)
        else:
            raise TypeError

    @property
    def channel_list(self) -> list:
        return self.__channel_list
