from helpers import load_all_region_json, load_region_json
from constants import (
    CHMASK,
    KEYS,
    REGION,
    BW,
    SF,
    CR,
    POWERMODE,
    DEVCLASS,
    ACTIVATION,
    TXPOWER,
    DR,
)
from constants import get_enum
from DataRate import DataRate
from ChannelMask import ChannelMaskCntl


class LoRaMAC:
    """Class to define the LoRa MAC Layer"""

    def __init__(
        self,
        region=REGION.US915,
        frequency=None,
        tx_power=None,
        bandwidth=None,
        sf=None,
        preamble=None,
        coding_rate=None,
        power_mode=None,
        tx_iq=None,
        rx_iq=None,
        adr=False,
        public=False,
        tx_retries=2,
        device_class=DEVCLASS.CLASS_A,
    ):

        self.__region = None
        self.__frequency = None
        self.__tx_power = None
        self.__bandwidth = None
        self.__sf = None
        self.__preamble = None
        self.__coding_rate = None
        self.__power_mode = None
        self.__tx_iq = None
        self.__rx_iq = None
        self.__adr = None
        self.__public = None
        self.__tx_retries = None
        self.__device_class = None
        self.__activation = None
        self.__rx_delay1 = None
        self.__rx_delay2 = None
        self.__join_accept_delay1 = None
        self.__join_accept_delay2 = None
        self.__max_fcnt_gap = None
        self.__adr_ack_limit = None
        self.__adr_ack_delay = None
        self.__retransmit_timeout = None
        self.__downlink_dwell_time = None
        self.__uplink_dwell_time = None
        self.__ping_slot_periodicity = None
        self.__ping_slot_datarate = None
        self.__ping_slot_channel = None
        self.__class_b_resp_timeout = None
        self.__class_c_resp_timeout = None
        self.__ism_id = None
        self.__supported_bw = None
        self.__join_request_data_rate = None
        self.__cflist_type_supported = None
        self.__mandatory_data_rate = None
        self.__optional_data_rate = None
        self.__txparamsetupreq_support = None
        self.__max_eirp = None
        self.__default_rx1droffset = None
        self.__allowed_rx1droffset = None
        self.__default_rx2_data_rate = None
        self.__default_rx2_frequency = None
        self.__duty_cycle = None
        self.__dwell_time = None
        self.__coding_rate = None
        self.__data_rates = None
        self.__tx_power = None
        self.__channel_mask_cntl = None
        self.__rx1droffset = None

        # Set self.****
        self.region = region
        self.adr = adr
        self.device_class = device_class
        # TODO Check if previous settings are present
        self.load_defaults()

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
        self.ping_slot_periodicity = json_data[KEYS.PING_SLOT_PERIODICITY.value]
        self.class_b_resp_timeout = json_data[KEYS.CLASS_B_RESP_TIMEOUT.value]
        self.class_c_resp_timeout = json_data[KEYS.CLASS_C_RESP_TIMEOUT.value]

    def decompose_region_defaults(self, json_data):
        self.ism_id = json_data[KEYS.ISM_ID.value]
        self.supported_bw = json_data[KEYS.SUPPORTED_BW.value]
        self.join_request_data_rate = json_data[KEYS.JOIN_REQ_DATA_RATE.value]
        self.cflist_type_supported = json_data[KEYS.CFLIST_TYPE_SUPPORTED.value]
        self.mandatory_data_rate = json_data[KEYS.MANDATORY_DATA_RATE.value]
        self.optional_data_rate = json_data[KEYS.OPTIONAL_DATA_RATE.value]
        self.txparamsetupreq_support = json_data[KEYS.TXPARAMSETUPREQ_SUPPORT.value]
        self.max_eirp = json_data[KEYS.MAX_EIRP.value]
        self.default_rx2_data_rate = json_data[KEYS.DEFAULT_RX2_DATA_RATE.value]
        self.default_rx2_frequency = json_data[KEYS.DEFAULT_RX2_FREQUENCY.value]
        self.duty_cycle = json_data[KEYS.DUTY_CYCLE.value]
        self.dwell_time = json_data[KEYS.DWELL_TIME.value]
        self.coding_rate = json_data[KEYS.CODING_RATE.value]
        self.data_rates = json_data[KEYS.DATA_RATES.value]
        self.tx_power = json_data[KEYS.TX_POWER.value]
        self.channel_mast_cntl = json_data[KEYS.CHANNEL_MASK_CNTL.value]
        self.rx1droffset = json_data[KEYS.RX1DROFFSET.value]

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
    def join_request_data_rate(self) -> dict:
        return self.__join_request_data_rate

    @join_request_data_rate.setter
    def join_request_data_rate(self, join_request_data_rate):
        if isinstance(join_request_data_rate, dict):
            if self.__join_request_data_rate is None:
                self.__join_request_data_rate = {}
                for bw, dr in join_request_data_rate.items():
                    self.__join_request_data_rate[get_enum(BW, bw)] = get_enum(DR, dr)
            else:
                raise ValueError(f"{self}.join_request_data_rate already exists!")
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
                raise ValueError(f"{self}.manadatory_data_rate already exists!")
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
    def default_rx2_frequency(self) -> int:
        return self.__default_rx2_frequency

    @default_rx2_frequency.setter
    def default_rx2_frequency(self, default_rx2_frequency: int):
        if isinstance(default_rx2_frequency, int):
            self.__default_rx2_frequency = default_rx2_frequency
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
    def tx_power(self) -> dict:
        return self.__tx_power

    @tx_power.setter
    def tx_power(self, tx_power):
        if isinstance(tx_power, dict):
            if self.__tx_power is None:
                self.__tx_power = {}
                for key, value in tx_power.items():
                    self.__tx_power[get_enum(TXPOWER, key)] = value
            else:
                raise ValueError(f"{self}.tx_power is not empty!")
        else:
            raise TypeError

    @property
    def channel_mask_cntl(self) -> dict:
        return self.__channel_mask_cntl

    @channel_mask_cntl.setter
    def channel_mask_cntl(self, channel_mask_cntl: dict):
        if isinstance(channel_mask_cntl, dict):
            if self.__channel_mask_cntl is None:
                self.__channel_mask_cntl = {}
                for key, value in channel_mask_cntl.items():
                    cntl = get_enum(CHMASK, key)
                    self.__channel_mask_cntl[cntl] = ChannelMaskCntl(cntl, value)
            else:
                raise ValueError(f"{self}.channel_mask_cntl is not empty!")
        else:
            raise TypeError

    @property
    def rx1droffset(self) -> dict:
        return self.__rx1droffset

    @rx1droffset.setter
    def rx1droffset(self, rx1droffset):
        if isinstance(rx1droffset, dict):
            if self.__rx1droffset is None:
                self.__rx1droffset = {}
                for key, value in rx1droffset.items():
                    dr = get_enum(DR, key)
                    drs = [get_enum(DR, item) for item in value]
                    self.__rx1droffset[dr] = drs
            else:
                raise ValueError(f"{self}.rx1droffset is not empty!")
        else:
            raise TypeError


if __name__ == "__main__":
    LoRaMAC()
