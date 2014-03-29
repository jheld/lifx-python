# network management
GET_PAN_GATEWAY = 0x02
PAN_GATEWAY = 0x03
# brightness & colors
GET_LIGHT_STATE = 0x65
SET_LIGHT_COLOR = 0x66
SET_WAVEFORM = 0x67
SET_DIM_ABSOLUTE = 0x68
SET_DIM_RELATIVE = 0x69
LIGHT_STATUS = 0x6b
# labels & tags
GET_BULB_LABEL = 0x17 # app to bulb
SET_BULB_LABEL = 0x18 # app to bulb
BULB_LABEL = 0x19 # bulb to app
GET_TAGS = 0x1a # app to bulb
SET_TAGS = 0x1b # app to bulb
TAGS = 0x1c # bulb to app
GET_TAG_LABELS = 0x1d # app to bulb
SET_TAG_LABELS = 0x1e # app to bulb
TAG_LABELS = 0x1f # bulb to app
# power management
GET_POWER_STATE = 0x14
SET_POWER_STATE = 0x15
POWER_STATE = 0x16
# diagnostic
REBOOT = 0x26 # app to bulb
