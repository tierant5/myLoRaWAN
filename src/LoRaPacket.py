from constants import FTYPE, CID, MAJOR, DR, TXPOWER, CHMASK


class Field:
    """ Define a generic field. """

    def __init__(self, name: str):
        self.__name = None
        self.__default_value = None
        self.__size = None


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

    @property
    def cid(self) -> CID:
        return self.__cid

    @cid.setter
    def cid(self, cid):
        if isinstance(cid, int):
            self.__cid = CID(cid)
        elif isinstance(cid, CID):
            self.__cid = cid
        else:
            raise TypeError

    @property
    def data(self) -> bytes:
        return self.__data

    @data.setter
    def data(self, data):
        if isinstance(data, int):
            self.__data = data.to_bytes(
                data.bit_length() + 7 // 8,
                byteorder='big'
            )
        elif isinstance(data, list):
            self.__data = bytes(data)
        else:
            raise TypeError


class LinkCheckReq(MACCommand):
    """ Define a Link Check Request MAC Command. """

    def __init__(self, *args):
        super(LinkCheckReq, self).__init__(*args)


class LinkCheckAns(MACCommand):
    """ Define a Link Check Answer MAC Command. """

    def __init__(self, *args):
        super(LinkCheckAns, self).__init__(*args)
        self.__margin = None
        self.__gwcnt = None
        self.decompose()

    def decompose(self):
        if self.data is not None:
            self.margin = int.from_bytes(self.data[0:1], byteorder='big')
            self.gwcnt = int.from_bytes(self.data[1:2], byteorder='big')
        else:
            raise ValueError

    @property
    def margin(self) -> int:
        return self.__margin

    @margin.setter
    def margin(self, margin):
        if isinstance(margin, int):
            self.__margin = margin
        else:
            raise TypeError

    @property
    def gwcnt(self) -> int:
        return self.__gwcnt

    @gwcnt.setter
    def gwcnt(self, gwcnt):
        if isinstance(gwcnt, int):
            self.__gwcnt = gwcnt
        else:
            raise TypeError


class LinkADRReq(MACCommand):
    """ Define a Link ADR Request MAC Command. """

    def __init__(self, *args):
        super(LinkADRReq, self).__init__(*args)
        self.__datarate_txpower = None
        self.__datarate = None
        self.__txpower = None
        self.__chmask = None
        self.__redundancy = None
        self.__chmaskcntl = None
        self.__nbtrans = None
        self.decompose()

    def decompose(self):
        if self.data is not None:
            self.datarate_txpower = int.from_bytes(self.data[0:1], byteorder='big')     # noqa: E501
            self.chmask = int.from_bytes(self.data[1:3], byteorder='big')
            self.redundancy = int.from_bytes(self.data[3:4], byteorder='big')
        else:
            raise ValueError

    @property
    def datarate_txpower(self):
        return self.__datarate_txpower

    @datarate_txpower.setter
    def datarate_txpower(self, datarate_txpower):
        if isinstance(datarate_txpower, int):
            self.__datarate_txpower = datarate_txpower
            self.datarate = (datarate_txpower & 0b11110000) >> 4
            self.txpower = (datarate_txpower & 0b00001111)
        else:
            raise TypeError

    @property
    def datarate(self) -> DR:
        return self.__datarate

    @datarate.setter
    def datarate(self, datarate):
        if isinstance(datarate, int):
            self.__datarate = DR(datarate)
        elif isinstance(datarate, DR):
            self.__datarate = datarate
        else:
            raise TypeError

    @property
    def txpower(self) -> TXPOWER:
        return self.__txpower

    @txpower.setter
    def txpower(self, txpower):
        if isinstance(txpower, int):
            self.__txpower = TXPOWER(txpower)
        elif isinstance(txpower, TXPOWER):
            self.__txpower = txpower
        else:
            raise TypeError

    @property
    def chmask(self) -> int:
        return self.__chmask

    @chmask.setter
    def chmask(self, chmask):
        if isinstance(chmask, int):
            self.__chmask = chmask
        else:
            raise TypeError

    @property
    def redundancy(self) -> int:
        return self.__redundancy

    @redundancy.setter
    def redundancy(self, redundancy):
        if isinstance(redundancy, int):
            self.__redundancy = redundancy
            self.chmaskcntl = (redundancy & 0b01110000) >> 4
            self.nbtrans = (redundancy & 0b00001111)
        else:
            raise TypeError

    @property
    def chmaskcntl(self) -> CHMASK:
        return self.__chmaskcntl

    @chmaskcntl.setter
    def chmaskcntl(self, chmaskcntl):
        if isinstance(chmaskcntl, int):
            self.__chmaskcntl = CHMASK(chmaskcntl)
        elif isinstance(chmaskcntl, CHMASK):
            self.__chmaskcntl = chmaskcntl
        else:
            raise TypeError

    @property
    def nbtrans(self) -> int:
        return self.__nbtrans

    @nbtrans.setter
    def nbtrans(self, nbtrans):
        if isinstance(nbtrans, int):
            self.__nbtrans = nbtrans
        else:
            raise TypeError


class LinkADRAns(MACCommand):
    """ Define a Link ADR Answer MAC Command. """

    def __init__(
            self, powerack=False, datarateack=False,
            channelmaskack=False, *args
    ):
        super(LinkADRAns, self).__init__(*args)
        self.__status = None
        self.__powerack = None
        self.__datarateack = None
        self.__channelmaskack = None

        self.powerack = powerack
        self.datarateack = datarateack
        self.channelmaskack = channelmaskack

        self.compose()

    def compose(self):
        status = int(self.powerack) << 2
        status = status | int(self.datarateack) << 1
        status = status | int(self.channelmaskack)
        self.status = status
        self.data = self.status

    @property
    def status(self) -> int:
        return self.__status

    @status.setter
    def status(self, status):
        if isinstance(status, int):
            self.__status = status
        else:
            raise TypeError

    @property
    def powerack(self, powerack) -> bool:
        return self.__powerack

    @powerack.setter
    def powerack(self, powerack):
        if isinstance(powerack, bool):
            self.__powerack = powerack
        else:
            raise TypeError

    @property
    def datarateack(self, datarateack) -> bool:
        return self.__datarateack

    @datarateack.setter
    def datarateack(self, datarateack):
        if isinstance(datarateack, bool):
            self.__datarateack = datarateack
        else:
            raise TypeError

    @property
    def channelmaskack(self, channelmaskack) -> bool:
        return self.__channelmaskack

    @channelmaskack.setter
    def channelmaskack(self, channelmaskack):
        if isinstance(channelmaskack, bool):
            self.__channelmaskack = channelmaskack
        else:
            raise TypeError


class DutyCycleReq(MACCommand):
    """ Define an End-Device Transmit Duty Cycle Request MAC Command. """

    def __init__(self, maxdutycycle, *args):
        super(DutyCycleReq, self).__init__(*args)
        self.__dutycyclepl = None
        self.__maxdutycycle = None

        self.maxdutycycle = maxdutycycle

        self.compose()

    def compose(self):
        self.dutycyclepl = self.maxdutycycle
        self.data = self.dutycyclepl

    @property
    def dutycyclepl(self) -> int:
        return self.__dutycyclepl

    @dutycyclepl.setter
    def dutycyclepl(self, dutycyclepl):
        if isinstance(dutycyclepl, int):
            self.__dutycyclepl = dutycyclepl
        else:
            raise TypeError

    @property
    def maxdutycycle(self) -> int:
        return self.__maxdutycycle

    @maxdutycycle.setter
    def maxdutycycle(self, maxdutycycle):
        if isinstance(maxdutycycle, int):
            self.__maxdutycycle = maxdutycycle
        else:
            raise TypeError


class DutyCycleAns(MACCommand):
    """ Define an End-Device Transmit Duty Cycle Answer MAC Command. """

    def __init__(self, *args):
        super(DutyCycleAns, self).__init__(*args)


class RXParamSetupReq(MACCommand):
    """ Define a Recieve Windows Parameters Request MAC Command. """

    def __init__(self, *args):
        super(RXParamSetupReq, self).__init__(*args)
        self.__dlsettings = None
        self.__frequency = None
        self.__rx1droffset = None
        self.__rx2datarate = None


class RXParamSetupAns(MACCommand):
    """ Define a Recieve Windows Parameters Ansswer MAC Command. """

    def __init__(self, *args):
        super(RXParamSetupAns, self).__init__(*args)
        self.__status = None
        self.__rx1droffsetack = None
        self.__rx2datarateack = None
        self.__channelack = None


class DevStatusReq(MACCommand):
    """ Define an End-Device Status Request MAC Command. """

    def __init__(self, *args):
        super(DevStatusReq, self).__init__(*args)


class DevStatusAns(MACCommand):
    """ Define an End-Device Status Answer MAC Command. """

    def __init__(self, *args):
        super(DevStatusAns, self).__init__(*args)
        self.__battery = None
        self.__radiostatus = None
        self.__snr = None


class NewChannelReq(MACCommand):
    """ Define a Creation of a Channel Request MAC Command. """

    def __init__(self, *args):
        super(NewChannelReq, self).__init__(*args)
        self.__chindex = None
        self.__frequency = None
        self.__drrange = None
        self.__maxdr = None
        self.__mindr = None


class NewChannelAns(MACCommand):
    """ Define a Creation of a Channel Answer MAC Command. """

    def __init__(self, *args):
        super(NewChannelAns, self).__init__(*args)
        self.__status = None
        self.__datarate_range_ok = None
        self.__channel_frequency_ok = None


class DLChannelReq(MACCommand):
    """ Define a Modification of a Channel Request MAC Command. """

    def __init__(self, *args):
        super(DLChannelReq, self).__init__(*args)
        self.__chindex = None
        self.__frequency = None


class DLChannelAns(MACCommand):
    """ Define a Modification of a Channel Answer MAC Command. """

    def __init__(self, *args):
        super(DLChannelAns, self).__init__(*args)
        self.__status = None
        self.__uplink_frequency_exists = None
        self.__channel_frequency_ok = None


class RXTimingSetupReq(MACCommand):
    """ Define a Setting Delay between TX and RX Request MAC Command. """

    def __init__(self, *args):
        super(RXTimingSetupReq, self).__init__(*args)
        self.__rxtimingsettings = None
        self.__del = None


class RXTimingSetupAns(MACCommand):
    """ Define a Setting Delay between TX and RX Answer MAC Command. """

    def __init__(self, *args):
        super(RXTimingSetupAns, self).__init__(*args)


class TXParamSetupReq(MACCommand):
    """ Define an End-Device Transmit Parameters Request MAC Command. """

    def __init__(self, *args):
        super(TXParamSetupReq, self).__init__(*args)
        self.__eirp_dwelltime = None
        self.__downlinkdwelltime = None
        self.__uplinkdwelltime = None
        self.__maxeirp = None


class TXParamSetupAns(MACCommand):
    """ Define an End-Device Transmit Parameters Answer MAC Command. """

    def __init__(self, *args):
        super(TXParamSetupAns, self).__init__(*args)


class FOpts:
    """ Define a Frame Options Class. """

    def __init__(self, fopts, ftype):
        self.__fopts = None
        self.__ftype = None
        self.__mac_commands = []


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
                self.__fctrl = FCtrl_Uplink(fctrl, ack=False)
            elif self.ftype == FTYPE.CONFDATAUP:
                self.__fctrl = FCtrl_Uplink(fctrl, ack=True)
            if self.ftype == FTYPE.UNCONFDATADOWN:
                self.__fctrl = FCtrl_Downlink(fctrl, ack=False)
            elif self.ftype == FTYPE.CONFDATADOWN:
                self.__fctrl = FCtrl_Downlink(fctrl, ack=True)
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
