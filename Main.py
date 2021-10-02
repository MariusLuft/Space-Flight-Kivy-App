from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400') 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color
from kivy.properties import Clock
#from kivy.core.window.Window import Window
from kivy.core.window import Window
from kivy import platform



class MainWidget(Widget):
    from transforms import transform, transform2D, transformPerspective
    from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up 
    perspecitvePointX = NumericProperty(0)
    perspecitvePointY = NumericProperty(0)

    verticalLines = []
    numVerticalLines = 10
    spacingVerticalLines = 0.25

    
    horizontalLines = []
    numhorizontalLines = 15
    spacinghorizontalLines = 0.1

    currentOffsetY = 0
    speed = 3

    speedx = 12
    currentSpeedX = 0
    currentOffsetX = 0


    def __init__(self, **args):
        super(MainWidget, self).__init__(**args)
        #print("init width: " + str(self.width) + " init height: " + str(self.height))
        self.initVerticalLines()
        self.initHorizontalLines()
        if self.is_desktop:
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def is_desktop():
        if platform in ('linux', 'win', 'macosx'):
            return True

    def initVerticalLines(self):
        with self.canvas:
            Color(1,1,1) 
            # self.line = Line(Points=[100,0,100,100])
            for i in range(0, self.numVerticalLines):
                self.verticalLines.append(Line())

    def on_size(self, *args):
        #print("init width: " + str(self.width) + " init height: " + str(self.height))
        self.perspecitvePointX = self.width/2
        self.perspecitvePointY = self.height*0.75

    def getLineXFromOffset(self, index):
        #find middle
        centerX = self.perspecitvePointX
        #calculate the spacing
        spacing = self.spacingVerticalLines * self.width
        # offset to start from the left line
        offset = index - 0.5
        lineX = centerX + offset* spacing + self.currentOffsetX
        return lineX

    def updateVerticalLines(self):
        startIndex = -int(self.numVerticalLines/2)+ 1
        for i in range(startIndex, startIndex + self.numVerticalLines):
            lineX = self.getLineXFromOffset(i)
            x1, y1 = self.transform(lineX, 0)
            x2, y2 = self.transform(lineX, self.width)
            self.verticalLines[i].points = [x1,y1,x2, y2]

        
    def initHorizontalLines(self):
        with self.canvas:
            Color(1,1,1) 
            # self.line = Line(Points=[100,0,100,100])
            for i in range(0, self.numhorizontalLines):
                self.horizontalLines.append(Line())

    def updateHorizontalLines(self):
        #find middle
        centerX = self.width/2
        #calculate the spacing
        spacing = self.spacingVerticalLines * self.width
        # offset to start from the left line
        offset = -int(self.numVerticalLines/2) + 0.5 # + 0.5 to shift half a spacing

        spacingY = self.spacinghorizontalLines * self.height
        xMin = centerX + spacing*offset + self.currentOffsetX
        xMax = centerX - spacing*offset + self.currentOffsetX

        for i in range(0, self.numhorizontalLines):
            lineY = int(i * spacingY - self.currentOffsetY)
            x1, y1 = self.transform(xMin, lineY)
            x2, y2 = self.transform(xMax, lineY)
            self.horizontalLines[i].points = [x1,y1,x2, y2]

    def update(self, dt):
        # adjusts frame difference which stemms from different hardware performance
        timeFactor = dt*60
        self.updateVerticalLines()
        self.updateHorizontalLines()
        self.currentOffsetY += self.speed * timeFactor
        spacingY = self.spacinghorizontalLines * self.height
        if self.currentOffsetY >= spacingY:
            self.currentOffsetY -= spacingY
        self.currentOffsetX += self.currentSpeedX * timeFactor
            

class GalaxyApp(App):
	pass


if __name__ == '__main__':    
    GalaxyApp().run()