from constants import FTYPE, CID, MAJOR


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


class RFU:
    """ Define a Reserved for Future Use Field. """


class Frame:
    """ Define a generic frame. """


class Header:
    """ Define a generic header. """


class MACCommand:
    """ Define a MAC Command. """

    def __init__(self):
        self.__cid = None
        self.__data = None


class FOpts:
    """ Define a Frame Options Class. """


class FCtrl:
    """ Define a base FCtrl Class"""

    def __init__(self):
        self.__adr = None
        self.__ack = None
        self.__foptslen = None


class FCtrl_Downlink(FCtrl):
    """ Define a FHDR Frame Control for Downlinks. """

    def __init__(self):
        super(FCtrl_Downlink, self).__init__()
        self.__fpending = None


class FCtrl_Uplink(FCtrl):
    """ Define a FHDR Frame Control for Uplinks. """

    def __init__(self):
        super(FCtrl_Uplink, self).__init__()
        self.__adrackreq = None
        self.__classb = None


class FHDR:
    """ Define a MACPayload Frame Header. """

    def __init__(self):
        self.__ftype = None
        self.__devaddr = None
        self.__fctrl = None
        self.__fcnt = None
        self.__fopts = None

    @property
    def ftype(self) -> FTYPE:
        return self.__ftype

    @ftype.setter
    def ftype(self, ftype):
        if isinstance(ftype, FTYPE):
            self.__ftype = ftype
        else:
            raise TypeError

    @property
    def fctrl(self) -> FCtrl:
        return self.__fctrl

    @fctrl.setter
    def fctrl(self, fctrl):
        if isinstance(fctrl, int):
            if self.ftype == FTYPE.UNCONFDATAUP:
                self.__fctrl = FCtrl_Uplink(fctrl, ack=True)
            elif self.ftype == FTYPE.CONFDATAUP:
                self.__fctrl = FCtrl_Uplink(fctrl, ack=False)
            if self.ftype == FTYPE.UNCONFDATADOWN:
                self.__fctrl = FCtrl_Downlink(fctrl, ack=True)
            elif self.ftype == FTYPE.CONFDATADOWN:
                self.__fctrl = FCtrl_Downlink(fctrl, ack=False)
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def fopts(self) -> FOpts:
        return self.__fopts

    @fopts.setter
    def fopts(self, fopts):
        if isinstance(fopts, int):
            self.__fopts = FOpts(fopts, self.ftype)
        else:
            raise TypeError


class MACPayload:
    """ Define a LoRaWAN MACPayload Frame. """

    def __init__(self):
        self.__ftype = None
        self.__fhdr = None
        self.__fport = None
        self.__frmpayload = None

    @property
    def ftype(self) -> FTYPE:
        return self.__ftype

    @ftype.setter
    def ftype(self, ftype):
        if isinstance(ftype, FTYPE):
            self.__ftype = ftype
        else:
            raise TypeError

    @property
    def fhdr(self) -> FHDR:
        return self.__fhdr

    @fhdr.setter
    def fhdr(self, fhdr):
        if isinstance(fhdr, int):
            self.__fhdr = FHDR(fhdr, self.ftype)
        else:
            raise TypeError


class JoinRequest(MACPayload):
    """ Define a LoRaWAN Join-Request Payload. """

    def __init__(self):
        self.__joineui = None
        self.__deveui = None
        self.__devnonce = None


class JoinAccept(MACPayload):
    """ Define a LoRaWAN Join-Accept Payload. """

    def __init__(self):
        self.__joinnonce = None
        self.__netid = None
        self.__devaddr = None
        self.__dlsettings = None
        self.__rxdelay = None
        self.__cflist = None


class MHDR:
    """ Define a MAC Frame Header. """

    def __init__(self):
        self.__ftype = None
        self.__major = None

    @property
    def ftype(self) -> FTYPE:
        return self.__ftype

    @ftype.setter
    def ftype(self, ftype):
        if isinstance(ftype, FTYPE):
            self.__ftype = ftype
        else:
            raise TypeError

    @property
    def major(self) -> MAJOR:
        return self.__major

    @major.setter
    def major(self, major):
        if isinstance(major, MAJOR):
            self.__major = major
        else:
            raise TypeError


class PHYPayload:
    """ Define a LoRaWAN Physical Payload. """

    def __init__(self):
        self.__mhdr = None
        self.__macpayload = None
        self.__mic = None

    @property
    def mhdr(self) -> MHDR:
        return self.__mhdr

    @mhdr.setter
    def mhdr(self, mhdr):
        if isinstance(mhdr, int):
            self.__mhdr = MHDR(mhdr)
        else:
            raise TypeError

    @property
    def macpayload(self) -> MACPayload:
        return self.__macpayload

    @macpayload.setter
    def macpayload(self, macpayload):
        if isinstance(macpayload, int):
            if self.mhdr.ftype == FTYPE.JOINACCEPT:
                self.__macpayload = JoinAccept(macpayload)
            elif self.mhdr.ftype == FTYPE.JOINREQUEST:
                self.__macpayload = JoinRequest(macpayload)
            else:
                self.__macpayload = MACPayload(macpayload, self.mhdr.ftype)
        else:
            raise TypeError

    @property
    def mic(self) -> int:
        return self.__mic

    @mic.setter
    def mic(self, mic):
        if isinstance(mic, int):
            self.__mic = mic
        else:
            raise TypeError


class LoRaPacket:
    """ Define a LoRa Packet. """

    def __init__(self, *args):
        self.__phypayload = None

    @property
    def phypayload(self, phypayload) -> PHYPayload:
        return self.__phypayload

    @phypayload.setter
    def phypayload(self, phypayload):
        if isinstance(phypayload, int):
            self.__phypayload = PHYPayload(phypayload)
        else:
            raise TypeError
