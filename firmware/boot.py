print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

from kmk.modules.layers import Layers

from kmk.extensions.rgb import RGB 

from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.mouse_keys import MouseKeys

from kmk.extensions.peg_oled_display import Oled,OledDisplayMode,OledReactionType,OledData
from kmk.extensions.lock_status import LockStatus
from kmk.extensions.wpm import WPM

keyboard = KMKKeyboard()

keyboard.col_pins = (board.D8, board.D9, board.D10)
keyboard.row_pins = (board.D7, board.D3, board.D2)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

encoder_handler = EncoderHandler()

keyboard.modules.append(encoder_handler)
keyboard.modules.append(MediaKeys())
keyboard.modules.append(MouseKeys())

encoder_handler.pins = ((board.GP9,board.GP10,None),)


keyboard.modules.append(Layers())


# RGB

rgb = RGB(pixel_pin=board.D6, num_pixels=4 ,rgb_order=(1,0,2,3)) 
keyboard.extensions.append(rgb) 


# OLED display
keyboard.SCL=board.D5
keyboard.SDA=board.D4

oled_ext = Oled(
    OledData(
        corner_one={0:OledReactionType.STATIC,1:["layer"]},
        corner_two={0:OledReactionType.LAYER,1:["1","2"]},
        corner_three={0:OledReactionType.STATIC,1:[""]},
        corner_four={0:OledReactionType.STATIC,1:["NumLk"]},
        corner_five={0:OledReactionType.STATIC,1:["wpm"]},
        corner_six={0:OledReactionType.STATIC,1:["ScrlLk"]},
        ),
        toDisplay=OledDisplayMode.TXT,flip=True)


TRANS = KC.TRNS
# RAISE = KC.MO(1)
LY2 = KC.DF(2)
LY1 = KC.DF(1)
LY0 = KC.DF(0)
# RAISE = KC.LT(1)

keyboard.keymap = [
    [ # Layer 0
     LY1, KC.B, KC.C,
     KC.D, KC.E, KC.F,
     KC.G, KC.F, KC.I,
    ],
    [ # Layer 1
     LY2, KC.B, KC.LEFT,
     KC.UP, KC.E, KC.F,
     KC.DOWN, KC.RIGHT, KC.I,
    ],
    [ # Layer 2
     LY0, KC.RGB_MODE_PLAIN, KC.RGB_TOG,
     KC.RGB_MODE_BREATHE, KC.RGB_MODE_SWIRL, KC.RGB_SAD,
     KC.RGB_MODE_KNIGHT, KC.RGB_MODE_BREATHE_RAINBOW, KC.RGB_HUI,
    ],
]

encoder_handler.map = [
            ((KC.VOLD, KC.VOLU),),       
            ((KC.BRIGHTNESS_DOWN, KC.BRIGHTNESS_UP),),   
            ((KC.MW_UP, KC.MW_DN),),      
            ]



# created a class to display CapsLock/Lower or NumLock/NumUnlock on OLED
class OLEDLockStatus(LockStatus):
    def set_lock_oled(self):
        caps = ""
        nums = "NumLk"
        scroll = ""
        if self.get_caps_lock():
            caps = "Caps"
        else:
            caps = ""
        if self.get_num_lock():
            nums = "NumLk"
        else:
            nums= ""
        if self.get_scroll_lock():
            scroll = "ScrlLk"
        else:
            scroll = ""
        oled_ext._views[2] = {0:OledReactionType.STATIC,1:[caps]}
        oled_ext._views[3] = {0:OledReactionType.STATIC,1:[nums]}
        oled_ext._views[5] = {0:OledReactionType.STATIC,1:[scroll]}

        keyboard.sandbox.lock_update = 1

    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)
        if self.report_updated:
            self.set_lock_oled()

keyboard.extensions.append(oled_ext)
keyboard.extensions.append(OLEDLockStatus())

wpm_ext = WPM()
keyboard.extensions.append(wpm_ext)
print(wpm_ext.calculate_wpm())




if __name__ == '__main__':
    keyboard.go()
