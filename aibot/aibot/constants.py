# navigation constants

DIST_FOLLOW_LINE_MIN      = 500 # ticks
DIST_FOLLOW_GYRO          = 80  # ticks
DIST_PUSH_CAN             = 500 # ticks
DIST_PUSH_CAN_REV         = 200 # ticks

SPEED_TURN                =  5 # percent
SPEED_FWD                 = 30 # percent

# hw constants

ADDR_GS                   = "ev3-ports:in1"
ADDR_CS_L                 = "ev3-ports:in2"
ADDR_CS_R                 = "ev3-ports:in3"

ADDR_MOT_R                = "ev3-ports:outA"
ADDR_MOT_L                = "ev3-ports:outB"

# follow_line_for()
FOLLOW_LINE_DUAL_P        = 3.2
FOLLOW_LINE_DUAL_I        = 0.01
FOLLOW_LINE_DUAL_D        = 2.0
FOLLOW_LINE_DUAL_TH_BLACK = 45

# follow_gyro_for()
FOLLOW_GYRO_P             = 3.0
FOLLOW_GYRO_I             = 0.01
FOLLOW_GYRO_D             = 2.0