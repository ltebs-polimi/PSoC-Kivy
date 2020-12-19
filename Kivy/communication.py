from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, StringProperty
import serial
import serial.tools.list_ports as list_ports
import struct
import threading
import time

"""
@brief Start byte of the data packet
"""
START_BYTE = 0xA0

"""
@brief End byte of the data packet
"""
END_BYTE = 0xC0

"""
@brief Connection command.
"""
CONNECTION_CMD = 'v'

"""
@brief Start streaming command.
"""
START_STREAMING_CMD = 'b'

"""
@brief Stop streaming command.
"""
STOP_STREAMING_CMD = 's'

"""
@brief Select wave as sine.
"""
WAVE_SINE_CMD = 'e'

"""
@brief Select wave as triangle.
"""
WAVE_TRIANGLE_CMD = 'f'

"""
@brief Select range as small.
"""
RANGE_SMALL_CMD = 't'

"""
@brief Select range as large.
"""
RANGE_LARGE_CMD = 'y'

class Singleton(type):
    """
    @brief Class used for Singleton pattern.

    This class allows to implement the Singleton pattern.
    This pattern restricts the instantiation of a class
    to one single instance. 
    [Link](https://en.wikipedia.org/wiki/Singleton_pattern)
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class KivySerial(EventDispatcher, metaclass=Singleton):
    """
    @brief Main class used for serial communication.
    
    This is the main class used to communicate with the serial port.
    It has @Singleton as a metaclass, so only one instance of this
    class exists throughout the application. 
    Automatic port discovery is implemented: it is not required to
    specify the serial port, as it is automatically detected by
    scanning all the available ports, and sending a known command
    to the port. If the expected response is detected, then 
    a connection with the serial port is carried out.
    """

    """
    @brief Connection status.

    0 means that the port is not connected, 1 that the
    port was found, 2 that a successfull connection was
    achieved.
    """
    connected = NumericProperty(0)

    """
    @brief Message to be shown.

    This is a string that is shown on the GUI for messages
    related to the serial communication.
    """
    message_string = StringProperty('')

    def __init__(self, baudrate=115200):
        """
        @brief Initialize the class.

        Args:
            - baudrate: the desired baudrate for serial communication.
        """
        self.port_name = ""         # port name, set later when port is found
        self.baudrate = baudrate    # baudrate for serial communication
        self.is_streaming = False   # streaming status
        self.connected = 0          # connection status
        self.read_state = 0         # read state for data parser
        self.callbacks = []         # list of callbacks to be called when new data are available
        self.samples_counter = 0    # counter for samples received
        self.timeout = 1        
        # Start thread for automatic port discovery
        find_port_thread = threading.Thread(target=self.find_port, daemon=True)
        find_port_thread.start()
        

    def add_callback(self, callback):
        """
        @brief Add callback.

        Add a callback to the list of callbacks
        that are called when a new sample is
        available.
        """
        if (callback not in self.callbacks):
            self.callbacks.append(callback)

    def find_port(self):
        """
        @brief Automatic port discovery.

        This function scans all the available COM ports
        to check if one of them is correct one. It does it
        by sending a #CONNECTION_CMD and checking if three
        $$$ are found in the response.
        """
        wave_dac_port_found = False
        while (not wave_dac_port_found):
            ports = list_ports.comports()
            for port in ports:
                wave_dac_port_found = self.check_wave_dac_port(port.device)
                if (wave_dac_port_found):
                    self.port_name = port.device
                    if (self.connect() == 0):
                        break

    def check_wave_dac_port(self, port_name):
        """
        @brief Check if port is the desired one.

        This function sends a #CONNECTION_CMD to the port,
        and checks if three $$$ are found in the response from
        the port.
        @return True if port was found.
        """
        self.message_string = 'Checking: {}'.format(port_name)
        try:
            port = serial.Serial(port=port_name, baudrate=self.baudrate, timeout=5)
            if (port.is_open):
                port.write(CONNECTION_CMD.encode('utf-8'))
                time.sleep(2)
                received_string = ''
                while (port.in_waiting > 0):
                    received_string += port.read().decode('utf-8', errors='replace')
                if ('$$$' in received_string):
                    self.message_string = 'Device found on port: {}'.format(port_name)
                    port.close()
                    self.connected = 1
                    time.sleep(1)
                    return True
        except serial.SerialException:
            return False
        except ValueError:
            return False
        return False

    def connect(self):
        """
        @brief Connect to the port.
        """
        self.port = serial.Serial(port=self.port_name, baudrate=self.baudrate, timeout=self.timeout)
        if (self.port.isOpen()):
            self.message_string = f'Device connected at {self.port_name}'
            self.connected = 2
            return 0

    def on_connected(self, instance, value):
        """
        @brief Callback for change in connected property.
        """
        if (value == 0):
            self.is_streaming = False
            self.message_string = 'Device disconnected'

    def start_streaming(self):
        """
        @brief Start streaming data from serial port.
        """
        if (not self.is_connected()):
            self.message_string = 'Board is not connected.'
            return

        if (not (self.is_streaming)):
            self.message_string = 'Started streaming'
            self.port.reset_input_buffer()
            self.port.write(START_STREAMING_CMD.encode('utf-8'))
            self.is_streaming = True
            self.read_state = 0
            self.skipped_bytes = 0
            read_thread = threading.Thread(target=self.collect_data)
            read_thread.daemon = True
            read_thread.start()
            self.samples_counter = 0

    def collect_data(self):
        """
        @brief Collect data from serial port while streaming is active.
        """
        while(self.is_streaming):
            self.skipped_bytes = 0
            self.read_serial_binary()

    def read_serial_binary(self, max_bytes_to_skip=3000):
        '''
        @brief Serial data parser.

        Parses incoming data packet into a Sample
        Incoming packet structure:
        START_BYTE(1)| DATA_MSB(1) | DATA_LSB(1) | END_BYTE (1)
        '''
        b = 0
        while self.is_streaming:
            while b != START_BYTE:
                # Check packet header
                self.skipped_bytes += 1
                b = self.port.read(1)
                if len(b) > 0:
                    b = struct.unpack('B', b)[0]

            self.skipped_bytes = 0
            # Get three bytes
            data = self.port.read(3)
            data = struct.unpack('3B', data)
            # Compute sensor data from 2 bytes and convert to V
            sensor_data = (((data[0] << 8) & 0xFFFF) | data[1])
            sensor_data = sensor_data/65535*5
            if data[2] == END_BYTE:
                # valid sample
                self.samples_counter += 1
                for callback in self.callbacks:
                    callback(sensor_data)
                b = self.port.read(1)
                if (len(b) > 0):
                    b = struct.unpack('B', b)[0]
            else:
                print("Invalid data.")

    def stop_streaming(self):
        """
        @brief Stop streaming from the serial port.
        """
        self.message_string = 'Stopped streaming data'
        self.is_streaming = False
        self.port.write(STOP_STREAMING_CMD.encode('utf-8'))

    def select_wave(self, wave):
        """
        @brief Select wave among SINE/TRIANGLE.

        """
        if (wave.upper() == 'SINE'):
            self.port.write(WAVE_SINE_CMD.encode('utf-8'))
        elif (wave.upper() == 'TRIANGLE'):
            self.port.write(WAVE_TRIANGLE_CMD.encode('utf-8'))

    def select_range(self, range_val):
        """
        @brief Select range among SMALL LARGE
        """
        if (range_val.upper() == 'SMALL'):
            self.port.write(RANGE_SMALL_CMD.encode('utf-8'))
        elif (range_val.upper() == 'LARGE'):
            self.port.write(RANGE_LARGE_CMD.encode('utf-8'))

    def is_connected(self):
        """
        @brief Check if serial port is connected.
        """
        if (self.connected == 2):
            return True
        else:
            return False
