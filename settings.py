# Display settings
DEFAULT_IMAGE_SIZE = (300, 300)
FPS = 60
HEIGHT = 1000
WIDTH = 1600
START_X, START_Y = 0, -300
X_OFFSET, Y_OFFSET = 20, 0

# Images
BG_IMAGE_PATH = 'graphics/assets/bg_black.png'
GRID_IMAGE_PATH = 'graphics/assets/gridline.png'
GAME_INDICES = [1, 2, 3] # 0 and 4 are outside of play area
SYM_PATH = 'graphics/symbols'

# Text
TEXT_COLOR = 'White'
UI_FONT = 'graphics/font/Casino3D.ttf'
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110

# Symbols dictionnary
SYMBOLS_PATH = {
    'diamond': f"{SYM_PATH}/diamond.png", 
    'sip': f"{SYM_PATH}/sip.png",
    'wah': f"{SYM_PATH}/wah.png",
    'jdg': f"{SYM_PATH}/jdg.png",
    'mgcil': f"{SYM_PATH}/mgcil.png",
    'bonus': f"{SYM_PATH}/bonus.png"
}

SYMBOLS_WEIGHT = {
    'diamond': 0, 
    'sip': 5,
    'wah': 10,
    'jdg': 2,
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