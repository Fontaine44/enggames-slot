import serial
import pygame

class Buttons():
    def __init__(self):
        # Define the serial port and baud rate
        self.serial_port = 'COM8'
        self.baud_rate = 19200

        self.red_pressed = False
        self.green_pressed = False

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
        
    def get_serial_input(self):
        if self.ser is not None:
            line = self.read_line_or_none()

            if line == '0':
                return 0    # Green pressed
            elif line == '1':
                print("cashing_out")
                return 1    # Red pressed
            else:
                return None # Nothing pressed
        
    def refresh_input(self):
        button_input = self.get_serial_input()

        self.red_pressed = True if button_input == 1 else False
        self.green_pressed = True if button_input == 0 else False

        # For debug purposed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.red_pressed = True
        elif  keys[pygame.K_SPACE]:
            self.green_pressed = True