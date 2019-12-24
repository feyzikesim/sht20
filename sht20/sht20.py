from smbus2 import i2c_msg, SMBus
from time import sleep

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def calculateCRC(input):
    crc = 0x0
    for i in range (0, 2):
        crc = crc ^ input[i]
        for j in range(8, 0, -1):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc = crc << 1
    crc = crc & 0x0000FF
    return crc

def checkCRC(result):
    for i in range(2, len(result), 3):
        data = []
        data.append(result[i-2])
        data.append(result[i-1])

        crc = result[i]

        if crc == calculateCRC(data):
            crc_result = True
        else:
            crc_result = False
    return crc_result

class SHT20():
    SHT20_ADDR = 0x40

    TRIG_TEMP_HOLD = 0xE3
    TRIG_HUMID_HOLD = 0xE5
    TRIG_TEMP_NOHOLD = 0xF3
    TRIG_HUMID_NOHOLD = 0xF5
    WRITE_USER_REG = 0xE6
    READ_USER_REG = 0xE7
    SOFT_RESET = 0xFE

    TEMP_RES_14bit = 0x00
    TEMP_RES_13bit = 0x80
    TEMP_RES_12bit = 0x01
    TEMP_RES_11bit = 0x81
    END_OF_BATTERY = 0x40
    ENABLE_HEATER = 0x04
    DISABLE_OTP_RELOAD = 0x02

    NO_ERROR = 0
    ERROR = -1

    def __init__(self, port, resolution):
        self.bus = SMBus(port)
        self.sht20_init(resolution)

    def sht20_init(self, inits):
        self.bus.write_byte(self.SHT20_ADDR, self.SOFT_RESET)
        sleep(1)
        self.bus.write_byte_data(self.SHT20_ADDR, self.WRITE_USER_REG, inits | self.DISABLE_OTP_RELOAD)

    def start_temp_measurement(self):
        self.bus.write_byte(self.SHT20_ADDR, self.TRIG_TEMP_NOHOLD)
        sleep(0.1)

    def start_humid_measurement(self):
        self.bus.write_byte(self.SHT20_ADDR, self.TRIG_HUMID_NOHOLD)
        sleep(0.1)

    def read_temp(self):
        temp_list = []

        self.start_temp_measurement()

        readTemp = i2c_msg.read(self.SHT20_ADDR, 3)
        self.bus.i2c_rdwr(readTemp)

        for i in range(readTemp.len):
            temp_list.append(bytes_to_int(readTemp.buf[i]))

        if checkCRC(temp_list):
            temp_list[1] &= 0xFC
            temp = (((temp_list[0] * pow(2, 8) + temp_list[1]) * 175.72) / pow(2, 16)) - 46.85
            return temp
        else:
            return self.ERROR

    def read_humid(self):
        humid_list = []

        self.start_humid_measurement()

        readHumid = i2c_msg.read(self.SHT20_ADDR, 3)
        self.bus.i2c_rdwr(readHumid)

        for i in range(readHumid.len):
            humid_list.append(bytes_to_int(readHumid.buf[i]))

        if checkCRC(humid_list):
            humid_list[1] &= 0xFC
            humid = (((humid_list[0] * pow(2, 8) + humid_list[1]) * 125) / pow(2, 16)) - 6
            return humid
        else:
            return self.ERROR

    def read_all(self):
        data_list = []
        data_list.append(self.read_temp())
        data_list.append(self.read_humid())

        return data_list

    def device_reset(self):
        self.bus.write_byte(self.SHT20_ADDR, self.SOFT_RESET)
        sleep(1)
