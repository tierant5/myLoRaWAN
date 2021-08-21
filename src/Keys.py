from random import randrange


class Keys:
    """ Class to define Keys in LoRaWAN Protocol. """

    def __init__(self, **kwargs):
        self.__devaddr = None
        self.__nwkskey = None
        self.__appskey = None
        self.__devnonce = None
        self.__appeui = None
        self.__deveui = None
        self.__appkey = None

        for key, value in kwargs.items():
            if key == 'devaddr':
                self.devaddr = value
            elif key == 'nwkskey':
                self.nwkskey = value
            elif key == 'appskey':
                self.appskey = value
            elif key == 'appeui':
                self.appeui = value
            elif key == 'deveui':
                self.deveui = value
            elif key == 'appkey':
                self.appkey = value
            else:
                raise KeyError

    @property
    def devaddr(self) -> list:
        return self.__devaddr

    @devaddr.setter
    def devaddr(self, devaddr):
        if isinstance(devaddr, list):
            if len(devaddr) == 4:
                self.__devaddr = devaddr
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def nwkskey(self) -> list:
        return self.__nwkskey

    @nwkskey.setter
    def nwkskey(self, nwkskey):
        if isinstance(nwkskey, list):
            if len(nwkskey) == 16:
                self.__nwkskey = nwkskey
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def appskey(self) -> list:
        return self.__appskey

    @appskey.setter
    def appskey(self, appskey):
        if isinstance(appskey, list):
            if len(appskey) == 16:
                self.__appskey = appskey
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def devnonce(self) -> list:
        if self.__devnonce is None:
            self.__devnonce = [randrange(256), randrange(256)]
        else:
            old_devnonce = int.from_bytes(
                bytes(self.__devnonce), byteorder='big'
            )
            new_devnonce = [byte for byte in bytes(old_devnonce + 1)]
            self.__devnonce = new_devnonce[-2:]
        return self.__devnonce

    @property
    def appeui(self) -> list:
        return self.__appeui

    @appeui.setter
    def appeui(self, appeui):
        if isinstance(appeui, list):
            if len(appeui) == 8:
                self.__appeui = appeui
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def deveui(self) -> list:
        return self.__deveui

    @deveui.setter
    def deveui(self, deveui):
        if isinstance(deveui, list):
            if len(deveui) == 8:
                self.__deveui = deveui
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def appkey(self) -> list:
        return self.__appkey

    @appkey.setter
    def appkey(self, appkey):
        if isinstance(appkey, list):
            if len(appkey) == 16:
                self.__appkey = appkey
            else:
                raise ValueError
        else:
            raise TypeError
