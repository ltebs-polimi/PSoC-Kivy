#!/usr/bin/python3

import serial
import struct

s = serial.Serial('/dev/ttyACM1', baudrate=115200, timeout=1)

if s.is_open:
    print("Connected to /dev/ttyACM1")

s.flush()
while len(s.read(1)) > 0:
    pass

print("buffer empty.")

s.write('b'.encode('utf-8'))
streaming = 1

skipped_bytes = 0
b = 0
samples_counter = 0

while streaming:
    while b != 160:
        skipped_bytes += 1
        b = s.read(1)
        if len(b) > 0:
            b = struct.unpack('B', b)[0]
        #print(b)

    print(f"Skipped {skipped_bytes} bytes before 0xA0")
    skipped_bytes = 0

    data = s.read(3)
    data = struct.unpack('3B', data)
    print(f"raw data = {data[0]} {data[1]}")
    sensor_data = (((data[0] << 8) & 0xFFFF) | data[1])
    sensor_data = sensor_data/65535*5
    if data[2] == 192:
        # valid sample
        print(f"Sample {samples_counter}: {sensor_data}")
        samples_counter += 1
        b = s.read(1)
        b = struct.unpack('B', b)[0]
        print(b)
    else:
        print("Invalid data.")
