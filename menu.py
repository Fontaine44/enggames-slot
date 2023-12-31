from settings import *
from state import State
import pygame
import cv2
import json

class Menu(State):
    def __init__(self, state_machine, sound, buttons):
        super().__init__()
        self.state_machine = state_machine
        self.sound = sound
        self.buttons = buttons
        self.font = pygame.freetype.Font(FONT_PATH, 150)
        self.started = True
        self.state = 0
        self.webcam_rect = ((WIDTH-WEBCAM_WIDTH)//2, (HEIGHT-WEBCAM_HEIGHT)//2+50, WEBCAM_WIDTH, WEBCAM_HEIGHT)
        self.cap = None
        self.detector = cv2.QRCodeDetector()

        self.cashin_time = 0
        self.amount_pos = None
        self.amount_surface = None

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()

        # Load images
        self.menu_screen = pygame.image.load(MENU_IMAGE_PATH).convert_alpha()
        self.scan_screen = pygame.image.load(SCAN_IMAGE_PATH).convert_alpha()
    
    def pre_start(self):
        self.started = False
        self.state = 0

    def start(self):
        self.buttons.clear_buffer()
        self.started = True

    def check_menu(self):
        self.buttons.refresh_input()

        if self.buttons.green_pressed:
            self.state_machine.next()
        elif self.buttons.red_pressed:
            self.state = 1
            self.start_cap()
    
    def check_scan(self):
        self.buttons.refresh_input()

        if self.buttons.red_pressed:
            self.state = 0
            try:
                self.cap.release()
                self.cap = None
            except:
                pass
            
    def menu(self):
        if self.started:
            self.check_menu()
        self.display_surface.blit(self.menu_screen, (0, 0))
    
    def scan(self):
        self.check_scan()
        self.display_surface.blit(self.scan_screen, (0, 0))

        # Capture and blit frame
        if self.cap:

            # Capture a frame from the camera
            ret, original_frame = self.cap.read()
            
            # Check for succesful capture
            if ret:
                # Convert the OpenCV frame to Pygame surface
                frame = cv2.resize(original_frame, (WEBCAM_WIDTH, WEBCAM_HEIGHT))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.transpose(frame)
                frame_surface = pygame.surfarray.make_surface(frame)
                # Blit the frame onto the Pygame screen
                self.display_surface.blit(frame_surface, self.webcam_rect)

                data, one, _ = self.detector.detectAndDecode(frame)
                if data:
                    print(data)
                    result = self.set_amount_surface(data)
                    if result:
                        self.state = 2
                        self.cap.release()
                        self.cap = None
                    
            else:
                print("Failed to capture webcam")
    
    def start_cap(self):
        self.buttons.clear_buffer()

        # Start camera object
        try:
            self.cap = cv2.VideoCapture(WEBCAM_PORT, cv2.CAP_DSHOW)
            # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH)
            # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT)
            ret, frame = self.cap.read()
        except:
            self.cap = None
            self.state_machine.next()
            print("Failed to init webcam object")
    
    def set_amount_surface(self, id):

        with open(DATA_PATH, 'r') as file:
            data = json.load(file)

        for ply in data :
            if id == ply["id"] and ply["redeemed"] == False:
                ply["redeemed"] = True
                amount = ply["balance"]

                with open(DATA_PATH, 'w') as file:
                    json.dump(data, file, indent=2)  # 'indent' parameter for pretty formatting, adjust as needed

                amount_str = str(int(amount)) + ' $'
                # Render text to a surface
                self.amount_surface, _ = self.font.render(amount_str, WHITE)
                # Get the size of the rendered text
                amount_width, amount_height = self.amount_surface.get_size()
                # Determine position
                self.amount_pos = ((WIDTH-amount_width)//2, (HEIGHT-amount_height)//2)

                return True
            
        return False

    def cashin(self, delta_time):
        self.cashin_time += delta_time
        self.display_surface.blit(self.scan_screen, (0, 0))
        self.display_surface.blit(self.amount_surface, self.amount_pos)

        # Show cashin amount for 3 seconds
        if self.cashin_time > 3:
            self.cashin_time = 0
            self.state_machine.next()
            

    def update(self, delta_time):
        if self.state == 0:
            self.menu()
        elif self.state == 1:
            self.scan()
        else:
            self.cashin(delta_time)
        
        return self.display_surface, [self.display_rect]
    

# Leader board scrolling

# Bottom with instructions for red/green buttons