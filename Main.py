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
from kivy.graphics.vertex_instructions import Quad, Triangle
import random


class MainWidget(Widget):
    from transforms import transform, transform2D, transformPerspective
    from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up 
    perspecitvePointX = NumericProperty(0)
    perspecitvePointY = NumericProperty(0)

    verticalLines = []
    numVerticalLines = 10
    spacingVerticalLines = 0.25

    
    horizontalLines = []
    numhorizontalLines = 25
    spacinghorizontalLines = 0.1

    currentOffsetY = 0
    speed = 3

    speedx = 12
    currentSpeedX = 0
    currentOffsetX = 0

    currentLoopIndex = 0

    tiles = []
    numberOfTiles = 15
    tilesCoordinates = []

    ship = None
    SHIP_WIDTH = 0.1
    SHIP_HEIGHT =  0.035
    SHIP_BASE_Y = 0.04


    def __init__(self, **args):
        super(MainWidget, self).__init__(**args)
        #print("init width: " + str(self.width) + " init height: " + str(self.height))
        self.initVerticalLines()
        self.initHorizontalLines()
        self.initTiles()     
        self.initShip()
        self.prefillTiles()
        self.generateTileCoordinates()
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

    def initTiles(self):
        with self.canvas:
            Color(1,1,1) 
            for i in range(0, self.numberOfTiles):
                self.tiles.append(Quad())

    def initShip(self): 
        with self.canvas:
            Color(0,1,1) 
            self.ship = Triangle()

    def updateShip(self):
        centerX = self.width/2
        shipBaseY = self.SHIP_BASE_Y * self.height
        shipHalfWidth = self.SHIP_WIDTH * self.width / 2
        shipheightAbsolute = self.SHIP_HEIGHT * self.height
        #  2
        # 1 3
        x1, y1 = self.transform(centerX - shipHalfWidth, shipBaseY)
        x2, y2 = self.transform(centerX, shipBaseY + shipheightAbsolute)
        x3, y3 = self.transform(centerX + shipHalfWidth, shipBaseY)
        self.ship.points = [x1, y1, x2, y2, x3, y3]
                

    def generateTileCoordinates(self):
        lastY = 0
        lastX = 0
        # clean coordiantes that leave the screen
        for i in range(len(self.tilesCoordinates)- 1, -1, -1):
            if self.tilesCoordinates[i][1] < self.currentLoopIndex:
                del self.tilesCoordinates[i]

        if len(self.tilesCoordinates) > 0:
            # stores last tile information
            lastcoordiantes = self.tilesCoordinates[-1]
            # increments y of last tile to make it be further away
            lastY = lastcoordiantes[1] + 1
            lastX = lastcoordiantes[0]

        # only append new coordinates if there is space
        for i in range(len(self.tilesCoordinates), self.numberOfTiles):
            # 0 = straight
            # 1 = right
            # 2 = left
            r = random.randint(0,2)

            startIndex = -int(self.numVerticalLines/2) + 1
            endIndex = startIndex + self.numVerticalLines - 1

            if lastX <= startIndex:
                r = 1
            if lastX >= endIndex-1: 
                r = 2
           
            self.tilesCoordinates.append((lastX, lastY))

            if r == 1:
                lastX += 1
                self.tilesCoordinates.append((lastX, lastY))
                lastY += 1
                self.tilesCoordinates.append((lastX, lastY))
            if r == 2:
                lastX -= 1
                self.tilesCoordinates.append((lastX, lastY))
                lastY += 1
                self.tilesCoordinates.append((lastX, lastY))

            lastY += 1
        
    def prefillTiles(self):
        numberOfPrefilledTiles = 13
        for i in range(1, numberOfPrefilledTiles):
            self.tilesCoordinates.append((0, i))


    def on_size(self, *args):
        #print("init width: " + str(self.width) + " init height: " + str(self.height))
        self.perspecitvePointX = self.width/2
        self.perspecitvePointY = self.height*0.75

    def getLineXFromIndex(self, index):
        #find middle
        centerX = self.perspecitvePointX
        #calculate the spacing
        spacing = self.spacingVerticalLines * self.width
        # offset to start from the left line
        offset = index - 0.5
        lineX = centerX + offset* spacing + self.currentOffsetX
        return lineX

    def getLineYFromIndex(self, index):
        spacingY = self.spacinghorizontalLines * self.height
        lineY = index * spacingY - self.currentOffsetY
        return lineY

    def updateVerticalLines(self):
        startIndex = -int(self.numVerticalLines/2)+ 1
        for i in range(startIndex, startIndex + self.numVerticalLines):
            lineX = self.getLineXFromIndex(i)
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
        startIndex = -int(self.numVerticalLines/2) + 1
        endIndex = startIndex + self.numVerticalLines - 1
        xMin = self.getLineXFromIndex(startIndex)
        xMax = self.getLineXFromIndex(endIndex)

        for i in range(0, self.numhorizontalLines):
            lineY = self.getLineYFromIndex(i)
            x1, y1 = self.transform(xMin, lineY)
            x2, y2 = self.transform(xMax, lineY)
            self.horizontalLines[i].points = [x1,y1,x2, y2]

    def updateTiles(self):
        for i in range(0, self.numberOfTiles):
            tile = self.tiles[i]
            tilesCoordinates = self.tilesCoordinates[i]
            # get xmin, ymin of the tile
            xmin, ymin = self.getTileCoordinates(tilesCoordinates[0], tilesCoordinates[1])
            xmax, ymax = self.getTileCoordinates(tilesCoordinates[0] + 1, tilesCoordinates[1] + 1)

            # construct the tile based on xmin, ymin
            # 2     3
            #
            # 1     4     
            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def getTileCoordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.currentLoopIndex  
        x = self.getLineXFromIndex(ti_x)
        y = self.getLineYFromIndex(ti_y)
        return x, y

    def update(self, dt):
        # adjusts frame difference which stemms from different hardware performance
        timeFactor = dt*60
        self.updateVerticalLines()
        self.updateHorizontalLines()
        self.updateTiles()
        self.updateShip()
        self.currentOffsetY += self.speed * timeFactor
        spacingY = self.spacinghorizontalLines * self.height
        # one vertical level has passed
        if self.currentOffsetY >= spacingY:
            self.currentOffsetY -= spacingY
            self.currentLoopIndex += 1
            self.generateTileCoordinates()
        self.currentOffsetX += self.currentSpeedX * timeFactor

    
            

class GalaxyApp(App):
	pass


if __name__ == '__main__':    
    GalaxyApp().run()