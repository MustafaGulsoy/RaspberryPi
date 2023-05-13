#!/usr/bin/env python3
## -*- coding: utf-8 -*
import time
from ctypes import c_short

import Parameter.SensorParameters as params

from prettytable import PrettyTable


def get_data_by_TFmini_1():
    while True:

        time.sleep(0.1)  # change the value if needed
        (count, recv) = params.pi.bb_serial_read(params.RX)

        if count > 8:
            for i in range(0, count - 9):
                if recv[i] == 89 and recv[i + 1] == 89:  # 0x59 is 89
                    checksum = 0
                    for j in range(0, 8):
                        checksum = checksum + recv[i + j]
                    checksum = checksum % 256
                    if checksum == recv[i + 8]:
                        distance = recv[i + 2] + recv[i + 3] * 256
                        strength = recv[i + 4] + recv[i + 5] * 256

                        return distance


def get_data_by_TFmini_2():
    while True:

        time.sleep(0.1)
        (count, recv) = params.pi2.bb_serial_read(params.RX2)

        if count > 8:
            for i in range(0, count - 9):
                if recv[i] == 89 and recv[i + 1] == 89:  # 0x59 is 89
                    checksum = 0
                    for j in range(0, 8):
                        checksum = checksum + recv[i + j]
                    checksum = checksum % 256
                    if checksum == recv[i + 8]:
                        distance = recv[i + 2] + recv[i + 3] * 256
                        strength = recv[i + 4] + recv[i + 5] * 256

                        return distance


def get_data_by_TFmini_3():
    while True:

        time.sleep(0.1)
        (count, recv) = params.pi3.bb_serial_read(params.RX3)

        if count > 8:
            for i in range(0, count - 9):
                if recv[i] == 89 and recv[i + 1] == 89:
                    checksum = 0
                    for j in range(0, 8):
                        checksum = checksum + recv[i + j]
                    checksum = checksum % 256
                    if checksum == recv[i + 8]:
                        distance = recv[i + 2] + recv[i + 3] * 256
                        strength = recv[i + 4] + recv[i + 5] * 256

                        return distance


def get_WPS_data():
    while True:
        value = [0]
        value[0] = params.adc.read_adc(0, gain=1)
        volts = value[0] / 32767.0 * 6.144
        psi = 50.0 * volts - 25.0
        bar = psi * 0.0689475729
        a = bar
        return a


# ----------------------------------------------------------------------


def MPU_Init():
    params.mpu_bus.write_byte_data(params.mpu_device_Address, params.SMPLRT_DIV, 7)

    params.mpu_bus.write_byte_data(params.mpu_device_Address, params.PWR_MGMT_1, 1)

    params.mpu_bus.write_byte_data(params.mpu_device_Address, params.CONFIG, 0)

    params.mpu_bus.write_byte_data(params.mpu_device_Address, params.GYRO_CONFIG, 24)

    params.mpu_bus.write_byte_data(params.mpu_device_Address, params.INT_ENABLE, 1)


def read_raw_data(addr):
    high = params.mpu_bus.read_byte_data(params.mpu_device_Address, addr)
    low = params.mpu_bus.read_byte_data(params.mpu_device_Address, addr + 1)

    value = ((high << 8) | low)

    if (value > 32768):
        value = value - 65536
    return value


def get_MPU_data():
    MPU_Init()

    while True:
        acc_x = read_raw_data(params.ACCEL_XOUT_H)
        acc_y = read_raw_data(params.ACCEL_YOUT_H)
        acc_z = read_raw_data(params.ACCEL_ZOUT_H)

        gyro_x = read_raw_data(params.GYRO_XOUT_H)
        gyro_y = read_raw_data(params.GYRO_YOUT_H)
        gyro_z = read_raw_data(params.GYRO_ZOUT_H)

        Ax = acc_x / 16384.0
        Ay = acc_y / 16384.0
        Az = acc_z / 16384.0

        Gx = gyro_x / 131.0
        Gy = gyro_y / 131.0
        Gz = gyro_z / 131.0
        return Gx, Gy, Gz, Ax, Ay, Az,


# def get_BME_data():
def get_short(data, index):
    return c_short((data[index + 1] << 8) + data[index]).value


def get_UShort(data, index):
    return (data[index + 1] << 8) + data[index]


def get_char(data, index):
    result = data[index]
    if result > 127:
        result -= 256
    return result


def get_UChar(data, index):
    result = data[index] & 0xFF
    return result


def read_BME280ID(addr=params.DEVICE):
    REG_ID = 0xD0
    (chip_id, chip_version) = params.bus.read_i2c_block_data(addr, REG_ID, 2)
    return (chip_id, chip_version)


def read_BME280_All(addr=params.DEVICE):
    REG_DATA = 0xF7
    REG_CONTROL = 0xF4
    REG_CONFIG = 0xF5

    REG_CONTROL_HUM = 0xF2
    REG_HUM_MSB = 0xFD
    REG_HUM_LSB = 0xFE

    OVERSAMPLE_TEMP = 2
    OVERSAMPLE_PRES = 2
    MODE = 1

    OVERSAMPLE_HUM = 2
    params.bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

    control = OVERSAMPLE_TEMP << 5 | OVERSAMPLE_PRES << 2 | MODE
    params.bus.write_byte_data(addr, REG_CONTROL, control)

    cal1 = params.bus.read_i2c_block_data(addr, 0x88, 24)
    cal2 = params.bus.read_i2c_block_data(addr, 0xA1, 1)
    cal3 = params.bus.read_i2c_block_data(addr, 0xE1, 7)

    dig_T1 = get_UShort(cal1, 0)
    dig_T2 = get_short(cal1, 2)
    dig_T3 = get_short(cal1, 4)

    dig_P1 = get_UShort(cal1, 6)
    dig_P2 = get_short(cal1, 8)
    dig_P3 = get_short(cal1, 10)
    dig_P4 = get_short(cal1, 12)
    dig_P5 = get_short(cal1, 14)
    dig_P6 = get_short(cal1, 16)
    dig_P7 = get_short(cal1, 18)
    dig_P8 = get_short(cal1, 20)
    dig_P9 = get_short(cal1, 22)

    dig_H1 = get_UChar(cal2, 0)
    dig_H2 = get_short(cal3, 0)
    dig_H3 = get_UChar(cal3, 2)

    dig_H4 = get_char(cal3, 3)
    dig_H4 = (dig_H4 << 24) >> 20
    dig_H4 = dig_H4 | (get_char(cal3, 4) & 0x0F)

    dig_H5 = get_char(cal3, 5)
    dig_H5 = (dig_H5 << 24) >> 20
    dig_H5 = dig_H5 | (get_UChar(cal3, 4) >> 4 & 0x0F)

    dig_H6 = get_char(cal3, 6)

    wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + (
            (2.3 * OVERSAMPLE_HUM) + 0.575)
    time.sleep(wait_time / 1000)

    data = params.bus.read_i2c_block_data(addr, REG_DATA, 8)
    pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    hum_raw = (data[6] << 8) | data[7]

    var1 = ((((temp_raw >> 3) - (dig_T1 << 1))) * (dig_T2)) >> 11
    var2 = (((((temp_raw >> 4) - (dig_T1)) * ((temp_raw >> 4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
    t_fine = var1 + var2
    temperature = float(((t_fine * 5) + 128) >> 8)

    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * dig_P6 / 32768.0
    var2 = var2 + var1 * dig_P5 * 2.0
    var2 = var2 / 4.0 + dig_P4 * 65536.0
    var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * dig_P1
    if var1 == 0:
        pressure = 0
    else:
        pressure = 1048576.0 - pres_raw
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
        var1 = dig_P9 * pressure * pressure / 2147483648.0
        var2 = pressure * dig_P8 / 32768.0
        pressure = pressure + (var1 + var2 + dig_P7) / 16.0

    humidity = t_fine - 76800.0
    humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (
            1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
    humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
    if humidity > 100:
        humidity = 100
    elif humidity < 0:
        humidity = 0

    return temperature / 100.0, pressure / 100.0, humidity


def main():
    (chip_id, chip_version) = read_BME280ID()

    temperature, pressure, humidity = read_BME280_All()
    Gx, Gy, Gz, Ax, Ay, Az = get_MPU_data()
    MOVE_CURSOR_UP = "\033[1A"
    ERASE = "\x1b[2K"

    myTable = PrettyTable(["Sensor Name:", "Value"])
    myTable.add_row(["Lidar1 cm", get_data_by_TFmini_1()])
    myTable.add_row(["Lidar2 cm", get_data_by_TFmini_2()])
    myTable.add_row(["Lidar3 cm", get_data_by_TFmini_3()])
    myTable.add_row(["Gyro Gx", Gx])
    myTable.add_row(["Gyro Gy", Gy])
    myTable.add_row(["Gyro Gz", Gz])
    myTable.add_row(["Gyro Ax", Ax])
    myTable.add_row(["Gyro Ay", Ay])
    myTable.add_row(["Gyro Az", Az])
    myTable.add_row(["Bar", get_WPS_data()])
    myTable.add_row(["Temperature C", temperature])
    myTable.add_row(["Pressure hPa", pressure])
    myTable.add_row(["Humidity %", humidity])
    print(myTable)

# while True:
#     print(getTFminiData2())
#     time.sleep(1)
