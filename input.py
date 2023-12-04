import serial

class ArcadeButton():
    def __init__(self):
        # Define the serial port and baud rate
        self.serial_port = 'COM8'
        self.baud_rate = 19200
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate)
        except:
            print("Cannot find Arduino")
            self.ser = None
    
    def clear_buffer(self):
        if self.ser is not None:
            self.ser.reset_input_buffer()
    
    def read_line_or_none(self):
        if self.ser.in_waiting > 0:
            return self.ser.readline().decode('utf-8').strip()
        else:
            return None
        
    def get_input(self):
        if self.ser is not None:
            line = self.read_line_or_none()

            if line == '0':
                return 0
            elif line == '1':
                print("cashing_out")
                return 1
            else:
                return None

# can_spin = False
# i = 0
# button = ArcadeButton()
# while True:
#     if can_spin:
#         if button.get_input() == 0:
#             print("spinning")
#             i = 0
#             can_spin = False
#     i+=1
#     if i > 10000000:
#         can_spin = True
#         print("spin allowed")
# try:
#     button = ArcadeButton()
#     button.get_input()
# except KeyboardInterrupt:
#     button.ser.close()


