

class Field:
    """ Define a generic field. """

    def __init__(self, name: str):
        self._name = None
        self._default_value = None
        self._size = None


class BitField(Field):
    """ Define a Bit Field. """

    def __init__(self):
        super(Field, self).__init__()


class Frame:
    """ Define a generic frame. """


class Header:
    """ Define a generic header. """


class PHYPayload:
    """ Define a LoRaWAN Physical Payload. """

    def __init__(self):
        self._mhdr = None
        self._macpayload = None
        self._join_request = None
        self._join_accept = None
        self._mic = None


class MHDR:
    """ Define a MAC Frame Header. """

    def __init__(self):
        self._ftype = None
        self._rfu = None
        self._major = None


class FType:
    """ Define a MHDR Frame Type. """

    def __init__(self):
        self._type = None


class RFU:
    """ Define a Reserved for Future Use Field. """


class Major:
    """ Define a bit field for LoRaWAN version. """

    def __init__(self):
        self._version = None


class MACPayload:
    """ Define a LoRaWAN MACPayload Frame. """

    def __init__(self):
        self._fhdr = None
        self._fport = None
        self._frmpayload = None


class FHDR:
    """ Define a MACPayload Frame Header. """

    def __init__(self):
        self._devaddr = None
        self._fctrl = None
        self._fcnt = None
        self._fopts = None


class FCtrl_Downlink:
    """ Define a FHDR Frame Control for Downlinks. """

    def __init__(self):
        self._adr = None
        self._rfu = None
        self._ack = None
        self._fpending = None
        self._foptslen = None


class FCtrl_Uplink:
    """ Define a FHDR Frame Control for Uplinks. """

    def __init__(self):
        self._adr = None
        self._adrackreq = None
        self._ack = None
        self._classb = None
        self._foptslen = None


class MIC:
    """ Define a field for Message Integrity Code. """


class JoinRequest:
    """ Define a LoRaWAN Join-Request Payload. """

    def __init__(self):
        self._joineui = None
        self._deveui = None
        self._devnonce = None


class JoinAccept:
    """ Define a LoRaWAN Join-Accept Payload. """

    def __init__(self):
        self._joinnonce = None
        self._netid = None
        self._devaddr = None
        self._dlsettings = None
        self._rxdelay = None
        self._cflist = None