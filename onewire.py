from serial import Serial

class OneWireError(Exception):
    pass

class OneWire:

    def __init__(self):
        self._ser = Serial('COM3', timeout=1)

    def reset(self, required=False):
        self._ser.baudrate = 9600
        self._ser.write(b'\x0f')
        out = self._ser.read(1)
        if out != b'\x0f':
            raise OneWireError
        self._ser.baudrate = 115200

    def readbit(self):
        self._ser.write(b'\xff')
        return self._ser.read(1)[0] & 1

    def readbyte(self):
        value = 0
        for i in range(8):
            bit = self.readbit()
            value = value | (bit << i)
        return value

    def writebit(self, value):
        # translating bits to bytes 1 is 0xFF and 0 is 0x00
        ext_value = (value << 8) - value
        byte_value = ext_value.to_bytes(1, 'big')
        self._ser.write(byte_value)
        self._ser.read(1)

    def writebyte(self, value):
        for i in range(8):
            self.writebit((value >> i) & 1)
