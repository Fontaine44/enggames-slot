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

X_OFFSET = 20
# topleft_x, topleft_y, width, height
REELS_ZONE = [0, 0, SYMBOL_SIZE*5+X_OFFSET*5, SYMBOL_SIZE*3]
BOTTOM_UI_ZONE = [0, REELS_ZONE[3], REELS_ZONE[2], HEIGHT-REELS_ZONE[3]]
SIDE_UI_ZONE =  [REELS_ZONE[2], 0, WIDTH-REELS_ZONE[2], HEIGHT]

# Images
BG_IMAGE_PATH = 'graphics/assets/neon_brick.jpg'
GRID_IMAGE_PATH = 'graphics/assets/slot_grid.png'
SYM_PATH = 'graphics/symbols'
NUM_PATH = 'graphics/numbers'
WHEEL_PATH = 'graphics/wheel'
LINE_PATH = 'graphics/lines'

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
    'sip': f"{SYM_PATH}/sip.png",
    'wah': f"{SYM_PATH}/wah.png",
    'jdg': f"{SYM_PATH}/jdg.png",
    'mgcil': f"{SYM_PATH}/mgcil.png",
    'bonus': f"{SYM_PATH}/bonus.png",
    'rat': f"{SYM_PATH}/rat.png"
}

SYMBOLS_WEIGHT = { 
    'sip': 2,
    'bonus': 4,
    'wah': 10,
    'jdg': 8,
    'mgcil': 10,
    'rat': 10,
}

SYMBOLS_PAY = {
    'sip': 0,
    'bonus': 0,
    'wah': 2,
    'jdg': 2,
    'mgcil': 2,
    'rat': 10,
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
WHEEL_SIZE = 900
ARROW = f'{WHEEL_PATH}/arrow.svg'
ARROW_SIZE = 400