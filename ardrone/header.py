#DEBUG = False
DEBUG = True

#ARDRONE_IP = '192.168.1.1'
ARDRONE_IP = '127.0.0.1'
ARDRONE_NAVDATA_PORT = 5554
ARDRONE_VIDEO_PORT = 5555
ARDRONE_COMMAND_PORT = 5556

COMWDG_INTERVAL = 1
COMWDG_CMD = ("COMWDG", )

DRONE_STATES = (
    'fly_mask',            # FLY MASK : (0) ardrone is landed, (1) ardrone is flying
    'video_mask',          # VIDEO MASK : (0) video disable, (1) video enable
    'vision_mask',         # VISION MASK : (0) vision disable, (1) vision enable */
    'control_mask',        # CONTROL ALGO (0) euler angles control, (1) angular speed control */
    'altitude_mask',       # ALTITUDE CONTROL ALGO : (0) altitude control inactive (1) altitude control active */
    'user_feedback_start', # USER feedback : Start button state */
    'command_mask',        # Control command ACK : (0) None, (1) one received */
    'fw_file_mask',        # Firmware file is good (1) */
    'fw_ver_mask',         # Firmware update is newer (1) */
    'fw_upd_mask',         # Firmware update is ongoing (1) */
    'navdata_demo_mask',   # Navdata demo : (0) All navdata, (1) only navdata demo */
    'navdata_bootstrap',   # Navdata bootstrap : (0) options sent in all or demo mode, (1) no navdata options sent */
    'motors_mask',         # Motor status : (0) Ok, (1) Motors problem */
    'com_lost_mask',       # Communication lost : (1) com problem, (0) Com is ok */
    'vbat_low',            # VBat low : (1) too low, (0) Ok */
    'user_el',             # User Emergency Landing : (1) User EL is ON, (0) User EL is OFF*/
    'timer_elapsed',       # Timer elapsed : (1) elapsed, (0) not elapsed */
    'angles_out_of_range', # Angles : (0) Ok, (1) out of range */
    'ultrasound_mask',     # Ultrasonic sensor : (0) Ok, (1) deaf */
    'cutout_mask',         # Cutout system detection : (0) Not detected, (1) detected */
    'pic_version_mask',    # PIC Version number OK : (0) a bad version number, (1) version number is OK */
    'atcodec_thread_on',   # ATCodec thread ON : (0) thread OFF (1) thread ON */
    'navdata_thread_on',   # Navdata thread ON : (0) thread OFF (1) thread ON */
    'video_thread_on',     # Video thread ON : (0) thread OFF (1) thread ON */
    'acq_thread_on',       # Acquisition thread ON : (0) thread OFF (1) thread ON */
    'ctrl_watchdog_mask',  # CTRL watchdog : (1) delay in control execution (> 5ms), (0) control is well scheduled */
    'adc_watchdog_mask',   # ADC Watchdog : (1) delay in uart2 dsr (> 5ms), (0) uart2 is good */
    'com_watchdog_mask',   # Communication Watchdog : (1) com problem, (0) Com is ok */
    'emergency_mask',      # Emergency landing : (0) no emergency, (1) emergency */
)

SHORTHAND_COMMAND = {
    'l': 'move_left',
    'r': 'move_right',
    'f': 'move_forward',
    'b': 'move_backward',
    'u': 'move_up',
    'd': 'move_down',
    'p': 'turn_left',
    'n': 'turn_right',

    'y': 'land',
    't': 'takeoff',
    'h': 'hover',
    'z': 'reset',
    
    's': 'sleep',
}
