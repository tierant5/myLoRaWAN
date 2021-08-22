import Device
import DeviceInfo
from Keys import Keys
import LoRaPacket
from constants import ACTIVATION, MAJOR, FTYPE


class LoRaWAN(Device.ClassC):
    """ Class to unify LoRaWAN Stack """

    def __init__(
        self, activation=ACTIVATION.OTAA,
        version=MAJOR.LORAWANR1, *args
    ):
        super(LoRaWAN, self).__init__(*args)
        self.__keys = None
        self.__activation = None
        self.__fcnt = None
        self.__rx_packet = None
        self.__tx_packet = None
        self.__version = None
        self.__rx_data = None

        self.activation = activation
        self.version = version
        self.load_device_info()

    def on_rx_done(self):
        super(LoRaWAN, self).on_rx_done()
        self.rx_packet = LoRaPacket.LoRaPacket(self.rx_payload)
        self.decompose_packet()

    def on_tx_done(self):
        super(LoRaWAN, self).on_tx_done()
        self.fcnt += 1

    def send_packet(self):
        self.tx_packet.compose(self.keys)
        self.tx(self.tx_packet.data_list)

    def send_join_request(self):
        mhdr = LoRaPacket.MHDR()
        mhdr.ftype = FTYPE.JOINREQUEST
        mhdr.major = self.version
        phypayload = LoRaPacket.PHYPayload()
        phypayload.mhdr = mhdr
        packet = LoRaPacket.LoRaPacket()
        packet.phypayload = phypayload
        packet.compose(self.keys)
        self.mac.rx_delay1 = self.mac.join_accept_delay1
        self.tx(packet.data_list)

    def load_device_info(self):
        if self.activation == ACTIVATION.OTAA:
            self.keys.appkey = DeviceInfo.appkey
            self.keys.joineui = DeviceInfo.joineui
            self.keys.deveui = DeviceInfo.deveui
        else:
            self.keys.devaddr = DeviceInfo.devaddr
            self.keys.nwkskey = DeviceInfo.nwkskey
            self.keys.appskey = DeviceInfo.appskey

    def setup_tx_packet(self, ftype=FTYPE.UNCONFDATAUP):
        self.tx_packet = LoRaPacket.LoRaPacket()
        self.tx_packet.phypayload = LoRaPacket.PHYPayload()
        self.tx_packet.phypayload.mhdr = LoRaPacket.MHDR()
        self.tx_packet.phypayload.macpayload = LoRaPacket.MACPayload()
        self.tx_packet.phypayload.macpayload.fhdr = LoRaPacket.FHDR()
        self.tx_packet.phypayload.macpayload.fhdr.fctrl = LoRaPacket.FCtrl_Uplink()     # noqa: E501
        self.tx_packet.phypayload.macpayload.fhdr.fcnt = self.fcnt
        self.tx_packet.phypayload.macpayload.fhdr.fopts = LoRaPacket.FOpts(ftype)   # noqa: E501
        self.tx_packet.phypayload.mhdr.major = self.version
        self.tx_packet.phypayload.mhdr.ftype = ftype

    def decompose_packet(self):
        self.rx_packet.decompose(self.keys)
        self.setup_tx_packet()
        macpayload = self.rx_packet.phypayload.macpayload
        if self.rx_packet.phypayload.mhdr.ftype == FTYPE.JOINACCEPT:
            self.decompose_join_accept(macpayload)
        elif self.rx_packet.phypayload.mhdr.ftype == FTYPE.UNCONFDATADOWN:
            self.decompose_data_down(macpayload)

    def decompose_join_accept(self, macpayload):
        self.mac.set_defaults(self.mac.band)
        self.mac.rx1droffset = macpayload.rx1droffset
        self.mac.rx2_data_rate = macpayload.rx2datarate
        self.mac.rx_delay1 = macpayload.rxdelay
        self.tx_packet.phypayload.mhdr.ftype = FTYPE.CONFDATAUP

    def decompose_data_down(self, macpayload):
        mac_commands = []
        if macpayload.fport is not None:
            if macpayload.fport == 0:
                self.rx_data = []
                mac_commands = LoRaPacket.FOpts(
                    macpayload.ftype, macpayload.decrypted_payload
                    )
                mac_commands.decompose()
                mac_commands = mac_commands.mac_commands
            else:
                self.rx_data = macpayload.decrypted_payload
                if macpayload.fhdr.fctrl.foptslen != 0:
                    mac_commands = macpayload.fhdr.fopts.mac_commands
        else:
            self.rx_data = []
            if macpayload.fhdr.fctrl.foptslen != 0:
                mac_commands = macpayload.fhdr.fopts.mac_commands
        self.decompose_mac_commands(mac_commands)

    def decompose_mac_commands(self, commands):
        for command in commands:
            if isinstance(command, LoRaPacket.LinkCheckAns):
                pass
            elif isinstance(command, LoRaPacket.LinkADRReq):
                self.mac.tx_data_rate = command.datarate
                self.mac.tx_power = command.txpower
                # self.mac.chmask = command.chmask
                # self.mac.chmaskcntl = command.chmaskcntl
                self.mac.tx_retries = command.nbtrans
            elif isinstance(command, LoRaPacket.DutyCycleReq):
                self.mac.duty_cycle = command.maxdutycycle
            elif isinstance(command, LoRaPacket.RXParamSetupReq):
                self.mac.rx1droffset = command.rx1droffset
                self.mac.rx2_data_rate = command.rx2datarate
                for channel in self.mac.band.channel_list:
                    if channel.frequency == command.frequency:
                        self.mac.rx2_channel = channel
                        break
            elif isinstance(command, LoRaPacket.DevStatusReq):
                pass
            elif isinstance(command, LoRaPacket.NewChannelReq):
                pass
            elif isinstance(command, LoRaPacket.DLChannelReq):
                pass
            elif isinstance(command, LoRaPacket.RXTimingSetupAns):
                self.mac.rx_delay1 = command.delay
            elif isinstance(command, LoRaPacket.TXParamSetupReq):
                pass
            elif isinstance(command, LoRaPacket.DeviceTimeAns):
                pass

    @property
    def keys(self) -> Keys:
        return self.__keys

    @keys.setter
    def keys(self, keys):
        if isinstance(keys, Keys):
            self.__keys = keys
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
    def version(self) -> MAJOR:
        return self.__version

    @version.setter
    def version(self, version):
        if isinstance(version, MAJOR):
            self.__version = version
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

    @property
    def rx_packet(self) -> LoRaPacket.LoRaPacket:
        self.__rx_packet

    @rx_packet.setter
    def rx_packet(self, rx_packet):
        if isinstance(rx_packet, LoRaPacket.LoRaPacket):
            self.__rx_packet = rx_packet
        else:
            raise TypeError

    @property
    def tx_packet(self) -> LoRaPacket.LoRaPacket:
        self.__tx_packet

    @tx_packet.setter
    def tx_packet(self, tx_packet):
        if isinstance(tx_packet, LoRaPacket.LoRaPacket):
            self.__tx_packet = tx_packet
        else:
            raise TypeError

    @property
    def rx_data(self) -> list:
        return self.__rx_data

    @rx_data.setter
    def rx_data(self, rx_data):
        if isinstance(rx_data, list):
            self.__rx_data = rx_data
        else:
            raise TypeError
