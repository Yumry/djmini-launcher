import socket
from serial import Serial
import time
import threading
import traceback
import bmlauncher.config as config

class LightsForwarder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server_address = "localhost"
        self.server_port = 8000
        self.connected = False
        self.serial_port = config.get_config()['djmini_serial_port']
        # Debugging mode, disable serial connection for use outside of a real cabinet.
        self.pass_serial = False
        self.rom_name = 'unknown'
        self.light_state_array = bytearray()
        # map for which lights go to which output bit.
        self.light_bit_bindings = {
            '1P-keyboard-1': 0,
            '1P-keyboard-2': 1,
            '1P-keyboard-3': 2,
            '1P-keyboard-4': 3,
            '1P-keyboard-5': 4,
            '2P-keyboard-1': 5,
            '2P-keyboard-2': 6,
            '2P-keyboard-3': 7,

            '2P-keyboard-4': 8,
            '2P-keyboard-5': 9,    
            'led0': 10, # P1 start
            'led1': 11, # P2 start
            'led2': 12, # Effector
            'right-ssr': 13,
            'left-blue-hlt': 14,
            'left-red-hlt': 15,
            
            'right-blue-hlt': 16,
            'right-red-hlt': 17,
            'pause': 18,
            'mame_stop': 19,
            'mame_start': 20,
            'left-ssr': 21,
        }

    def set_light_status(self, light_name, light_status):
        try:
            light_bit = self.light_bit_bindings[light_name]
            # Find which byte we need to change
            byte_num = -1 * ( -(light_bit + 1) // 8 ) -1
            if self.pass_serial: print(light_name, ': changing light bit', light_bit - (byte_num * 8), 'from byte', byte_num, 'to value', light_status)
            if light_status == 1:
                new_byte = self.light_state_array[byte_num] | (1 << light_bit - (byte_num * 8))
            if light_status == 0:
                new_byte = self.light_state_array[byte_num] & ~(1 << light_bit - (byte_num * 8))

            self.light_state_array[byte_num] = new_byte
        except KeyError:
            print("Unknown light: ", light_name)
            pass

    def run(self):
        # Perform a ceiling division operation on the number of light bindings, then allocate the needed number of bytes for them.
        for i in range(0, -1 * ( -len(self.light_bit_bindings) // 8 )):
            self.light_state_array.append(0x00)

        device = None
        if not self.pass_serial:
            device = Serial(self.serial_port, 9600, timeout=10)
            print("Connected to serial device")

        # Connect to our IO device via serial 9600 baud rate.
        while True:
            clear_lights = False
            try:
                mameLine = ''
                while(self.connected == False):
                    try:
                        light_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        light_server.connect((self.server_address, self.server_port))
                        print('Connected to MAME lights server. Beginning lights forwarding...')
                        self.connected = True
                        clear_lights = True
                    except:
                        pass

                while self.connected:
                    mame_data = light_server.recv(1)
                    if(mame_data == b'\r'):
                        mame_light_name = mameLine.split(' = ')[0]
                        mame_light_status = mameLine.split(' = ')[1]
                        
                        # Set the game name since that is the first thing MAME will send.
                        if(mame_light_name == 'mame_start'):
                            self.set_light_status('mame_start', 1)
                            self.rom_name = mame_light_status

                        try:
                            if int(mame_light_status) == 0 or int(mame_light_status) == 1:
                                # Update the lighting bits
                                self.set_light_status(mame_light_name, int(mame_light_status))
                                start_marker = bytearray()
                                start_marker.append(0xDD)
                                start_marker.append(0xDD)
                                
                                if not self.pass_serial:
                                    device.write(start_marker)
                                    device.write(self.light_state_array)

                        except ValueError:
                            pass

                        mameLine = ''
                    else:
                        mameLine += mame_data[0:1].decode("utf-8")\

                if clear_lights:
                    # MAME has closed and the lights need to be turned off
                    print('Diconnected. Clearing lights')
                    for light in self.light_bit_bindings:
                        self.set_light_status(light, 0)
                    if not self.pass_serial:
                        device.write(start_marker)
                        device.write(self.light_state_array)
                    clear_lights = False

            except Exception:
                traceback.print_exc()
                time.sleep(1)
                pass