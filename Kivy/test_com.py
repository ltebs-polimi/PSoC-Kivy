#!/usr/bin/python3

from communication import *

ks = KivySerial()
#ks.find_port()
ks.port_name = '/dev/ttyACM1'
if ks.connect() == 0:
    print("Connected")

# Empty the buffer
ks.port.flush()
while len(ks.port.read(1)) > 0:
    pass

print("buffer empty.")

# Start streaming
ks.port.write('b'.encode('utf-8'))
ks.is_streaming = 1

skipped_bytes = 0
b = 0

while ks.is_streaming:

    while b != 160:
        skipped_bytes += 1
        b = ks.port.read(1)
        if len(b) > 0:
            b = struct.unpack('B', b)[0]
        #print(b)

    print(f"Skipped {skipped_bytes} bytes before 0xA0")
    skipped_bytes = 0

    data = ks.port.read(3)
    data = struct.unpack('3B', data)
    print(f"raw data = {data[0]} {data[1]}")
    sensor_data = (((data[0] << 8) & 0xFFFF) | data[1])
    sensor_data = sensor_data/65535*5
    if data[2] == 192:
        # valid sample
        print(f"Sample {ks.samples_counter}: {sensor_data}")
        ks.samples_counter += 1
        b = ks.port.read(1)
        b = struct.unpack('B', b)[0]
        print(b)
    else:
        print("Invalid data.")
