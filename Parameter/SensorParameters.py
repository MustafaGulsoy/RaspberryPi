
import Adafruit_ADS1x15
import pigpio
import smbus
from prettytable import PrettyTable



adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

DEVICE = 0x76  # Default device I2C address

bus = smbus.SMBus(1)

RX = 23
pigpio.exceptions = False
pi = pigpio.pi()
pi.set_mode(RX, pigpio.INPUT)
pi.bb_serial_read_open(RX, 115200)

RX2 = 23
pigpio.exceptions = False
pi2 = pigpio.pi()
pi2.set_mode(RX2, pigpio.INPUT)
pi2.bb_serial_read_open(RX2, 115200)


RX3 = 22
pigpio.exceptions = False
pi3 = pigpio.pi()
pi3.set_mode(RX3, pigpio.INPUT)
pi3.bb_serial_read_open(RX3, 115200)


PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

mpu_bus = smbus.SMBus(1)
mpu_device_Address = 0x68
