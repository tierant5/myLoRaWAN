from enum import Enum, auto


class LoRaMAC:
    """ Class to define the LoRa MAC Layer """

    class REGION(Enum):
        AS923 = auto()
        AU915 = auto()
        EU868 = auto()
        US915 = auto()
        CN470 = auto()
        IN865 = auto()

    class BW(Enum):
        BW_125KHZ = 125000
        BW_250KHZ = 250000
        BW_500KHZ = 500000

    class SF(Enum):
        SF7 = 7
        SF8 = 8
        SF9 = 9
        SF10 = 10
        SF11 = 11
        SF12 = 12

    class CR(Enum):
        CR_4_5 = auto()
        CR_4_6 = auto()
        CR_4_7 = auto()
        CR_4_8 = auto()

    class POWERMODE(Enum):
        ALWAYS_ON = auto()
        TX_ONLY = auto()
        SLEEP = auto()

    class DEVCLASS(Enum):
        CLASS_A = auto()
        CLASS_B = auto()
        CLASS_C = auto()

    class ACTIVATION(Enum):
        OTAA = auto()
        ABP = auto()

    class DATARATE(Enum):
        DR0 = auto()
        DR1 = auto()
        DR2 = auto()
        DR3 = auto()
        DR4 = auto()
        DR5 = auto()
        DR6 = auto()
        DR7 = auto()
        DR8 = auto()
        DR9 = auto()
        DR10 = auto()
        DR11 = auto()
        DR12 = auto()
        DR13 = auto()
        DR14 = auto()
        DR15 = auto()

    class TXPOWER(Enum):
        TXPOWER0 = auto()
        TXPOWER1 = auto()
        TXPOWER2 = auto()
        TXPOWER3 = auto()
        TXPOWER4 = auto()
        TXPOWER5 = auto()
        TXPOWER6 = auto()
        TXPOWER7 = auto()
        TXPOWER8 = auto()
        TXPOWER9 = auto()
        TXPOWER10 = auto()
        TXPOWER11 = auto()
        TXPOWER12 = auto()
        TXPOWER13 = auto()
        TXPOWER14 = auto()
        TXPOWER15 = auto()

    class CHMASK(Enum):
        CNTL0 = auto()
        CNTL1 = auto()
        CNTL2 = auto()
        CNTL3 = auto()
        CNTL4 = auto()
        CNTL5 = auto()
        CNTL6 = auto()
        CNTL7 = auto()

    class KEYS(Enum):
        RECEIVE_DELAY1 = 'receive_delay1'
        RECEIVE_DELAY2 = 'receive_delay2'
        JOIN_ACCEPT_DELAY1 = 'join_accept_delay1'
        JOIN_ACCEPT_DELAY2 = 'join_accept_delay2'
        MAX_FCNT_GAP = 'max_fcnt_gap'
        ADR_ACK_LIMIT = 'adr_ack_limit'
        ADR_ACK_DELAY = 'adr_ack_delay'
        RETRANSMIT_TIMEOUT = 'retransmit_timeout'
        DOWNLINK_DWELL_TIME = 'downlink_dwell_time'
        PING_SLOT_PERIODICITY = 'ping_slot_periodicity'
        CLASS_B_RESP_TIMEOUT = 'class_b_resp_timeout'
        CLASS_C_RESP_TIMEOUT = 'class_c_resp_timeout'
        REGION = 'region'
        ISM_ID = 'ism_id'
        SUPPORTED_BW = 'supported_bw'
        JOIN_REQ_DATA_RATE = 'join_req_data_rate'
        CFLIST_TYPE_SUPPORTED = 'cflist_type_supported'
        MANDATORY_DATA_RATE = 'mandatory_data_rate'
        OPTIONAL_DATA_RATE = 'optional_data_rate'
        TXPARAMSETUPREQ_SUPPORT = 'txparamsetupreq_support'
        MAX_EIRP = 'max_eirp'
        DEFAULT_RX1DROFFSET = 'default_rx1droffset'
        ALLOWED_RX1DROFFSET = 'allowed_rx1droffset'
        DEFAULT_RX2_DATA_RATE = 'default_rx2_data_rate'
        DEFAULT_RX2_FREQUENCY = 'default_rx2_frequency'
        DUTY_CYCLE = 'duty_cycle'
        DWELL_TIME = 'dwell_time'
        CODING_RATE = 'coding_rate'
        DATA_RATES = 'data_rates'
        TX_POWER = 'tx_power'
        CHANNEL_MASK_CNTL = 'channel_mask_cntl'
        RX1DROFFSET = 'rx1droffset'
        DR_TYPE = 'type'
        DR_SF = 'spreading_factor'
        DR_BW = 'bandwidth'
        DR_BR = 'bit_rate'
        DR_NEXT = 'dr_next'
        DR_MAX_M_PAYLOAD = 'max_m_payload'
        DR_MAX_N_PAYLOAD = 'max_n_payload'
        CHMASK_TYPE = 'type'
        CHMASK_MIN = 'min'
        CHMASK_MAX = 'max'

    def __init__(
        self, region=REGION.US915, frequency=None,
        tx_power=None, bandwidth=None, sf=None, preamble=None,
        coding_rate=None, power_mode=None, tx_iq=None, rx_iq=None,
        adr=False, public=False, tx_retries=2, device_class=DEVCLASS.CLASS_A
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
        self.__rx1droffset = None
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

        self.region = region
        self.adr = adr
        self.public = public
        self.tx_retries = tx_retries
        self.device_class = device_class

    def get_enum(self, enum_class, enum_name):
        return enum_class[enum_name]

    @property
    def region(self) -> REGION:
        return self.__region

    @region.setter
    def region(self, region: REGION):
        if isinstance(region, self.REGION):
            self.__region = region
        else:
            raise ValueError

    @property
    def adr(self) -> bool:
        return self.__adr

    @adr.setter
    def adr(self, adr: bool):
        if isinstance(adr, bool):
            self.__adr = adr
        else:
            raise ValueError

    @property
    def public(self) -> bool:
        return self.__public

    @public.setter
    def public(self, public: bool):
        if isinstance(public, bool):
            self.__public = public
        else:
            raise ValueError

    @property
    def tx_retries(self) -> int:
        return self.__tx_retries

    @tx_retries.setter
    def tx_retries(self, tx_retries: int):
        if isinstance(tx_retries, int):
            self.__tx_retries = tx_retries
        else:
            raise ValueError

    @property
    def device_class(self) -> DEVCLASS:
        return self.__device_class

    @device_class.setter
    def device_class(self, device_class: DEVCLASS):
        if isinstance(device_class, self.DEVCLASS):
            self.__device_class = device_class
        else:
            raise ValueError
