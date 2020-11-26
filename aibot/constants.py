# navigation constants

DIST_FOLLOW_LINE_MIN      = 300 # ticks
DIST_BETWEEN_INTERSECTION = 500 # ticks
DIST_INTERSECTION_OFFSET  = 80  # ticks
DIST_PUSH_CAN             = 430 # ticks

INTERSECTIONS_FOR_BOOST   = 2
SLEW_RATE                 = None # slope (0 to disable)
SPEED_TURN                = 20 # percent
SPEED_FWD                 = 40 # percent
SPEED_FWD_FAST            = 40 # percent
SPEED_REV                 = 40 # percent
SPEED_OFFSET              = 40 # percent
SPEED_PUSH                = 30 # percent
SPEED_MAX_NATIVE          = 1050 # native units

# hw constants

ADDR_GS                   = "ev3-ports:in1"
ADDR_CS_L                 = "ev3-ports:in3"
ADDR_CS_R                 = "ev3-ports:in2"
ADDR_LS_F                 = "ev3-ports:in4"

ADDR_MOT_L                = "ev3-ports:outA"
ADDR_MOT_R                = "ev3-ports:outD"

# threshold species value before it is categorized as BLACK
# white 100 <---> 0 black
CS_TH_BLACK               = 45
LS_TH_BLACK               = 57

# line follower PID (dual)
SLEEP_TIME                = None # dt
LP_CUTOFF_FREQ            = 10 # Hz
FOLLOW_LINE_DUAL_P        = 4.2
FOLLOW_LINE_DUAL_I        = 0.01
FOLLOW_LINE_DUAL_D        = 7.0

# gyro follower PID
FOLLOW_GYRO_P             = 3.0
FOLLOW_GYRO_I             = 0.01
FOLLOW_GYRO_D             = 2.0