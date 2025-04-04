from pygame.locals import USEREVENT
import math

PADDLE_FIRE_EVENT = USEREVENT + 1
REACHED_BORDER_EVENT = USEREVENT + 2
CURSOR_BLINK_EVENT = USEREVENT + 3

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

PADDLE_OFFSET = 25
PADDLE_WIDTH = 7
PADDLE_HEIGHT = SCREEN_HEIGHT // 4

BALL_OFFSET = PADDLE_OFFSET + 13
BALL_RADIUS = 8
BALL_PIXELS = 2
BALL_VELOCITY = 7
BALL_ANGLE = math.radians(60)
BALL_ACCELERATION = 0.4
MIN_ANGLE_FACTOR = 0.5

SCORE_FONT_SIZE = 40
SCORE_OFFSETS = [200, 100]

SFX_VOLUME = 0.4

LINE_WIDTH = 6
LINE_HEIGHT = 40
LINE_GAP = 20
LINE_OFFSET = 10

BUTTON_FONT_SIZE = 25
BUTTON_FILL = "black"
BUTTON_ACCENT_ACTIVE = "grey"
BUTTON_ACCENT_INACTIVE = "white"

TEXT_FIELD_FONT_SIZE = 20
TEXT_FIELD_FILL = "black"
TEXT_FIELD_ACCENT = "white"

CURSOR_BLINK_DELAY = 200
CURSOR_WIDTH = 5
CURSOR_X_OFFSET = 2
CURSOR_Y_OFFSET = 10

MAIN_MENU_OFFSET = 80
TITLE_FONT_SIZE = 30
MAIN_MENU_BUTTON_WIDTH = 500
MAIN_MENU_BUTTON_HEIGHT = 70
MAIN_MENU_BUTTON_BORDER = 10