import threading
import array
import struct
from fcntl import ioctl

class Controller(threading.Thread):
    def __init__(self, js_path):
        threading.Thread.__init__(self)
        self.js_path = js_path
        self.running = False
        self.js_device = open(js_path, 'rb')
        self.button_states = {}
        self.callback_btn_pressed = []
        self.callback_btn_released = []

        buf = array.array('B', [0] * 64)
        ioctl(self.js_device, 0x80006a13 + (0x10000 * len(buf)), buf)

        self.js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
        print('Opening native joystick', self.js_name)

        buf = array.array('B', [0])
        ioctl(self.js_device, 0x80016a12, buf)
        self.num_buttons = buf[0]

        for i in range(self.num_buttons):
            btn_name = 'btn_' + str(i)
            self.button_states[btn_name] = 0

    def run(self):
        self.running = True
        try:
            while self.running:
                evbuf = self.js_device.read(8)
                if evbuf:
                    time, value, type, number = struct.unpack('IhBB', evbuf)
                    if type & 0x01:
                        btn_name = 'btn_' + str(number)
                        self.button_states[btn_name] = value
                        if value == 1:
                            for callback in self.callback_btn_pressed:
                                callback(btn_name)
                        else:
                            for callback in self.callback_btn_released:
                                callback(btn_name)
        except:
            self.running = False

    def stop(self):
        self.running = False
    
    def add_press_handler(self, callback_function):
        self.callback_btn_pressed.append(callback_function)
    
    def add_release_handler(self, callback_function):
        self.callback_btn_released.append(callback_function)

    def remove_handlers(self):
        self.callback_btn_pressed = []