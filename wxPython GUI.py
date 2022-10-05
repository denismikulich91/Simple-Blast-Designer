import wx
from wx.lib.floatcanvas import FloatCanvas

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simple Blast Designer')
        self.SetSize(1200, 800)
        main_panel = MainPanel(self)
        self.Show()
        # self.Maximize(True)

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        canvas_sizer = wx.BoxSizer()
        main_canvas = Canvas(self)
        canvas_sizer.Add(main_canvas, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(canvas_sizer)
        self.Show()

class Canvas(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.start = (0, 0)
        self.Canvas = FloatCanvas.FloatCanvas(self, -1, size=wx.Size(1000, 1000), BackgroundColor="White")
        self.initial_coordinates = (0, 0)
        self.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.zoom)
        self.Bind(FloatCanvas.EVT_MOTION, self.dragging)
        self.Canvas.Bind(wx.EVT_MIDDLE_DOWN, self.get_coords)


        # add a circle
        cir = FloatCanvas.Circle((500, 500), 100)
        self.Canvas.AddObject(cir)

        # add a rectangle
        rect = FloatCanvas.Rectangle((110, 10), (100, 100), FillColor='Red')
        self.Canvas.AddObject(rect)

        self.Canvas.Draw()
        self.Show()

        # add a circle
        cir = FloatCanvas.Circle((10, 10), 100)
        self.Canvas.AddObject(cir)

        # add a rectangle
        rect = FloatCanvas.Rectangle((110, 10), (100, 100), FillColor='Red')
        self.Canvas.AddObject(rect)

        self.Canvas.Draw()

    def zoom(self, evt):
        if evt.GetWheelRotation() > 0:
            self.Canvas.Zoom(1 + 0.05)
        else:
            self.Canvas.Zoom(1 - 0.05)

    def get_coords(self, evt):
        self.initial_coordinates = evt.GetPosition()

    def dragging(self, evt):
        if evt.Dragging() and evt.MiddleIsDown():
            self.Canvas.MoveImage((self.initial_coordinates - evt.GetPosition()), 'Pixel')
            self.initial_coordinates = evt.GetPosition()


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
