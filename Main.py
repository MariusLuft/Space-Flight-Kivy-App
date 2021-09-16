from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color

class MainWidget(Widget):
    perspecitvePointX = NumericProperty(0)
    perspecitvePointY = NumericProperty(0)

    verticalLines = []
    numVerticalLines = 4
    spacingVerticalLines = 0.1

    
    horizontalLines = []
    numhorizontalLines = 4
    spacinghorizontalLines = 0.2


    def __init__(self, **args):
        super(MainWidget, self).__init__(**args)
        #print("init width: " + str(self.width) + " init height: " + str(self.height))
        self.initVerticalLines()
        self.initHorizontalLines()

    def on_parent(self, widget, parent):
        pass
    
    def on_size(self, *args):
        #print("init width: " + str(self.width) + " init height: " + str(self.height))
        self.perspecitvePointX = self.width/2
        self.perspecitvePointY = self.height*0.75
        self.updateVerticalLines()
        self.updateHorizontalLines()

    def on_perspecitvePointX(self, widget, value):
        #print("PX: " +  str(value))
        pass 
    
    def on_perspecitvePointY(self, widget, value):
        #print("PY: " +  str(value))
        pass 

    def initVerticalLines(self):
        with self.canvas:
            Color(1,1,1) 
            # self.line = Line(Points=[100,0,100,100])
            for i in range(0, self.numVerticalLines):
                self.verticalLines.append(Line())


    def updateVerticalLines(self):
        #find middle
        centerX = self.width/2
        #calculate the spacing
        spacing = self.spacingVerticalLines * self.width
        # offset to start from the left line
        offset = -int(self.numVerticalLines/2) + 0.5 

        for i in range(0, self.numVerticalLines):
            lineX = int(centerX + offset* spacing)
            x1, y1 = self.transform(lineX, 0)
            x2, y2 = self.transform(lineX, self.width)
            self.verticalLines[i].points = [x1,y1,x2, y2]
            offset += 1

        
    def initHorizontalLines(self):
        with self.canvas:
            Color(1,1,1) 
            # self.line = Line(Points=[100,0,100,100])
            for i in range(0, self.numhorizontalLines):
                self.horizontalLines.append(Line())

    def updateHorizontalLines(self):
        xMin = 0
        xMax = self.width

        for i in range(0, self.numhorizontalLines):
            lineY = int(i * self.spacinghorizontalLines * self.height)
            x1, y1 = self.transform(xMin, lineY)
            x2, y2 = self.transform(xMax, lineY)
            self.horizontalLines[i].points = [x1,y1,x2, y2]

    def transform(self, x, y):
        # return self.transformPerspective(x, y)
        return self.transform2D(x,y)

    def transform2D(self, x, y):
        return int(x), int(y)
    
    def transformPerspective(self, x, y):
        transformedY = y * self.perspecitvePointY / self.height
        if transformedY > self.perspecitvePointY:
            transformedY = self.perspecitvePointY

        diffX = x - self.perspecitvePointX
        diffY = self.perspecitvePointY - transformedY

        proportionY = diffY/self.perspecitvePointY

        transformedX = self.perspecitvePointX + diffX * proportionY

        return int(transformedX), int(transformedY)
            

class GalaxyApp(App):
	pass


if __name__ == '__main__':    
    GalaxyApp().run()


