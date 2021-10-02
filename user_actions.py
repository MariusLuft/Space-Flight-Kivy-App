def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

def on_touch_down(self, touch):
        if touch.x < self.width/2:
            self.currentSpeedX = self.speedx
            #print("<-")
        else:
            self.currentSpeedX = -self.speedx
            #print("->")
    
def on_touch_up(self, touch):
    self.currentSpeedX = 0
    #print("Up")

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.currentSpeedX = self.speedx
    elif keycode[1] == 'right':
        self.currentSpeedX = -self.speedx

    return True

def on_keyboard_up(self, keyboard, keycode):
    self.currentSpeedX = 0