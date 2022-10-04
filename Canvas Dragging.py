import wx
from wx.lib.floatcanvas import FloatCanvas

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.Size = (500, 500)
        self.panel = ImagePanel(self)
        self.Show()

class ImagePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_coordinates = (0,0)
        self.Canvas = FloatCanvas.FloatCanvas(self, -1, size=(500, 500), BackgroundColor="White")
        # self.Canvas.WheelEvent(self.zoom)
        self.Canvas.Bind(wx.EVT_MOUSEWHEEL, self.zoom) 
        self.Canvas.Bind(wx.EVT_MOTION, self.move) 
        self.Canvas.Bind(wx.EVT_MIDDLE_DOWN, self.get_coords)


        # add a circle
        cir = FloatCanvas.Circle((10, 10), 100)
        self.Canvas.AddObject(cir)

        # add a rectangle
        rect = FloatCanvas.Rectangle((110, 10), (100, 100), FillColor='Red')
        self.Canvas.AddObject(rect)

        self.Canvas.Draw()
        self.Layout()

    def get_coords(self, evt):
        self.initial_coordinates = evt.GetPosition()
        print('Down')

    def move(self, evt):
        if evt.Dragging() and evt.MiddleIsDown():  
            self.Canvas.MoveImage((self.initial_coordinates - evt.GetPosition()), 'Pixel')
            # print(c)
            print(evt.GetPosition() - self.initial_coordinates)
            self.initial_coordinates = evt.GetPosition()

    def zoom(self, evt):

        if evt.GetWheelRotation() > 0:
            self.Canvas.Zoom(1 - 0.05)
        elif evt.GetWheelRotation() < 0:
            self.Canvas.Zoom(1 + 0.05)

app = wx.App()
frame = MyFrame(None)
app.MainLoop()

