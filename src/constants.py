from enum import Enum, auto
import Radio
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


class RADIO(Enum):
    SX1276 = Radio.SX127X()


class BW(Enum):
    BW_125KHZ = 7
    BW_250KHZ = 8
    BW_500KHZ = 9


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
    DR0 = 0
    DR1 = 1
    DR2 = 2
    DR3 = 3
    DR4 = 4
    DR5 = 5
    DR6 = 6
    DR7 = 7
    DR8 = 8
    DR9 = 9
    DR10 = 10
    DR11 = 11
    DR12 = 12
    DR13 = 13
    DR14 = 14
    DR15 = 15
    TYPE_LORA = auto()
    TYPE_LRFHSS = auto()
    TYPE_RFU = auto()


class TXPOWER(Enum):
    TXPOWER0 = 0
    TXPOWER1 = 1
    TXPOWER2 = 2
    TXPOWER3 = 3
    TXPOWER4 = 4
    TXPOWER5 = 5
    TXPOWER6 = 6
    TXPOWER7 = 7
    TXPOWER8 = 8
    TXPOWER9 = 9
    TXPOWER10 = 10
    TXPOWER11 = 11
    TXPOWER12 = 12
    TXPOWER13 = 13
    TXPOWER14 = 14
    TXPOWER15 = 15


class CHMASK(Enum):
    CNTL0 = 0
    CNTL1 = 1
    CNTL2 = 2
    CNTL3 = 3
    CNTL4 = 4
    CNTL5 = 5
    CNTL6 = 6
    CNTL7 = 7
    TYPE_INDIVIDUAL = auto()
    TYPE_BAND = auto()
    TYPE_ALL_ON = auto()
    TYPE_ALL_OFF = auto()


class UPLINK(Enum):
    CH0 = 0
    CH1 = 1
    CH2 = 2
    CH3 = 3
    CH4 = 4
    CH5 = 5
    CH6 = 6
    CH7 = 7
    CH8 = 8
    CH9 = 9
    CH10 = 10
    CH11 = 11
    CH12 = 12
    CH13 = 13
    CH14 = 14
    CH15 = 15
    CH16 = 16
    CH17 = 17
    CH18 = 18
    CH19 = 19
    CH20 = 20
    CH21 = 21
    CH22 = 22
    CH23 = 23
    CH24 = 24
    CH25 = 25
    CH26 = 26
    CH27 = 27
    CH28 = 28
    CH29 = 29
    CH30 = 30
    CH31 = 31
    CH32 = 32
    CH33 = 33
    CH34 = 34
    CH35 = 35
    CH36 = 36
    CH37 = 37
    CH38 = 38
    CH39 = 39
    CH40 = 40
    CH41 = 41
    CH42 = 42
    CH43 = 43
    CH44 = 44
    CH45 = 45
    CH46 = 46
    CH47 = 47
    CH48 = 48
    CH49 = 49
    CH50 = 50
    CH51 = 51
    CH52 = 52
    CH53 = 53
    CH54 = 54
    CH55 = 55
    CH56 = 56
    CH57 = 57
    CH58 = 58
    CH59 = 59
    CH60 = 60
    CH61 = 61
    CH62 = 62
    CH63 = 63
    CH64 = 64
    CH65 = 65
    CH66 = 66
    CH67 = 67
    CH68 = 68
    CH69 = 69
    CH70 = 70
    CH71 = 71


class DOWNLINK(Enum):
    CH0 = 0
    CH1 = 1
    CH2 = 2
    CH3 = 3
    CH4 = 4
    CH5 = 5
    CH6 = 6
    CH7 = 7


class BAND(Enum):
    BAND0 = 0
    BAND1 = 1
    BAND2 = 2
    BAND3 = 3
    BAND4 = 4
    BAND5 = 5
    BAND6 = 6
    BAND7 = 7


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
    JOIN_REQ_DATA_RATES = 'join_req_data_rates'
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
    TX_POWERS = 'tx_powers'
    CHANNEL_MASK_CNTL_TABLE = 'channel_mask_cntl_table'
    RX1DROFFSET_TABLE = 'rx1droffset_table'
    DR_TYPE = 'type'
    DR_SF = 'spreading_factor'
    DR_BW = 'bandwidth'
    DR_BR = 'bit_rate'
    DR_NEXT = 'dr_next'
    DR_MAX_M_PAYLOAD = 'max_m_payload'
    DR_MAX_N_PAYLOAD = 'max_n_payload'
    CHMASK_TYPE = 'type'
    CHMASK_MIN_CH = 'min_channel'
    CHMASK_MAX_CH = 'max_channel'
    CHMASK_MIN_BAND = 'min_band'
    CHMASK_MAX_BAND = 'max_band'
    UPLINK_CH = 'uplink_channels'
    DOWNLINK_CH = 'downlink_channels'
    CH_FREQ = 'frequency'
    CH_MIN_DR = 'min_data_rate'
    CH_MAX_DR = 'max_data_rate'
    CH_BW = 'bandwidth'
    BANDS = 'bands'
    BAND_MIN_CH = 'min_channel'
    BAND_MAX_CH = 'max_channel'
