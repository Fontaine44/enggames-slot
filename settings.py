# Display settings
DEFAULT_IMAGE_SIZE = (300, 300)
FPS = 120
HEIGHT = 1000
WIDTH = 1600
START_X, START_Y = 0, -300
X_OFFSET, Y_OFFSET = 20, 0

# Images
BG_IMAGE_PATH = 'graphics/0/bg_black.png'
GRID_IMAGE_PATH = 'graphics/0/gridline.png'
GAME_INDICES = [1, 2, 3] # 0 and 4 are outside of play area
SYM_PATH = 'graphics/0/symbols'

# Text
TEXT_COLOR = 'White'
UI_FONT = 'graphics/font/Casino3D.ttf'
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110

# Symbols dictionnary
symbols = {
    'diamond': f"{SYM_PATH}/0_diamond.png", 
    'chug': f"{SYM_PATH}/0_chug.png",
    'wah': f"{SYM_PATH}/0_wah.png",
    'jdg': f"{SYM_PATH}/0_jdg.png",
    'mgcil': f"{SYM_PATH}/0_mgcil.png",
}

symbols_weight = {
    'diamond': 20, 
    'chug': 2,
    'wah': 10,
    'jdg': 10,
    'mgcil': 10,
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