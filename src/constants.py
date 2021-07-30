from enum import Enum, auto
import os

path_to_data = f'{os.getcwd()}/data'
all_region_defaults_file = 'all_region_defaults.json'


def get_enum(enum_class, enum_name):
    return enum_class[enum_name]


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


class DR(Enum):
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
    TYPE_LORA = auto()
    TYPE_LRFHSS = auto()
    TYPE_RFU = auto()


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
    TYPE_INDIVIDUAL = auto()
    TYPE_BLOCK = auto()
    TYPE_ALL_ON = auto()
    TYPE_ALL_OFF = auto()


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
