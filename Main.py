from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color

class MainWidget(Widget):
    perspecitvePointX = NumericProperty(0)
    perspecitvePointY = NumericProperty(0)
    line = None

    def __init__(self, **args):
        super(MainWidget, self).__init__(**args)
        #print("init width: " + str(self.width) + " init height: " + str(self.height))
        self.initVerticalLines()

    def on_parent(self, widget, parent):
        pass
    
    def on_size(self, *args):
        #print("init width: " + str(self.width) + " init height: " + str(self.height))
        self.perspecitvePointX = self.width/2
        self.perspecitvePointY = self.height*0.75
        self.updateVerticalLines()

    def on_perspecitvePointX(self, widget, value):
        #print("PX: " +  str(value))
        pass 
    
    def on_perspecitvePointY(self, widget, value):
        #print("PY: " +  str(value))
        pass 

    def initVerticalLines(self):
        with self.canvas:
            Color(1,1,1) 
            self.line = Line(Points=[100,0,100,100])

    def updateVerticalLines(self):
        centerX = self.width/2
        self.line.points = [centerX, 0, centerX, 100]
            

class GalaxyApp(App):
	pass


if __name__ == '__main__':    
    GalaxyApp().run()


