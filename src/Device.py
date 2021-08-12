from SX127x import LoRa
from constants import DEVCLASS, MODE, RXMODE
from LoRaMAC import LoRaMAC
from Radio import Radio, SX127X
import asyncio


class Device(LoRa):
    """ Base Class of LoRaWAN Device """

    def __init__(self, mac, radio=SX127X()):
        super(Device, self).__init__()
        self.__device_class = None
        self.__mac = None
        self.__radio = None
        self.__rx_mode = None

        self.delay1 = None
        self.delay2 = None

        self.mac = mac
        self.radio = radio

    def on_rx_done(self):
        if self.rx_mode in [RXMODE.RX1, RXMODE.RX2]:
            self.rx1_timeout = False
            self.rx2_timeout = False
            if (self.delay2 is not None) and (self.rx_mode == RXMODE.RX1):
                self.delay2.cancel()
        self.clear_irq_flags(RxDone=1)
        self.rx_payload = self.read_payload(nocheck=True)
        self.setup_rx_done()

    def on_rx_timeout(self):
        self.clear_irq_flags(RxTimeout=1)
        if self.rx_mode == RXMODE.RX1:
            self.rx1_timeout = True
            self.rx2_timeout = False
            self.setup_rx1_timeout()
        else:
            self.rx1_timeout = True
            self.rx2_timeout = True
            self.setup_rx2_timeout()

    def on_tx_done(self):
        self.clear_irq_flags(TxDone=1)
        asyncio.run(self.async_start_rx_delays())

    def tx(self, tx_payload):
        self.rx_mode = RXMODE.OFF
        max_tx_power_code = self.radio.dbm2code(self.radio.max_tx_power)
        if self.mac.tx_power < self.radio.min_tx_power:
            tx_power_code = self.radio.dbm2code(self.radio.min_tx_power)
        elif self.mac.tx_power > self.radio.max_tx_power:
            tx_power_code = max_tx_power_code
        else:
            tx_power_code = self.radio.dbm2code(self.mac.tx_power)
        self.clear_irq_flags(RxDone=1)
        self.set_mode(self.get_radio_mode(MODE.SLEEP))
        self.set_dio_mapping([1, 0, 0, 0, 0, 0])
        self.set_freq(self.mac.tx_channel.frequency / self.radio.freq_scale)
        self.set_bw(self.get_radio_bw(self.mac.tx_data_rate.bandwidth))
        self.set_spreading_factor(
            self.get_radio_sf(self.mac.tx_data_rate.spreading_factor)
        )
        self.set_pa_config(
            max_power=max_tx_power_code,
            output_power=tx_power_code
        )
        self.set_sync_word(0x34)
        self.set_rx_crc(True)
        self.set_invert_iq(0)
        assert(self.get_agc_auto_on() == 1)
        self.write_payload(tx_payload)
        self.set_mode(self.get_radio_mode(MODE.TX))

    def rx(self, channel, data_rate, mode):
        self.set_mode(self.get_radio_mode(MODE.SLEEP))
        self.set_dio_mapping([0, 0, 0, 0, 0, 0])
        self.set_freq(channel.frequency / self.radio.freq_scale)
        self.set_bw(self.get_radio_bw(data_rate.bandwidth))
        self.set_spreading_factor(
            self.get_radio_sf(data_rate.spreading_factor)
        )
        self.set_pa_config(pa_select=1)
        self.set_sync_word(0x34)
        self.set_rx_crc(False)
        self.set_invert_iq(1)
        self.reset_ptr_rx()
        self.set_mode(self.get_radio_mode(mode))

    def setup_rx1(self):
        self.rx_mode = RXMODE.RX1
        self.rx(
            channel=self.mac.rx1_channel,
            data_rate=self.mac.rx1_data_rate,
            mode=MODE.RXSINGLE
        )

    def setup_rx2(self):
        self.rx_mode = RXMODE.RX2
        self.rx(
            channel=self.mac.rx2_channel,
            data_rate=self.mac.rx2_data_rate,
            mode=MODE.RXSINGLE
        )

    def setup_rx_done(self):
        self.set_mode(self.get_radio_mode(MODE.SLEEP))

    async def async_start_rx_delays(self):
        self.delay1 = asyncio.create_task(self.async_rx1_delay())
        self.delay2 = asyncio.create_task(self.async_rx2_delay())
        await asyncio.gather(self.delay1, self.delay2)

    async def async_rx1_delay(self):
        await asyncio.sleep(self.mac.rx_delay1)
        self.setup_rx1()

    async def async_rx2_delay(self):
        try:
            await asyncio.sleep(self.mac.rx_delay2)
            self.setup_rx2()
        except asyncio.CancelledError:
            pass

    def setup_rx1_timeout(self):
        self.rx_mode = RXMODE.OFF
        self.set_mode(self.get_radio_mode(MODE.STDBY))

    def setup_rx2_timeout(self):
        self.rx_mode = RXMODE.OFF
        self.set_mode(self.get_radio_mode(MODE.SLEEP))

    def get_radio_mode(self, mode):
        return self.radio.mode_table[mode]

    def get_radio_sf(self, sf):
        return self.radio.sf_table[sf]

    def get_radio_bw(self, bw):
        return self.radio.bw_table[bw]

    def get_radio_coding_rate(self, coding_rate):
        return self.radio.coding_rate_table[coding_rate]

    @property
    def device_class(self) -> DEVCLASS:
        return self.__device_class

    @device_class.setter
    def device_class(self, device_class: DEVCLASS):
        if self.__device_class is None:
            if isinstance(device_class, DEVCLASS):
                self.__device_class = device_class
            else:
                raise TypeError
        else:
            raise ValueError(f'{self}.__device_class already exists!')

    @property
    def mac(self) -> LoRaMAC:
        return self.__mac

    @mac.setter
    def mac(self, mac):
        if isinstance(mac, LoRaMAC):
            self.__mac = mac
        else:
            raise TypeError

    @property
    def radio(self) -> Radio:
        return self.__radio

    @radio.setter
    def radio(self, radio):
        if isinstance(radio, Radio):
            self.__radio = radio
        else:
            raise TypeError

    @property
    def rx_mode(self) -> RXMODE:
        return self.__rx_mode

    @rx_mode.setter
    def rx_mode(self, rx_mode):
        if isinstance(rx_mode, RXMODE):
            self.__rx_mode = rx_mode
        else:
            raise TypeError


class ClassA(Device):
    """ Class to define LoRaWAN Class A Device """

    def __init__(self, *args):
        super(ClassA, self).__init__(*args)
        self.device_class = DEVCLASS.CLASS_A


class ClassC(Device):
    """ Class to define LoRaWAN Class C Device """

    def __init__(self, *args):
        super(ClassC, self).__init__(*args)
        self.device_class = DEVCLASS.CLASS_C

    def setup_rx1_timeout(self):
        """ Override Class A Timeout """
        self.setup_rxc()

    def setup_rx2_timeout(self):
        """ Override Class A Timeout """
        self.setup_rxc()

    def setup_rxc(self):
        self.rx_mode = RXMODE.RXC
        self.rx(
            channel=self.mac.rx2_channel,
            data_rate=self.mac.rx2_data_rate,
            mode=MODE.RXCONT
        )

    def on_tx_done(self):
        self.clear_irq_flags(TxDone=1)
        self.setup_rxc()
        asyncio.run(self.async_start_rx_delays())

    def setup_rx_done(self):
        self.setup_rxc()


if __name__ == '__main__':
    loramac = LoRaMAC()
    device = ClassA(loramac)
