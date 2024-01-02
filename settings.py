# Display settings
SYMBOL_SIZE = 300
FPS = 60
HEIGHT = 1080
WIDTH = 1920
REEL_SPEED = 100    # number of pixels down per frame, must be a divider of the image size
DELAY_TIME = 200
SPIN_TIME = 1000

X_OFFSET = 20
# topleft_x, topleft_y, width, height
REELS_ZONE = [0, 0, SYMBOL_SIZE*5+X_OFFSET*5, SYMBOL_SIZE*3] # [0, 0, 1600, 900]
BOTTOM_UI_ZONE = [0, REELS_ZONE[3], REELS_ZONE[2], HEIGHT-REELS_ZONE[3]] # [0, 900, 1600, 180]
SIDE_UI_ZONE =  [REELS_ZONE[2], 0, WIDTH-REELS_ZONE[2], HEIGHT] # [1600, 0, 320, 1080]

# Images
MENU_IMAGE_PATH = 'graphics/assets/menu_screen.png'
SCAN_IMAGE_PATH = 'graphics/assets/scan_screen.png'
GRID_IMAGE_PATH = 'graphics/assets/slot_grid.png'
BOTTOM_UI_IMAGE_PATH = 'graphics/assets/bottom_ui_screen.png'
SIDE_UI_IMAGE_PATH = 'graphics/assets/side_ui_screen.png'
CASHOUT_IMAGE_PATH = 'graphics/assets/cashout_screen.png'
BANKRUPT_IMAGE_PATH = 'graphics/assets/bankrupt_screen.png'
PRINTING_IMAGE_PATH = 'graphics/assets/printing_screen.png'
PHOTO_IMAGE_PATH = 'graphics/assets/photo_screen.png'
COUNTDOWN_1_PATH = 'graphics/assets/countdown_1.png'
COUNTDOWN_2_PATH = 'graphics/assets/countdown_2.png'
COUNTDOWN_3_PATH = 'graphics/assets/countdown_3.png'
BLUR_IMAGE_PATH = 'graphics/assets/blur_screen.png'
CASHOUT_CONFIRM_PATH = 'graphics/assets/cashout_confirm.png'
SIP_CONFIRM_PATH = 'graphics/assets/sips_confirm.png'
VIDEO_0_PATH = 'graphics/assets/video_0.png'
VIDEO_1_PATH = 'graphics/assets/video_1.png'
VIDEO_2_PATH = 'graphics/assets/video_2.png'
VIDEO_3_PATH = 'graphics/assets/video_3.png'

FONT_PATH = 'graphics/font/CasinoFlat_COMBIEN.ttf'
SYM_PATH = 'graphics/symbols'
NUM_PATH = 'graphics/numbers'
WHEEL_PATH = 'graphics/wheel'
LINE_PATH = 'graphics/lines'

# Printer & Webcam & Arduino
ARDUINO_PORT = 'COM8'
WEBCAM_PORT = 1
PRINTER_PORT = 'COM7'
WEBCAM_HEIGHT = 600
WEBCAM_WIDTH = 800
MGCIL_LOGO_PATH = 'graphics/assets/mgcil_logo.png'
DATA_PATH = 'data.json'

# Colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 50, 255)
PINK = (255, 0, 216)
YELLOW = (255, 255, 0)
GREY = (169, 169, 169)

NUMBERS_PATH = {
    '1': f"{NUM_PATH}/1.png",
    '2': f"{NUM_PATH}/2.png",
    '3': f"{NUM_PATH}/3.png",
    '4': f"{NUM_PATH}/4.png",
    '5': f"{NUM_PATH}/5.png",
    '6': f"{NUM_PATH}/6.png",
    '7': f"{NUM_PATH}/7.png",
    '8': f"{NUM_PATH}/8.png",
    '9': f"{NUM_PATH}/9.png",
}

NUMBERS_WEIGHT = {
    '1': 1,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 4,
    '7': 4,
    '8': 3,
    '9': 2,
}

# Symbols dictionnary
SYMBOLS_PATH = {
    'sip': f"{SYM_PATH}/sip.png",
    'wah': f"{SYM_PATH}/wah.png",
    'jdg': f"{SYM_PATH}/jdg.png",
    'mgcil': f"{SYM_PATH}/mgcil.png",
    'bonus': f"{SYM_PATH}/bonus.png",
    'rat': f"{SYM_PATH}/rat.png"
}

SYMBOLS_WEIGHT = { 
    'sip': 3,
    'bonus': 3,
    'wah': 10,
    'jdg': 8,
    'mgcil': 10,
    'rat': 10,
}

SYMBOLS_PAY = {
    'sip': 0,
    'bonus': 0,
    'wah': 1,
    'jdg': 1,
    'mgcil': 1,
    'rat': 1,
}

# Paylines (index=reel, value=row)
PAYLINES = [
    [0, 0, 0, 0, 0],   # 0: Top Row
    [1, 1, 1, 1, 1],   # 1: Middle Row
    [2, 2, 2, 2, 2],   # 2: Bottom Row
    [0, 1, 2, 1, 0],   # 3: V
    [2, 1, 0, 1, 2],   # 4: Reverse V
    [0, 0, 1, 2, 2],   # 5: Cross top-left to bottom-right
    [2, 2, 1, 0, 0],   # 6: Cross bottom-left to top-right
    [0, 1, 0, 1, 0],   # 7: Top zig-zag
    [1, 0, 1, 0, 1],   # 8: Middle zig-zag 1
    [1, 2, 1, 2, 1],   # 9: Middle zig-zag 2
    [2, 1, 2, 1, 2],   # 10: Bottom zig-zag
    [1, 0, 0, 0, 1],   # 11: Bump Up
    [1, 2, 2, 2, 1],   # 12: Bump Down
]

LINES_PATH = [
    f'{LINE_PATH}/line0.png',
    f'{LINE_PATH}/line1.png',
    f'{LINE_PATH}/line2.png',
    f'{LINE_PATH}/line3.png',
    f'{LINE_PATH}/line4.png',
    f'{LINE_PATH}/line5.png',
    f'{LINE_PATH}/line6.png',
    f'{LINE_PATH}/line7.png',
    f'{LINE_PATH}/line8.png',
    f'{LINE_PATH}/line9.png',
    f'{LINE_PATH}/line10.png',
    f'{LINE_PATH}/line11.png',
    f'{LINE_PATH}/line12.png',
]

# Wheel
WHEEL = f'{WHEEL_PATH}/wheel.png'
ARROW = f'{WHEEL_PATH}/arrow.svg'
ARROW_SIZE = 400
WHEEL_RANGES = [(-22.5, 22.5), (22.5, 68), (68, 113.5), (113.5, 159), (159, 204.5), (204.5, 250), (250, 295.5), (295.5, 341)]
WHEEL_WEIGHTS = [1, 2, 2, 2, 0.5, 2, 2, 2]