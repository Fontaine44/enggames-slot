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

# 5 Symbols for demo
# symbols = {
#     'diamond': f"{SYM_PATH}/0_diamond.png", 
#     'floppy': f"{SYM_PATH}/0_floppy.png",
#     'hourglass': f"{SYM_PATH}/0_hourglass.png",
#     'seven': f"{SYM_PATH}/0_seven.png",
#     'telephone': f"{SYM_PATH}/0_telephone.png"
# }

# 4 Symbols for more wins
symbols = {
    'diamond': f"{SYM_PATH}/0_diamond.png", 
    'chug': f"{SYM_PATH}/0_chug.png",
    'wah': f"{SYM_PATH}/0_wah.png",
    'jdg': f"{SYM_PATH}/0_jdg.png",
    'mgcil': f"{SYM_PATH}/0_mgcil.png"
}