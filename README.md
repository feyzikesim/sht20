# SHT20 Temperature & Humidity Sensor Driver for Python3

SHT20 is a Temperature & Humidity sensor manufactured by Sensirion. With this driver, you can use SHT20 with Python3 over I2C.

## Dependencies
Only smbus2 other than Python. 

## Installation
```bash
pip3 install sht20
```

## Usage
```bash
run-sht20
```
or
```python
from sht20 import SHT20
from time import sleep

sht = SHT20(1, resolution=SHT20.TEMP_RES_14bit)

temp = sht.read_temp()
humid = sht.read_humid()

#   or

data = sht.read_all()
temp = data[0]
humid = data[1]

print("Temperature (°C): " + str(temp))
print("Humidity (%RH): " + str(humid))
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
