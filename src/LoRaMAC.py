from Channel import Channel, ChannelMaskCntl, Band
from constants import (ACTIVATION, BW, CHMASK, CR, DEVCLASS, DR, KEYS, REGION,
                       SF, TXPOWER, RADIO, BAND, DOWNLINK, UPLINK, get_enum)
from DataRate import DataRate
from helpers import load_all_region_json, load_region_json
from Radio import Radio
from random import randint


class LoRaMAC:
    """Class to define the LoRa MAC Layer"""

    def __init__(
        self,
        region=REGION.US915,
        device_class=DEVCLASS.CLASS_A,
        adr=False,
        radio=RADIO.SX1276,
        tx_retries=1,
        band=BAND.BAND0,
        tx_power=None,
        public=False
    ):

        self.__preamble = None
        self.__power_mode = None
        self.__tx_iq = None
        self.__rx_iq = None
        self.__adr = None
        self.__public = None
        self.__max_fcnt_gap = None
        self.__adr_ack_limit = None
        self.__adr_ack_delay = None
        self.__downlink_dwell_time = None
        self.__uplink_dwell_time = None
        self.__cflist_type_supported = None
        self.__max_eirp = None
        self.__radio = None

        # Device Params
        self.__region = None
        self.__ism_id = None
        self.__device_class = None
        self.__activation = None
        self.__txparamsetupreq_support = None
        self.__band = None

        # Lookups
        self.__data_rates = None
        self.__mandatory_data_rate = None
        self.__optional_data_rate = None
        self.__channel_mask_cntl_table = None
        self.__uplink_channels = None
        self.__downlink_channels = None
        self.__bands = None
        self.__supported_bw = None
        self.__join_request_data_rates = None

        # Radio Params
        self.__coding_rate = None
        self.__duty_cycle = None
        self.__dwell_time = None

        # TX Params
        self.__tx_channel = None
        self.__tx_data_rate = None
        self.__tx_powers = None
        self.__tx_retries = None
        self.__retransmit_timeout = None

        # RX1 Params
        self.__rx1_channel = None
        self.__rx1_data_rate = None
        self.__rx1droffset = None
        self.__rx1_received = None
        self.__rx_delay1 = None
        self.__rx_delay2 = None
        self.__default_rx1droffset = None
        self.__allowed_rx1droffset = None
        self.__rx1droffset_table = None

        # RX2 Params
        self.__rx2_channel = None
        self.__rx2_data_rate = None
        self.__default_rx2_data_rate = None
        self.__default_rx2_channel = None

        # Join-Request Params
        self.__join_request_data_rate = None

        # Join-Accept Params
        self.__join_accept_delay1 = None
        self.__join_accept_delay2 = None

        # Class B Device Params
        self.__ping_slot_periodicity = None
        self.__ping_slot_datarate = None
        self.__ping_slot_channel = None
        self.__class_b_resp_timeout = None

        # Class C Device Params
        self.__class_c_resp_timeout = None

        # Set self.****
        self.region = region
        self.adr = adr
        self.radio = radio
        self.device_class = device_class
        self.tx_retries = tx_retries
        # TODO Check if previous settings are present
        self.load_defaults()
        self.set_defaults(band, tx_power)

    def load_defaults(self):
        self.load_all_region_defaults()
        self.load_region_defaults()

    def load_all_region_defaults(self):
        self.decompose_all_region_defaults(load_all_region_json())

    def load_region_defaults(self):
        self.decompose_region_defaults(load_region_json(self.region))

    def decompose_all_region_defaults(self, json_data):
        self.rx_delay1 = json_data[KEYS.RECEIVE_DELAY1.value]
        self.rx_delay2 = json_data[KEYS.RECEIVE_DELAY2.value]
        self.join_accept_delay1 = json_data[KEYS.JOIN_ACCEPT_DELAY1.value]
        self.join_accept_delay2 = json_data[KEYS.JOIN_ACCEPT_DELAY2.value]
        self.max_fcnt_gap = json_data[KEYS.MAX_FCNT_GAP.value]
        self.adr_ack_limit = json_data[KEYS.ADR_ACK_LIMIT.value]
        self.adr_ack_delay = json_data[KEYS.ADR_ACK_DELAY.value]
        self.retransmit_timeout = json_data[KEYS.RETRANSMIT_TIMEOUT.value]
        self.downlink_dwell_time = json_data[KEYS.DOWNLINK_DWELL_TIME.value]
        self.ping_slot_periodicity = json_data[KEYS.PING_SLOT_PERIODICITY.value]    # noqa: E501
        self.class_b_resp_timeout = json_data[KEYS.CLASS_B_RESP_TIMEOUT.value]
        self.class_c_resp_timeout = json_data[KEYS.CLASS_C_RESP_TIMEOUT.value]

    def decompose_region_defaults(self, json_data):
        self.ism_id = json_data[KEYS.ISM_ID.value]
        self.supported_bw = json_data[KEYS.SUPPORTED_BW.value]
        self.join_request_data_rates = json_data[KEYS.JOIN_REQ_DATA_RATES.value]    # noqa: E501
        self.cflist_type_supported = json_data[KEYS.CFLIST_TYPE_SUPPORTED.value]    # noqa: E501
        self.mandatory_data_rate = json_data[KEYS.MANDATORY_DATA_RATE.value]
        self.optional_data_rate = json_data[KEYS.OPTIONAL_DATA_RATE.value]
        self.txparamsetupreq_support = json_data[KEYS.TXPARAMSETUPREQ_SUPPORT.value]    # noqa: E501
        self.max_eirp = json_data[KEYS.MAX_EIRP.value]
        self.allowed_rx1droffset = json_data[KEYS.ALLOWED_RX1DROFFSET.value]
        self.default_rx1droffset = json_data[KEYS.DEFAULT_RX1DROFFSET.value]
        self.default_rx2_data_rate = json_data[KEYS.DEFAULT_RX2_DATA_RATE.value]    # noqa: E501
        self.default_rx2_channel = json_data[KEYS.DEFAULT_RX2_CH.value]    # noqa: E501
        self.duty_cycle = json_data[KEYS.DUTY_CYCLE.value]
        self.dwell_time = json_data[KEYS.DWELL_TIME.value]
        self.coding_rate = json_data[KEYS.CODING_RATE.value]
        self.data_rates = json_data[KEYS.DATA_RATES.value]
        self.tx_powers = json_data[KEYS.TX_POWERS.value]
        self.channel_mask_cntl_table = json_data[KEYS.CHANNEL_MASK_CNTL_TABLE.value]    # noqa: E501
        self.rx1droffset_table = json_data[KEYS.RX1DROFFSET_TABLE.value]
        self.uplink_channels = json_data[KEYS.UPLINK_CH.value]
        self.downlink_channels = json_data[KEYS.DOWNLINK_CH.value]
        self.bands = json_data[KEYS.BANDS.value]

    def set_defaults(self, band, tx_power):
        self.band = band
        rand_ch_index = randint(0, len(self.band.channel_list) - 1)
        self.tx_channel = self.band.channel_list[rand_ch_index]
        self.tx_data_rate = self.tx_channel.data_rates[0]
        self.rx1droffset = self.default_rx1droffset
        self.rx2_channel = self.default_rx2_channel
        self.rx2_data_rate = self.default_rx2_data_rate

    ###########################################################################
    # Properties
    ###########################################################################
    @property
    def region(self) -> REGION:
        return self.__region

    @region.setter
    def region(self, region: REGION):
        if isinstance(region, REGION):
            self.__region = region
        else:
            raise TypeError

    @property
    def adr(self) -> bool:
        return self.__adr

    @adr.setter
    def adr(self, adr: bool):
        if isinstance(adr, bool):
            self.__adr = adr
        else:
            raise TypeError

    @property
    def public(self) -> bool:
        return self.__public

    @public.setter
    def public(self, public: bool):
        if isinstance(public, bool):
            self.__public = public
        else:
            raise TypeError

    @property
    def tx_retries(self) -> int:
        return self.__tx_retries

    @tx_retries.setter
    def tx_retries(self, tx_retries: int):
        if isinstance(tx_retries, int):
            self.__tx_retries = tx_retries
        else:
            raise TypeError

    @property
    def device_class(self) -> DEVCLASS:
        return self.__device_class

    @device_class.setter
    def device_class(self, device_class: DEVCLASS):
        if isinstance(device_class, DEVCLASS):
            self.__device_class = device_class
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
    def spreading_factor(self) -> SF:
        return self.__spreading_factor

    @spreading_factor.setter
    def spreading_factor(self, spreading_factor):
        if isinstance(spreading_factor, SF):
            self.__spreading_factor = spreading_factor
        else:
            raise TypeError

    @property
    def bandwidth(self) -> BW:
        return self.__bandwidth

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        if isinstance(bandwidth, BW):
            self.__bandwidth = bandwidth
        else:
            raise TypeError

    @property
    def rx_delay1(self) -> int:
        return self.__rx_delay1

    @rx_delay1.setter
    def rx_delay1(self, rx_delay1: int):
        if isinstance(rx_delay1, int):
            self.__rx_delay1 = rx_delay1
        else:
            raise TypeError

    @property
    def rx_delay2(self) -> int:
        return self.__rx_delay2

    @rx_delay2.setter
    def rx_delay2(self, rx_delay2: int):
        if isinstance(rx_delay2, int):
            self.__rx_delay2 = rx_delay2
        else:
            raise TypeError

    @property
    def join_accept_delay1(self) -> int:
        return self.__join_accept_delay1

    @join_accept_delay1.setter
    def join_accept_delay1(self, join_accept_delay1: int):
        if isinstance(join_accept_delay1, int):
            self.__join_accept_delay1 = join_accept_delay1
        else:
            raise TypeError

    @property
    def join_accept_delay2(self) -> int:
        return self.__join_accept_delay2

    @join_accept_delay2.setter
    def join_accept_delay2(self, join_accept_delay2: int):
        if isinstance(join_accept_delay2, int):
            self.__join_accept_delay2 = join_accept_delay2
        else:
            raise TypeError

    @property
    def max_fcnt_gap(self) -> int:
        return self.__max_fcnt_gap

    @max_fcnt_gap.setter
    def max_fcnt_gap(self, max_fcnt_gap: int):
        if isinstance(max_fcnt_gap, int):
            self.__max_fcnt_gap = max_fcnt_gap
        else:
            raise TypeError

    @property
    def adr_ack_limit(self) -> int:
        return self.__adr_ack_limit

    @adr_ack_limit.setter
    def adr_ack_limit(self, adr_ack_limit: int):
        if isinstance(adr_ack_limit, int):
            self.__adr_ack_limit = adr_ack_limit
        else:
            raise TypeError

    @property
    def adr_ack_delay(self) -> int:
        return self.__adr_ack_delay

    @adr_ack_delay.setter
    def adr_ack_delay(self, adr_ack_delay: int):
        if isinstance(adr_ack_delay, int):
            self.__adr_ack_delay = adr_ack_delay
        else:
            raise TypeError

    @property
    def retransmit_timeout(self) -> int:
        return self.__retransmit_timeout

    @retransmit_timeout.setter
    def retransmit_timeout(self, retransmit_timeout: int):
        if isinstance(retransmit_timeout, int):
            self.__retransmit_timeout = retransmit_timeout
        else:
            raise TypeError

    @property
    def downlink_dwell_time(self) -> int:
        return self.__downlink_dwell_time

    @downlink_dwell_time.setter
    def downlink_dwell_time(self, downlink_dwell_time: int):
        if isinstance(downlink_dwell_time, int):
            self.__downlink_dwell_time = downlink_dwell_time
        else:
            raise TypeError

    @property
    def ping_slot_periodicity(self) -> int:
        return self.__ping_slot_periodicity

    @ping_slot_periodicity.setter
    def ping_slot_periodicity(self, ping_slot_periodicity: int):
        if isinstance(ping_slot_periodicity, int):
            self.__ping_slot_periodicity = ping_slot_periodicity
        else:
            raise TypeError

    @property
    def class_b_resp_timeout(self) -> int:
        return self.__class_b_resp_timeout

    @class_b_resp_timeout.setter
    def class_b_resp_timeout(self, class_b_resp_timeout: int):
        if isinstance(class_b_resp_timeout, int):
            self.__class_b_resp_timeout = class_b_resp_timeout
        else:
            raise TypeError

    @property
    def class_c_resp_timeout(self) -> int:
        return self.__class_c_resp_timeout

    @class_c_resp_timeout.setter
    def class_c_resp_timeout(self, class_c_resp_timeout: int):
        if isinstance(class_c_resp_timeout, int):
            self.__class_c_resp_timeout = class_c_resp_timeout
        else:
            raise TypeError

    @property
    def ism_id(self) -> str:
        return self.__ism_id

    @ism_id.setter
    def ism_id(self, ism_id):
        if isinstance(ism_id, str):
            self.__ism_id = ism_id
        else:
            raise TypeError

    @property
    def supported_bw(self) -> list:
        return self.__supported_bw

    @supported_bw.setter
    def supported_bw(self, supported_bw):
        if isinstance(supported_bw, list):
            if self.__supported_bw is None:
                self.__supported_bw = []
            for bw in supported_bw:
                self.__supported_bw.append(get_enum(BW, bw))
        else:
            raise TypeError

    @property
    def join_request_data_rates(self) -> dict:
        return self.__join_request_data_rates

    @join_request_data_rates.setter
    def join_request_data_rates(self, join_request_data_rates):
        if isinstance(join_request_data_rates, dict):
            if self.__join_request_data_rates is None:
                self.__join_request_data_rates = {}
                for bw, dr in join_request_data_rates.items():
                    self.__join_request_data_rates[get_enum(BW, bw)] = get_enum(DR, dr)  # noqa: E501
            else:
                raise ValueError(f"{self}.join_request_data_rates already exists!")  # noqa: E501
        else:
            raise TypeError

    @property
    def cflist_type_supported(self) -> int:
        return self.__cflist_type_supported

    @cflist_type_supported.setter
    def cflist_type_supported(self, cflist_type_supported):
        if isinstance(cflist_type_supported, int):
            self.__cflist_type_supported = cflist_type_supported
        else:
            raise TypeError

    @property
    def mandatory_data_rate(self) -> list:
        return self.__mandatory_data_rate

    @mandatory_data_rate.setter
    def mandatory_data_rate(self, mandatory_data_rate):
        if isinstance(mandatory_data_rate, list):
            if self.__mandatory_data_rate is None:
                self.__mandatory_data_rate = []
            else:
                raise ValueError(f"{self}.manadatory_data_rate already exists!")    # noqa: E501
            for dr in mandatory_data_rate:
                self.__mandatory_data_rate.append(get_enum(DR, dr))

    @property
    def optional_data_rate(self) -> list:
        return self.__optional_data_rate

    @optional_data_rate.setter
    def optional_data_rate(self, optional_data_rate):
        if isinstance(optional_data_rate, list):
            if self.__optional_data_rate is None:
                self.__optional_data_rate = []
            else:
                raise ValueError(f"{self}.optional_data_rate already exists!")
            for dr in optional_data_rate:
                self.__optional_data_rate.append(get_enum(DR, dr))
        else:
            raise TypeError

    @property
    def txparamsetupreq_support(self) -> bool:
        return self.__txparamsetupreq_support

    @txparamsetupreq_support.setter
    def txparamsetupreq_support(self, txparamsetupreq_support):
        if isinstance(txparamsetupreq_support, bool):
            self.__txparamsetupreq_support = txparamsetupreq_support
        else:
            raise TypeError

    @property
    def max_eirp(self) -> int:
        return self.__max_eirp

    @max_eirp.setter
    def max_eirp(self, max_eirp):
        if isinstance(max_eirp, int):
            self.__max_eirp = max_eirp
        else:
            raise TypeError

    @property
    def default_rx1droffset(self) -> int:
        return self.__default_rx1droffset

    @default_rx1droffset.setter
    def default_rx1droffset(self, default_rx1droffset):
        if isinstance(default_rx1droffset, int):
            self.__default_rx1droffset = default_rx1droffset
        else:
            raise TypeError

    @property
    def allowed_rx1droffset(self) -> list:
        return self.__allowed_rx1droffset

    @allowed_rx1droffset.setter
    def allowed_rx1droffset(self, allowed_rx1droffset):
        if isinstance(allowed_rx1droffset, list):
            if len(allowed_rx1droffset) != 0:
                if isinstance(allowed_rx1droffset[0], int):
                    self.__allowed_rx1droffset = allowed_rx1droffset
                else:
                    raise TypeError
            else:
                raise ValueError("Provided data is empty")
        else:
            raise TypeError

    @property
    def default_rx2_data_rate(self) -> DR:
        return self.__default_rx2_data_rate

    @default_rx2_data_rate.setter
    def default_rx2_data_rate(self, default_rx2_data_rate):
        if isinstance(default_rx2_data_rate, DR):
            self.__default_rx2_data_rate = default_rx2_data_rate
        elif isinstance(default_rx2_data_rate, str):
            self.__default_rx2_data_rate = get_enum(DR, default_rx2_data_rate)
        else:
            raise TypeError

    @property
    def default_rx2_channel(self) -> DOWNLINK:
        return self.__default_rx2_channel

    @default_rx2_channel.setter
    def default_rx2_channel(self, default_rx2_channel):
        if isinstance(default_rx2_channel, DOWNLINK):
            self.__default_rx2_channel = default_rx2_channel
        elif isinstance(default_rx2_channel, str):
            self.__default_rx2_channel = get_enum(
                DOWNLINK, default_rx2_channel
            )
        else:
            raise TypeError

    @property
    def duty_cycle(self) -> bool:
        return self.__duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, duty_cycle):
        if isinstance(duty_cycle, bool):
            self.__duty_cycle = duty_cycle
        else:
            raise TypeError

    @property
    def dwell_time(self) -> float:
        return self.__dwell_time

    @dwell_time.setter
    def dwell_time(self, dwell_time: float):
        if isinstance(dwell_time, float):
            self.__dwell_time = dwell_time
        else:
            raise TypeError

    @property
    def coding_rate(self) -> CR:
        return self.__coding_rate

    @coding_rate.setter
    def coding_rate(self, coding_rate):
        if isinstance(coding_rate, CR):
            self.__coding_rate = coding_rate
        elif isinstance(coding_rate, str):
            self._coding_rate = get_enum(CR, coding_rate)
        else:
            raise TypeError

    @property
    def data_rates(self) -> dict:
        return self.__data_rates

    @data_rates.setter
    def data_rates(self, data_rates: dict):
        if isinstance(data_rates, dict):
            if self.__data_rates is None:
                self.__data_rates = {}
                for key, value in data_rates.items():
                    dr = get_enum(DR, key)
                    self.__data_rates[dr] = DataRate(dr, value)
            else:
                raise ValueError(f"{self}.data_rates is not empty!")
        else:
            raise TypeError

    @property
    def tx_powers(self) -> dict:
        return self.__tx_powers

    @tx_powers.setter
    def tx_powers(self, tx_powers):
        if isinstance(tx_powers, dict):
            if self.__tx_powers is None:
                self.__tx_powers = {}
                for key, value in tx_powers.items():
                    self.__tx_powers[get_enum(TXPOWER, key)] = value
            else:
                raise ValueError(f"{self}.tx_powers is not empty!")
        else:
            raise TypeError

    @property
    def channel_mask_cntl_table(self) -> dict:
        return self.__channel_mask_cntl_table

    @channel_mask_cntl_table.setter
    def channel_mask_cntl_table(self, channel_mask_cntl_table: dict):
        if isinstance(channel_mask_cntl_table, dict):
            if self.__channel_mask_cntl_table is None:
                self.__channel_mask_cntl_table = {}
                for key, value in channel_mask_cntl_table.items():
                    cntl = get_enum(CHMASK, key)
                    self.__channel_mask_cntl_table[cntl] = ChannelMaskCntl(cntl, **value)   # noqa: E501
            else:
                raise ValueError(f"{self}.channel_mask_cntl_table is not empty!")   # noqa: E501
        else:
            raise TypeError

    @property
    def rx1droffset_table(self) -> dict:
        return self.__rx1droffset_table

    @rx1droffset_table.setter
    def rx1droffset_table(self, rx1droffset_table):
        if isinstance(rx1droffset_table, dict):
            if self.__rx1droffset_table is None:
                self.__rx1droffset_table = {}
                for key, value in rx1droffset_table.items():
                    dr = get_enum(DR, key)
                    drs = [get_enum(DR, item) for item in value]
                    self.__rx1droffset_table[dr] = drs
            else:
                raise ValueError(f"{self}.rx1droffset_table is not empty!")
        else:
            raise TypeError

    @property
    def uplink_channels(self) -> dict:
        return self.__uplink_channels

    @uplink_channels.setter
    def uplink_channels(self, uplink_channels):
        if isinstance(uplink_channels, dict):
            if self.__uplink_channels is None:
                self.__uplink_channels = {}
                for key, value in uplink_channels.items():
                    ch = get_enum(UPLINK, key)
                    self.__uplink_channels[ch] = Channel(ch, **value)
            else:
                raise ValueError(f"{self}.uplink_channels is not empty!")
        else:
            raise TypeError

    @property
    def downlink_channels(self) -> dict:
        return self.__downlink_channels

    @downlink_channels.setter
    def downlink_channels(self, downlink_channels):
        if isinstance(downlink_channels, dict):
            if self.__downlink_channels is None:
                self.__downlink_channels = {}
                for key, value in downlink_channels.items():
                    ch = get_enum(DOWNLINK, key)
                    self.__downlink_channels[ch] = Channel(ch, **value)
            else:
                raise ValueError(f"{self}.downlink_channels is not empty!")
        else:
            raise TypeError

    @property
    def bands(self) -> dict:
        return self.__bands

    @bands.setter
    def bands(self, bands):
        if isinstance(bands, dict):
            if self.__bands is None:
                self.__bands = {}
                for key, value in bands.items():
                    band = get_enum(BAND, key)
                    self.__bands[band] = Band(band, **value)
            else:
                raise ValueError(f"{self}.bands is not empty!")
        else:
            raise TypeError

    @property
    def tx_channel(self) -> Channel:
        return self.__tx_channel

    @tx_channel.setter
    def tx_channel(self, tx_channel):
        if isinstance(tx_channel, UPLINK):
            self.__tx_channel = self.uplink_channels[tx_channel]
            rx_channel_num = tx_channel.value % 8
            self.rx1_channel = DOWNLINK(rx_channel_num)
        else:
            raise TypeError

    @property
    def rx1_channel(self) -> Channel:
        return self.__rx1_channel

    @rx1_channel.setter
    def rx1_channel(self, rx1_channel):
        if isinstance(rx1_channel, DOWNLINK):
            self.__rx1_channel = self.downlink_channels[rx1_channel]
        else:
            raise TypeError

    @property
    def rx2_channel(self) -> Channel:
        return self.__rx2_channel

    @rx2_channel.setter
    def rx2_channel(self, rx2_channel):
        if isinstance(rx2_channel, DOWNLINK):
            self.__rx2_channel = self.downlink_channels[rx2_channel]
        else:
            raise TypeError

    @property
    def tx_data_rate(self) -> DataRate:
        return self.__tx_data_rate

    @tx_data_rate.setter
    def tx_data_rate(self, tx_data_rate):
        if self.tx_channel is not None:
            if isinstance(tx_data_rate, DR):
                if tx_data_rate in self.tx_channel.data_rates:
                    self.__tx_data_rate = self.data_rates[tx_data_rate]
                else:
                    raise ValueError(f"{tx_data_rate} not in allowed data rates for tx_channel")     # noqa: E501
            else:
                raise TypeError
        else:
            raise ValueError(f"{self}.tx_channel is not set!")

    @property
    def rx1_data_rate(self) -> DataRate:
        return self.__rx1_data_rate

    @rx1_data_rate.setter
    def rx1_data_rate(self, rx1_data_rate):
        if self.rx1_channel is not None:
            if isinstance(rx1_data_rate, DR):
                if rx1_data_rate in self.rx1_channel.data_rates:
                    self.__rx1_data_rate = self.data_rates[rx1_data_rate]
                else:
                    raise ValueError(f"{rx1_data_rate} not in allowed data rates for rx1_channel")     # noqa: E501
            else:
                raise TypeError
        else:
            raise ValueError(f"{self}.rx1_channel is not set!")

    @property
    def rx2_data_rate(self) -> DataRate:
        return self.__rx2_data_rate

    @rx2_data_rate.setter
    def rx2_data_rate(self, rx2_data_rate):
        if self.rx2_channel is not None:
            if isinstance(rx2_data_rate, DR):
                if rx2_data_rate in self.rx2_channel.data_rates:
                    self.__rx2_data_rate = self.data_rates[rx2_data_rate]
                else:
                    raise ValueError(f"{rx2_data_rate} not in allowed data rates for rx2_channel")     # noqa: E501
            else:
                raise TypeError
        else:
            raise ValueError(f"{self}.rx2_channel is not set!")

    @property
    def join_request_data_rate(self) -> DataRate:
        return self.__join_request_data_rate

    @join_request_data_rate.setter
    def join_request_data_rate(self, join_request_data_rate):
        if self.tx_channel is not None:
            if isinstance(join_request_data_rate, DR):
                if join_request_data_rate in self.tx_channel.data_rates:
                    self.__join_request_data_rate = self.data_rates[join_request_data_rate]     # noqa: E501
                else:
                    raise ValueError(f"{join_request_data_rate} not in allowed data rates for tx_channel")     # noqa: E501
            else:
                raise TypeError
        else:
            raise ValueError(f"{self}.tx_channel is not set!")

    @property
    def rx1droffset(self) -> int:
        return self.__rx1droffset

    @rx1droffset.setter
    def rx1droffset(self, rx1droffset):
        if self.tx_data_rate is not None:
            if isinstance(rx1droffset, int):
                if rx1droffset in self.allowed_rx1droffset:
                    self.__rx1droffset = rx1droffset
                    self.rx1_data_rate = self.rx1droffset_table[self.tx_data_rate.datarate][rx1droffset]    # noqa: E501
                else:
                    raise ValueError(f"{rx1droffset} is not an allowed rx1droffset")    # noqa: E501
            else:
                raise TypeError
        else:
            raise ValueError(f"{self}.tx_data_rate is not set!")

    @property
    def radio(self) -> Radio:
        return self.__radio

    @radio.setter
    def radio(self, radio):
        if isinstance(radio, RADIO):
            self.__radio = radio.value
        else:
            TypeError

    @property
    def band(self) -> Band:
        return self.__band

    @band.setter
    def band(self, band):
        if self.bands is not None:
            if isinstance(band, BAND):
                self.__band = self.bands[band]
            else:
                raise TypeError
        else:
            raise ValueError(f"{self}.bands is empty!")


if __name__ == "__main__":
    # LoRaMAC()
    pass
