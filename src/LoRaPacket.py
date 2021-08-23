from constants import FTYPE, CID, MAJOR, DR, TXPOWER, CHMASK
from AES_CMAC import AES_CMAC
from Crypto.Cipher import AES
from copy import deepcopy
import math


class Field:
    """ Define a generic field. """

    def __init__(self, data=None):
        self.__name = None
        self.__default_value = None
        self.__size = None
        self.__data = None
        self.__data_list = None

        self.data = data

    @property
    def data(self) -> bytes:
        return self.__data

    @data.setter
    def data(self, data):
        if isinstance(data, int):
            self.__data = data.to_bytes(
                (data.bit_length() + 7) // 8,
                byteorder='big'
            )
        elif isinstance(data, list):
            self.__data = bytes(data)
        elif data is None:
            self.__data = data
        else:
            raise TypeError

    @property
    def data_list(self) -> list:
        return [byte for byte in self.data]


class MACCommand(Field):
    """ Define a MAC Command. """

    def __init__(self, *args):
        super(MACCommand, self).__init__(*args)
        self.__cid = None

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


class LinkCheckReq(MACCommand):
    """ Define a Link Check Request MAC Command. """

    def __init__(self, *args):
        super(LinkCheckReq, self).__init__(*args)
        self.cid = CID.LINKCHECK


class LinkCheckAns(MACCommand):
    """ Define a Link Check Answer MAC Command. """

    def __init__(self, *args):
        super(LinkCheckAns, self).__init__(*args)
        self.__margin = None
        self.__gwcnt = None
        self.cid = CID.LINKCHECK
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
        self.cid = CID.LINKADR
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

        self.cid = CID.LINKADR
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
    def powerack(self) -> bool:
        return self.__powerack

    @powerack.setter
    def powerack(self, powerack):
        if isinstance(powerack, bool):
            self.__powerack = powerack
        else:
            raise TypeError

    @property
    def datarateack(self) -> bool:
        return self.__datarateack

    @datarateack.setter
    def datarateack(self, datarateack):
        if isinstance(datarateack, bool):
            self.__datarateack = datarateack
        else:
            raise TypeError

    @property
    def channelmaskack(self) -> bool:
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

        self.cid = CID.DUTYCYCLE
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
        self.cid = CID.DUTYCYCLE


class RXParamSetupReq(MACCommand):
    """ Define a Recieve Windows Parameters Request MAC Command. """

    def __init__(self, *args):
        super(RXParamSetupReq, self).__init__(*args)
        self.__dlsettings = None
        self.__frequency = None
        self.__rx1droffset = None
        self.__rx2datarate = None

        self.cid = CID.RXPARAMSETUP
        self.decompose()

    def decompose(self):
        if self.data is not None:
            self.dlsettings = int.from_bytes(self.data[0:1], byteorder='big')
            self.frequency = int.from_bytes(self.data[1:4], byteorder='big')
        else:
            raise ValueError

    @property
    def rx1droffset(self) -> int:
        return self.__rx1droffset

    @rx1droffset.setter
    def rx1droffset(self, rx1droffset):
        if isinstance(rx1droffset, int):
            self.__rx1droffset = rx1droffset
        else:
            raise TypeError

    @property
    def rx2datarate(self) -> DR:
        return self.__rx2datarate

    @rx2datarate.setter
    def rx2datarate(self, rx2datarate):
        if isinstance(rx2datarate, int):
            self.__rx2datarate = DR(rx2datarate)
        elif isinstance(rx2datarate, DR):
            self.__rx2datarate = rx2datarate
        else:
            raise TypeError

    @property
    def dlsettings(self) -> int:
        return self.__dlsettings

    @dlsettings.setter
    def dlsettings(self, dlsettings):
        if isinstance(dlsettings, int):
            self.__dlsettings = dlsettings
            self.rx1droffset = (dlsettings & 0b01110000) >> 4
            self.rx2datarate = (dlsettings & 0b00001111)
        else:
            raise TypeError

    @property
    def frequency(self) -> int:
        return self.__frequency

    @frequency.setter
    def frequency(self, frequency):
        if isinstance(frequency, int):
            self.__frequency = frequency
        else:
            raise TypeError


class RXParamSetupAns(MACCommand):
    """ Define a Recieve Windows Parameters Ansswer MAC Command. """

    def __init__(
            self, rx1droffsetack=False, rx2datarateack=False,
            channelack=False, *args
            ):
        super(RXParamSetupAns, self).__init__(*args)
        self.__status = None
        self.__rx1droffsetack = None
        self.__rx2datarateack = None
        self.__channelack = None

        self.cid = CID.RXPARAMSETUP
        self.rx1droffsetack = rx1droffsetack
        self.rx2datarateack = rx2datarateack
        self.channelack = channelack

        self.compose()

    def compose(self):
        status = int(self.rx1droffsetack) << 2
        status = status | int(self.rx2datarateack) << 1
        status = status | int(self.channelack)
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
    def rx1droffsetack(self) -> bool:
        return self.__rx1droffsetack

    @rx1droffsetack.setter
    def rx1droffsetack(self, rx1droffsetack):
        if isinstance(rx1droffsetack, bool):
            self.__rx1droffsetack = rx1droffsetack
        else:
            raise TypeError

    @property
    def rx2datarateack(self) -> bool:
        return self.__rx2datarateack

    @rx2datarateack.setter
    def rx2datarateack(self, rx2datarateack):
        if isinstance(rx2datarateack, bool):
            self.__rx2datarateack = rx2datarateack
        else:
            raise TypeError

    @property
    def channelack(self) -> bool:
        return self.__channelack

    @channelack.setter
    def channelack(self, channelack):
        if isinstance(channelack, bool):
            self.__channelack = channelack
        else:
            raise TypeError


class DevStatusReq(MACCommand):
    """ Define an End-Device Status Request MAC Command. """

    def __init__(self, *args):
        super(DevStatusReq, self).__init__(*args)
        self.cid = CID.DEVSTATUS


class DevStatusAns(MACCommand):
    """ Define an End-Device Status Answer MAC Command. """

    def __init__(self, snr, battery=0, *args):
        super(DevStatusAns, self).__init__(*args)
        self.__battery = None
        self.__radiostatus = None
        self.__snr = None

        self.cid = CID.DEVSTATUS
        self.battery = battery
        self.snr = snr

        self.compose()

    def compose(self):
        self.radiostatus = self.snr
        self.data = (self.battery << 8) | self.radiostatus

    @property
    def battery(self) -> int:
        return self.__battery

    @battery.setter
    def battery(self, battery):
        if isinstance(battery, int):
            if battery < 256:
                self.__battery = battery
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def snr(self) -> int:
        return self.__snr

    @snr.setter
    def snr(self, snr):
        if isinstance(snr, int):
            if (snr >= -32) and (snr <= 31):
                self.__snr = snr & (2 ** 6 - 1)
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def radiostatus(self) -> int:
        return self.__radiostatus

    @radiostatus.setter
    def radiostatus(self, radiostatus):
        if isinstance(radiostatus, int):
            self.__radiostatus = radiostatus
        else:
            raise TypeError


class NewChannelReq(MACCommand):
    """ Define a Creation of a Channel Request MAC Command. """

    def __init__(self, *args):
        super(NewChannelReq, self).__init__(*args)
        self.__chindex = None
        self.__frequency = None
        self.__drrange = None
        self.__maxdr = None
        self.__mindr = None

        self.cid = CID.NEWCHANNEL


class NewChannelAns(MACCommand):
    """ Define a Creation of a Channel Answer MAC Command. """

    def __init__(self, *args):
        super(NewChannelAns, self).__init__(*args)
        self.__status = None
        self.__datarate_range_ok = None
        self.__channel_frequency_ok = None

        self.cid = CID.NEWCHANNEL


class DLChannelReq(MACCommand):
    """ Define a Modification of a Channel Request MAC Command. """

    def __init__(self, *args):
        super(DLChannelReq, self).__init__(*args)
        self.__chindex = None
        self.__frequency = None

        self.cid = CID.DLCHANNEL


class DLChannelAns(MACCommand):
    """ Define a Modification of a Channel Answer MAC Command. """

    def __init__(self, *args):
        super(DLChannelAns, self).__init__(*args)
        self.__status = None
        self.__uplink_frequency_exists = None
        self.__channel_frequency_ok = None

        self.cid = CID.DLCHANNEL


class RXTimingSetupReq(MACCommand):
    """ Define a Setting Delay between TX and RX Request MAC Command. """

    def __init__(self, *args):
        super(RXTimingSetupReq, self).__init__(*args)
        self.__rxtimingsettings = None
        self.__delay = None

        self.cid = CID.RXTIMINGSETUP
        self.decompose()

    def decompose(self):
        self.rxtimingsettings = int.from_bytes(self.data[0:1], byteorder='big')

    @property
    def delay(self) -> int:
        return self.__delay

    @delay.setter
    def delay(self, delay):
        if isinstance(delay, int):
            self.__delay = delay
        else:
            raise TypeError

    @property
    def rxtimingsettings(self) -> int:
        return self.__rxtimingsettings

    @rxtimingsettings.setter
    def rxtimingsettings(self, rxtimingsettings):
        if isinstance(rxtimingsettings, int):
            self.__rxtimingsettings = rxtimingsettings
            self.delay = (rxtimingsettings & 0b00001111)
        else:
            raise TypeError


class RXTimingSetupAns(MACCommand):
    """ Define a Setting Delay between TX and RX Answer MAC Command. """

    def __init__(self, *args):
        super(RXTimingSetupAns, self).__init__(*args)
        self.cid = CID.RXTIMINGSETUP


class TXParamSetupReq(MACCommand):
    """ Define an End-Device Transmit Parameters Request MAC Command. """

    def __init__(self, *args):
        super(TXParamSetupReq, self).__init__(*args)
        self.__eirp_dwelltime = None
        self.__downlinkdwelltime = None
        self.__uplinkdwelltime = None
        self.__maxeirp = None

        self.cid = CID.TXPARAMSETUP


class TXParamSetupAns(MACCommand):
    """ Define an End-Device Transmit Parameters Answer MAC Command. """

    def __init__(self, *args):
        super(TXParamSetupAns, self).__init__(*args)

        self.cid = CID.TXPARAMSETUP


class DeviceTimeReq(MACCommand):
    """ Define an End-Device Time Request MAC Command. """

    def __init__(self, *args):
        super(DeviceTimeReq, self).__init__(*args)
        self.cid = CID.DEVICETIME


class DeviceTimeAns(MACCommand):
    """ Define an End-Device Time Answer MAC Command. """

    def __init__(self, *args):
        super(DeviceTimeAns, self).__init__(*args)
        self.cid = CID.DEVICETIME


class FOpts(Field):
    """ Define a Frame Options Class. """

    def __init__(self, ftype, *args):
        super(FOpts, self).__init__(*args)
        self.__ftype = None
        self.mac_commands = []

        self.ftype = ftype

    def decompose(self):
        self.mac_commands = []
        mac_data = deepcopy(self.data_list)
        while len(mac_data) != 0:
            cid_byte = mac_data.pop(0)
            size, maccommand = self.get_mac_info(cid_byte=cid_byte)
            cid_data = []
            for i in range(0, size):
                cid_data.append(mac_data.pop(0))
            self.mac_commands.append(maccommand(cid_data))

    def compose(self):
        data = []
        for command in self.mac_commands:
            command.compose()
            data = data + [command.cid.value] + command.data_list
        self.data = data

    def get_mac_info(self, cid_byte):
        cid = CID(cid_byte)
        if self.ftype in [FTYPE.UNCONFDATADOWN, FTYPE.CONFDATADOWN]:
            if cid == CID.LINKCHECK:
                size = 2
                maccommand = LinkCheckAns
            elif cid == CID.LINKADR:
                size = 4
                maccommand = LinkADRReq
            elif cid == CID.DUTYCYCLE:
                size = 1
                maccommand = DutyCycleReq
            elif cid == CID.RXPARAMSETUP:
                size = 4
                maccommand = RXParamSetupReq
            elif cid == CID.DEVSTATUS:
                size = 0
                maccommand = DevStatusReq
            elif cid == CID.NEWCHANNEL:
                size = 5
                maccommand = NewChannelReq
            elif cid == CID.RXTIMINGSETUP:
                size = 1
                maccommand = RXTimingSetupReq
            elif cid == CID.TXPARAMSETUP:
                size = 1
                maccommand = TXParamSetupReq
            elif cid == CID.DLCHANNEL:
                size = 4
                maccommand = DLChannelReq
            elif cid == CID.DEVICETIME:
                size = 5
                maccommand = DevStatusAns
            else:
                raise ValueError(f'{cid} is not supported')
        elif self.ftype in [FTYPE.UNCONFDATAUP, FTYPE.CONFDATAUP]:
            if cid == CID.LINKCHECK:
                size = 0
                maccommand = LinkCheckReq
            elif cid == CID.LINKADR:
                size = 1
                maccommand = LinkADRAns
            elif cid == CID.DUTYCYCLE:
                size = 0
                maccommand = DutyCycleAns
            elif cid == CID.RXPARAMSETUP:
                size = 1
                maccommand = RXParamSetupAns
            elif cid == CID.DEVSTATUS:
                size = 2
                maccommand = DevStatusAns
            elif cid == CID.NEWCHANNEL:
                size = 1
                maccommand = NewChannelAns
            elif cid == CID.RXTIMINGSETUP:
                size = 0
                maccommand = RXTimingSetupAns
            elif cid == CID.TXPARAMSETUP:
                size = 0
                maccommand = TXParamSetupAns
            elif cid == CID.DLCHANNEL:
                size = 1
                maccommand = DLChannelAns
            elif cid == CID.DEVICETIME:
                size = 0
                maccommand = DevStatusReq
            else:
                raise ValueError(f'{cid} is not supported')
        else:
            raise ValueError(f'{self.ftype} is not supported')
        return size, maccommand

    @property
    def ftype(self) -> FTYPE:
        return self.__ftype

    @ftype.setter
    def ftype(self, ftype):
        if isinstance(ftype, FTYPE):
            self.__ftype = ftype
        else:
            raise TypeError


class FCtrl(Field):
    """ Define a base FCtrl Class"""

    def __init__(self, ack, *args):
        super(FCtrl, self).__init__(*args)
        self.__adr = None
        self.__ack = None
        self.__foptslen = None

        self.ack = ack

    def decompose(self):
        data = int.from_bytes(self.data, byteorder='big')
        self.adr = (data & 0b10000000) >> 7
        self.ack = (data & 0b00100000) >> 5
        self.foptslen = (data & 0b00001111)

    def compose(self):
        data = int(self.adr) << 7
        data = data | (int(self.ack) << 5)
        data = data | self.foptslen
        self.data = data

    @property
    def adr(self) -> bool:
        return self.__adr

    @adr.setter
    def adr(self, adr):
        if isinstance(adr, bool):
            self.__adr = adr
        elif isinstance(adr, int):
            if adr == 0:
                self.__adr = False
            else:
                self.__adr = True
        else:
            raise TypeError

    @property
    def ack(self) -> bool:
        return self.__ack

    @ack.setter
    def ack(self, ack):
        if isinstance(ack, bool):
            self.__ack = ack
        elif isinstance(ack, int):
            if ack == 0:
                self.__ack = False
            else:
                self.__ack = True
        else:
            raise TypeError

    @property
    def foptslen(self) -> int:
        return self.__foptslen

    @foptslen.setter
    def foptslen(self, foptslen):
        if isinstance(foptslen, int):
            self.__foptslen = foptslen
        else:
            raise TypeError


class FCtrl_Downlink(FCtrl):
    """ Define a FHDR Frame Control for Downlinks. """

    def __init__(self, *args):
        super(FCtrl_Downlink, self).__init__(*args)
        self.__fpending = None

    def decompose(self):
        super(FCtrl_Downlink, self).decompose()
        data = int.from_bytes(self.data, byteorder='big')
        self.fpending = (data & 0b00010000) >> 4

    @property
    def fpending(self) -> bool:
        return self.__fpending

    @fpending.setter
    def fpending(self, fpending):
        if isinstance(fpending, bool):
            self.__fpending = fpending
        elif isinstance(fpending, int):
            if fpending == 0:
                self.__fpending = False
            else:
                self.__fpending = True
        else:
            raise TypeError


class FCtrl_Uplink(FCtrl):
    """ Define a FHDR Frame Control for Uplinks. """

    def __init__(self, *args):
        super(FCtrl_Uplink, self).__init__(*args)
        self.__adrackreq = None
        self.__classb = None

    def compose(self):
        super(FCtrl_Uplink, self).compose()
        data = int(self.adrackreq) << 6
        data = data | (int(self.classb) << 4)
        self.data = int.from_bytes(self.data, byteorder='big') | data

    @property
    def adrackreq(self) -> bool:
        return self.__adrackreq

    @adrackreq.setter
    def adrackreq(self, adrackreq):
        if isinstance(adrackreq, bool):
            self.__adrackreq = adrackreq
        else:
            raise TypeError

    @property
    def classb(self) -> bool:
        return self.__classb

    @classb.setter
    def classb(self, classb):
        if isinstance(classb, bool):
            self.__classb = classb
        else:
            raise TypeError


class FHDR(Field):
    """ Define a MACPayload Frame Header. """

    def __init__(self, ftype, *args):
        super(FHDR, self).__init__(*args)
        self.__ftype = None
        self.__devaddr = None
        self.__fctrl = None
        self.__fcnt = None
        self.__fopts = None

        self.ftype = ftype

    def decompose(self):
        self.devaddr = list(reversed(self.data_list[:4]))
        self.fctrl = self.data_list[4:5]
        self.fctrl.decompose()
        self.fcnt = int.from_bytes(self.data[5:7], byteorder='little')
        self.data = self.data_list[:7 + self.fctrl.foptslen]
        if self.fctrl.foptslen != 0:
            self.fopts = self.data_list[-self.fctrl.foptslen:]
            self.fopts.decompose()

    def compose(self):
        data = list(reversed(self.devaddr))
        self.fctrl.foptslen = len(self.fopts.data)
        self.fctrl.compose()
        data = data + self.fctrl.data_list
        data = data + [
            byte for byte in self.fcnt.to_bytes(2, byteorder='little')
        ]
        if self.fctrl.foptslen != 0:
            self.fopts.compose()
            data = data + self.fopts.data_list
        self.data = data

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
        if isinstance(fctrl, list):
            if self.ftype == FTYPE.UNCONFDATAUP:
                self.__fctrl = FCtrl_Uplink(False, fctrl)
            elif self.ftype == FTYPE.CONFDATAUP:
                self.__fctrl = FCtrl_Uplink(True, fctrl)
            if self.ftype == FTYPE.UNCONFDATADOWN:
                self.__fctrl = FCtrl_Downlink(False, fctrl)
            elif self.ftype == FTYPE.CONFDATADOWN:
                self.__fctrl = FCtrl_Downlink(True, fctrl)
            else:
                raise ValueError
        elif issubclass(fctrl, FCtrl):
            self.__fctrl = fctrl
        else:
            raise TypeError

    @property
    def fopts(self) -> FOpts:
        return self.__fopts

    @fopts.setter
    def fopts(self, fopts):
        if isinstance(fopts, list):
            self.__fopts = FOpts(fopts, self.ftype)
        elif isinstance(fopts, FOpts):
            self.__fopts = fopts
        else:
            raise TypeError

    @property
    def devaddr(self) -> list:
        return self.__devaddr

    @devaddr.setter
    def devaddr(self, devaddr):
        if isinstance(devaddr, list):
            self.__devaddr = devaddr
        else:
            raise TypeError

    @property
    def fcnt(self) -> int:
        return self.__fcnt

    @fcnt.setter
    def fcnt(self, fcnt):
        if isinstance(fcnt, int):
            self.__fcnt = fcnt
        else:
            raise TypeError


class MACPayload(Field):
    """ Define a LoRaWAN MACPayload Frame. """

    def __init__(self, ftype, *args):
        super(MACPayload, self).__init__(*args)
        self.__ftype = None
        self.__fhdr = None
        self.__fport = None
        self.__frmpayload = None
        self.__decrypted_payload = None

        self.ftype = ftype

    def decompose(self, keys):
        self.fhdr = self.data_list
        self.fhdr.decompose()
        fhdr_size = len(self.fhdr.data)
        if fhdr_size < len(self.data):
            self.fport = int.from_bytes(
                self.data[fhdr_size:(fhdr_size + 1)],
                byteorder='big'
            )
            self.frmpayload = [byte for byte in self.data[(fhdr_size + 1):]]
            self.decrypt_payload(keys)

    def encryption(self, keys):
        if self.frmpayload is not None:
            if self.fport == 0:
                key = keys.nwskey
            else:
                key = keys.appskey
            if self.ftype in [FTYPE.UNCONFDATADOWN, FTYPE.CONFDATADOWN]:
                direction = 0x01
            else:
                direction = 0x00
            k = int(math.ceil(len(self.frmpayload) / 16.0))

            a = []
            for i in range(k):
                a += [0x01]
                a += [0x00, 0x00, 0x00, 0x00]
                a += [direction]
                a += list(reversed(self.fhdr.devaddr))
                a += [
                    byte for byte in self.fhdr.fcnt.to_bytes(4, byteorder='little')    # noqa: E501
                ]
                # a += [0x00]     # fcnt 32bit
                # a += [0x00]     # fcnt 32bit
                a += [0x00]
                a += [i+1]

            cipher = AES.new(bytes(key), AES.MODE_ECB)
            s = cipher.encrypt(bytes(a))

            padded_payload = []
            for i in range(k):
                idx = (i + 1) * 16
                padded_payload += (self.frmpayload[idx - 16:idx] + ([0x00] * 16))[:16]     # noqa: E501

            payload = []
            for i in range(len(self.frmpayload)):
                payload += [s[i] ^ padded_payload[i]]
            return list(map(int, payload))

    def decrypt_payload(self, keys):
        self.decrypted_payload = self.encryption(keys)

    def compose(self, keys):
        self.fhdr.compose()
        if self.fport == 0:
            self.frmpayload = self.fhdr.fopts.data_list
            self.fhdr.fctrl.foptslen = 0
            self.fhdr.compose()
        data = self.fhdr.data_list
        if self.fport is not None:
            data = data + [self.fport]
            self.encrypt_payload(keys)
            data = data + self.frmpayload
        self.data = data

    def encrypt_payload(self, keys):
        if self.decrypted_payload is not None:
            self.frmpayload = self.decrypted_payload
            self.frmpayload = self.encryption(keys)

    def calculate_mic(self, keys, mhdr):
        if self.ftype in [FTYPE.UNCONFDATADOWN, FTYPE.CONFDATADOWN]:
            direction = 0x01
        else:
            direction = 0x00

        msg = mhdr.data_list + self.fhdr.data_list
        if self.fport is not None:
            msg += [self.fport] + self.frmpayload

        mic = [0x49]
        mic += [0x00, 0x00, 0x00, 0x00]
        mic += [direction]
        mic += list(reversed(self.fhdr.devaddr))
        mic += [
            byte for byte in self.fhdr.fcnt.to_bytes(4, byteorder='little')    # noqa: E501
        ]
        mic += [0x00]
        mic += [len(msg)]
        mic += msg

        cmac = AES_CMAC()
        computed_mic = cmac.encode(bytes(keys.nwkskey), bytes(mic))[:4]
        return list(map(int, computed_mic))

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
        if isinstance(fhdr, list):
            self.__fhdr = FHDR(self.ftype, fhdr)
        elif isinstance(fhdr, FHDR):
            self.__fhdr = fhdr
        else:
            raise TypeError

    @property
    def fport(self) -> int:
        return self.__fport

    @fport.setter
    def fport(self, fport):
        if isinstance(fport, int):
            self.__fport = fport
        else:
            raise TypeError

    @property
    def frmpayload(self) -> list:
        return self.__frmpayload

    @frmpayload.setter
    def frmpayload(self, frmpayload):
        if isinstance(frmpayload, list):
            if len(frmpayload) != 0:
                self.__frmpayload = frmpayload
            else:
                self.__frmpayload = None
        else:
            raise TypeError

    @property
    def decrypted_payload(self) -> list:
        return self.__decrypted_payload

    @decrypted_payload.setter
    def decrypted_payload(self, decrypted_payload):
        if isinstance(decrypted_payload, list):
            if len(decrypted_payload) != 0:
                self.__decrypted_payload = decrypted_payload
            else:
                self.__decrypted_payload = None
        else:
            raise TypeError


class JoinRequest(Field):
    """ Define a LoRaWAN Join-Request Payload. """

    def __init__(self, *args):
        super(JoinRequest, self).__init__(*args)
        self.__joineui = None
        self.__deveui = None
        self.__devnonce = None

    def compose(self, keys):
        self.joineui = list(reversed(keys.joineui))
        self.deveui = list(reversed(keys.deveui))
        self.devnonce = keys.devnonce
        self.data = self.joineui + self.deveui + self.devnonce

    def calculate_mic(self, keys, mhdr):
        mic = mhdr.data_list
        mic += self.data_list

        cmac = AES_CMAC()
        computed_mic = cmac.encode(bytes(keys.appkey), bytes(mic))[:4]
        return list(map(int, computed_mic))

    @property
    def joineui(self) -> list:
        return self.__joineui

    @joineui.setter
    def joineui(self, joineui):
        if isinstance(joineui, list):
            self.__joineui = joineui
        else:
            raise TypeError

    @property
    def deveui(self) -> list:
        return self.__deveui

    @deveui.setter
    def deveui(self, deveui):
        if isinstance(deveui, list):
            self.__deveui = deveui
        else:
            raise TypeError

    @property
    def devnonce(self) -> list:
        return self.__devnonce

    @devnonce.setter
    def devnonce(self, devnonce):
        if isinstance(devnonce, list):
            self.__devnonce = devnonce
        else:
            raise TypeError


class JoinAccept(Field):
    """ Define a LoRaWAN Join-Accept Payload. """

    def __init__(self, *args):
        super(JoinAccept, self).__init__(*args)
        self.__joinnonce = None
        self.__netid = None
        self.__devaddr = None
        self.__dlsettings = None
        self.__rx1droffset = None
        self.__rx2datarate = None
        self.__rxdelay = None
        self.__cflist = None
        self.__decrypted_payload = None

    def decompose(self, keys, mic):
        self.decrypt_payload(keys, mic)
        self.joinnonce = self.decrypted_payload[0:3]
        self.netid = self.decrypted_payload[3:6]
        self.devaddr = list(reversed(self.decrypted_payload[6:10]))
        self.dlsettings = int.from_bytes(
            bytes(self.decrypted_payload[10:11]), byteorder='big'
        )
        self.rxdelay = int.from_bytes(
            bytes(self.decrypted_payload[11:12]), byteorder='big'
        )
        self.cflist = self.decrypted_payload[13:]
        self.set_keys(keys)

    def decrypt_payload(self, keys, mic):
        a = self.data_list
        a += mic

        cipher = AES.new(bytes(keys.appkey), AES.MODE_ECB)
        self.decrypted_payload = cipher.encrypt(bytes(a))[:-4]

    def calculate_mic(self, keys, mhdr):
        mic = mhdr.data_list
        mic += self.joinnonce
        mic += self.netid
        mic += list(reversed(self.devaddr))
        mic += [self.dlsettings]
        mic += [self.rxdelay]
        mic += self.cflist

        cmac = AES_CMAC()
        computed_mic = cmac.encode(bytes(keys.appkey), bytes(mic))[:4]
        return list(map(int, computed_mic))

    def set_keys(self, keys):
        keys.devaddr = self.devaddr
        keys.nwkskey = self.derive_session_key(keys, 0x01)
        keys.appskey = self.derive_session_key(keys, 0x02)
        keys.increment_devnonce()

    def derive_session_key(self, keys, session):
        a = [session]
        a += self.joinnonce
        a += self.netid
        a += keys.devnonce
        a += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        cipher = AES.new(bytes(keys.appkey))
        return list(map(int, cipher.encrypt(bytes(a))))

    @property
    def joinnonce(self) -> list:
        return self.__joinnonce

    @joinnonce.setter
    def joinnonce(self, joinnonce):
        if isinstance(joinnonce, list):
            self.__joinnonce = joinnonce
        else:
            raise TypeError

    @property
    def netid(self) -> list:
        return self.__netid

    @netid.setter
    def netid(self, netid):
        if isinstance(netid, list):
            self.__netid = netid
        else:
            raise TypeError

    @property
    def devaddr(self) -> list:
        return self.__devaddr

    @devaddr.setter
    def devaddr(self, devaddr):
        if isinstance(devaddr, list):
            self.__devaddr = devaddr
        else:
            raise TypeError

    @property
    def rx1droffset(self) -> int:
        return self.__rx1droffset

    @rx1droffset.setter
    def rx1droffset(self, rx1droffset):
        if isinstance(rx1droffset, int):
            self.__rx1droffset = rx1droffset
        else:
            raise TypeError

    @property
    def rx2datarate(self) -> DR:
        return self.__rx2datarate

    @rx2datarate.setter
    def rx2datarate(self, rx2datarate):
        if isinstance(rx2datarate, int):
            self.__rx2datarate = DR(rx2datarate)
        elif isinstance(rx2datarate, DR):
            self.__rx2datarate = rx2datarate
        else:
            raise TypeError

    @property
    def dlsettings(self) -> int:
        return self.__dlsettings

    @dlsettings.setter
    def dlsettings(self, dlsettings):
        if isinstance(dlsettings, int):
            self.__dlsettings = dlsettings
            self.rx1droffset = (dlsettings & 0b01110000) >> 4
            self.rx2datarate = (dlsettings & 0b00001111)
        else:
            raise TypeError

    @property
    def rxdelay(self) -> int:
        return self.__rxdelay

    @rxdelay.setter
    def rxdelay(self, rxdelay):
        if isinstance(rxdelay, int):
            self.__rxdelay = rxdelay
        else:
            raise TypeError

    @property
    def cflist(self) -> list:
        return self.__cflist

    @cflist.setter
    def cflist(self, cflist):
        if isinstance(cflist, list):
            self.__cflist = cflist
        else:
            raise TypeError

    @property
    def decrypted_payload(self) -> list:
        return self.__decrypted_payload

    @decrypted_payload.setter
    def decrypted_payload(self, decrypted_payload):
        if isinstance(decrypted_payload, list):
            if len(decrypted_payload) != 0:
                self.__decrypted_payload = decrypted_payload
            else:
                self.__decrypted_payload = None
        else:
            raise TypeError


class MHDR(Field):
    """ Define a MAC Frame Header. """

    def __init__(self, *args):
        super(MHDR, self).__init__(*args)
        self.__ftype = None
        self.__major = None

    def decompose(self):
        data = int.from_bytes(self.data, byteorder='big')
        self.ftype = (data & 0b11100000) >> 5
        self.major = (data & 0b00000011)

    def compose(self):
        data = (self.ftype.value & 0b111) << 5
        data = data | (self.major.value & 0b11)
        self.data = data

    @property
    def ftype(self) -> FTYPE:
        return self.__ftype

    @ftype.setter
    def ftype(self, ftype):
        if isinstance(ftype, FTYPE):
            self.__ftype = ftype
        elif isinstance(ftype, int):
            self.__ftype = FTYPE(ftype)
        else:
            raise TypeError

    @property
    def major(self) -> MAJOR:
        return self.__major

    @major.setter
    def major(self, major):
        if isinstance(major, MAJOR):
            self.__major = major
        elif isinstance(major, int):
            self.__major = MAJOR(major)
        else:
            raise TypeError


class PHYPayload(Field):
    """ Define a LoRaWAN Physical Payload. """

    def __init__(self, *args):
        super(PHYPayload, self).__init__(*args)
        self.__mhdr = None
        self.__macpayload = None
        self.__mic = None

    def decompose(self, keys):
        self.mhdr = self.data_list[0:1]
        self.mhdr.decompose()
        self.macpayload = self.data_list[1:-4]
        self.mic = self.data_list[-4:]
        if isinstance(self.macpayload, JoinAccept):
            self.macpayload.decompose(keys, self.mic)
        else:
            self.macpayload.decompose(keys)
        if self.mic != self.macpayload.calculate_mic(keys, self.mhdr):
            raise ValueError

    def compose(self, keys):
        self.mhdr.compose()
        data = self.mhdr.data_list
        self.macpayload.compose(keys)
        data = data + self.macpayload.data_list
        self.mic = self.macpayload.calculate_mic(keys, self.mhdr)
        data = data + self.mic

    @property
    def mhdr(self) -> MHDR:
        return self.__mhdr

    @mhdr.setter
    def mhdr(self, mhdr):
        if isinstance(mhdr, list):
            self.__mhdr = MHDR(mhdr)
        elif isinstance(mhdr, MHDR):
            self.__mhdr = mhdr
        else:
            raise TypeError

    @property
    def macpayload(self) -> MACPayload:
        return self.__macpayload

    @macpayload.setter
    def macpayload(self, macpayload):
        if isinstance(macpayload, list):
            if self.mhdr.ftype == FTYPE.JOINACCEPT:
                self.__macpayload = JoinAccept(macpayload)
            elif self.mhdr.ftype == FTYPE.JOINREQUEST:
                self.__macpayload = JoinRequest(macpayload)
            else:
                self.__macpayload = MACPayload(self.mhdr.ftype, macpayload)
        elif isinstance(macpayload, (MACPayload, JoinAccept, JoinRequest)):
            self.__macpayload = macpayload
        else:
            raise TypeError

    @property
    def mic(self) -> list:
        return self.__mic

    @mic.setter
    def mic(self, mic):
        if isinstance(mic, list):
            self.__mic = mic
        else:
            raise TypeError


class LoRaPacket(Field):
    """ Define a LoRa Packet. """

    def __init__(self, *args):
        super(LoRaPacket, self).__init__(*args)
        self.__phypayload = None

    def decompose(self, keys):
        self.phypayload = self.data_list
        self.phypayload.decompose(keys)

    def compose(self, keys):
        self.phypayload.compose(keys)
        self.data = self.phypayload.data_list

    @property
    def phypayload(self) -> PHYPayload:
        return self.__phypayload

    @phypayload.setter
    def phypayload(self, phypayload):
        if isinstance(phypayload, list):
            self.__phypayload = PHYPayload(phypayload)
        elif isinstance(phypayload, PHYPayload):
            self.__phypayload = phypayload
        else:
            raise TypeError
