# Display settings
# SYMBOL_SIZE = 268
# FPS = 90
# HEIGHT = 900
# WIDTH = 1600
# REEL_SPEED =  67   # number of pixels down per frame, must be a divider of the image size
SYMBOL_SIZE = 300
FPS = 60
HEIGHT = 1080
WIDTH = 1920
REEL_SPEED = 100    # number of pixels down per frame, must be a divider of the image size
DELAY_TIME = 200
SPIN_TIME = 1000
# topleft_x, topleft_y, width, height
REELS_ZONE = [0, 0, SYMBOL_SIZE*5, SYMBOL_SIZE*3]
BOTTOM_UI_ZONE = [0, REELS_ZONE[3], SYMBOL_SIZE*5, HEIGHT-REELS_ZONE[3]]
SIDE_UI_ZONE =  [REELS_ZONE[2], 0, WIDTH-REELS_ZONE[2], HEIGHT]

# Images
BG_IMAGE_PATH = 'graphics/assets/bg_black.png'
GRID_IMAGE_PATH = 'graphics/assets/gridline.png'
SYM_PATH = 'graphics/symbols'
NUM_PATH = 'graphics/numbers'

# Text
TEXT_COLOR = 'White'
UI_FONT = 'graphics/font/Casino3D.ttf'
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110

# Colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
    '1': 2,
    '2': 3,
    '3': 3,
    '4': 3,
    '5': 3,
    '6': 2,
    '7': 2,
    '8': 1,
    '9': 1,
}

# Symbols dictionnary
SYMBOLS_PATH = {
    'diamond': f"{SYM_PATH}/diamond.png", 
    'sip': f"{SYM_PATH}/sip.png",
    'wah': f"{SYM_PATH}/wah.png",
    'jdg': f"{SYM_PATH}/jdg.png",
    'mgcil': f"{SYM_PATH}/mgcil.png",
    'bonus': f"{SYM_PATH}/bonus.png",
}

SYMBOLS_WEIGHT = {
    'diamond': 0, 
    'sip': 7,
    'wah': 10,
    'jdg': 8,
    'mgcil': 10,
    'bonus': 1
}

SYMBOLS_PAY = {
    'diamond': 1, 
    'sip': 0,
    'wah': 2,
    'jdg': 2,
    'mgcil': 2,
    'bonus': 0
}

# Paylines (index=reel, value=row)
PAYLINES = [
    [0, 0, 0, 0, 0],   # Top Row
    [1, 1, 1, 1, 1],   # Middle Row
    [2, 2, 2, 2, 2],   # Bottom Row
    [0, 1, 2, 1, 0],   # V
    [2, 1, 0, 1, 2],   # Reverse V
    [0, 0, 1, 2, 2],   # Cross top-left to bottom-right
    [2, 2, 1, 0, 0],   # Cross bottom-left to top-right
    [0, 1, 0, 1, 0],   # Top zig-zag
    [1, 0, 1, 0, 1],   # Middle zig-zag 1
    [1, 2, 1, 2, 1],   # Middle zig-zag 2
    [2, 1, 2, 1, 2]    # Bottom zig-zag
]

# Wheel
WHEEL_PATH = 'graphics/wheel/wheel.png'
WHEEL_SIZE = 800
ARROW_PATH = 'graphics/wheel/arrow.svg'
ARROW_SIZE = 400