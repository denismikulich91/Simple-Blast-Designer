import wx
from wx.lib.floatcanvas import FloatCanvas
import wx.lib.agw.ribbon as RB


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
        canvas_sizer = wx.BoxSizer(wx.VERTICAL)
        main_canvas = Canvas(self)
        ribbon = RibbonFrame(self)
        canvas_sizer.Add(ribbon, flag=wx.ALL | wx.EXPAND, border=10)
        canvas_sizer.Add(main_canvas, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizer(canvas_sizer)
        self.Show()


class RibbonFrame(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent=parent)
        lock_icon = wx.Bitmap('Source/bitmaps/lbdecrypted.png')
        dices = wx.Bitmap('Source/bitmaps/lbroll.png')
        self._colour_data = wx.ColourData()

        self._ribbon = RB.RibbonBar(self, wx.ID_ANY, agwStyle=RB.RIBBON_BAR_DEFAULT_STYLE|RB.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)
        self._bitmap_creation_dc = wx.MemoryDC()
        color_settings = self._ribbon.GetArtProvider()
        self._ribbon.GetArtProvider().SetColourScheme(wx.Colour(85, 150, 140, 255),
                                                      wx.Colour(255, 50, 40, 255),
                                                      wx.Colour(85, 50, 40, 255))

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Main")
        main_toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "Main Tools", wx.NullBitmap, wx.DefaultPosition,
                                       wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE|RB.RIBBON_PANEL_EXT_BUTTON)
        toolbar = RB.RibbonToolBar(main_toolbar_panel)

        toolbar.AddTool(wx.ID_NEW, wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddTool(wx.ID_NEW, wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddSeparator()

        toolbar.AddTool(wx.ID_NEW, wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddSeparator()
        toolbar.AddTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddSeparator()
        toolbar.AddTool(wx.ID_ANY, lock_icon)
        toolbar.AddTool(wx.ID_ANY, dices)
        toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(32, 32)))

        properties_panel = RB.RibbonPanel(home, wx.ID_ANY, "Properties (Double-click on item to generate)")

        # sizer_panelcombo = wx.TextCtrl(properties_panel, wx.ID_ANY, size=(-1, -1))
        sizer_panelsizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panelsizer.AddSpacer(700)
        # sizer_panelsizer.Add(sizer_panelcombo, 1, wx.ALL|wx.EXPAND, 2)

        sizer_panelsizer.AddStretchSpacer(1)
        properties_panel.SetSizer(sizer_panelsizer)

        label_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
        self._bitmap_creation_dc.SetFont(label_font)

        dummy_2 = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Empty Page", wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 15)))
        shapes = RB.RibbonButtonBar(dummy_2)



        self._ribbon.Realize()
        s = wx.BoxSizer(wx.VERTICAL)

        s.Add(self._ribbon, 0, wx.EXPAND)
        self.SetSizer(s)
        self.Show()

class Canvas(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.start = (0, 0)
        self.Canvas = FloatCanvas.FloatCanvas(self, -1, size=wx.Size(1200, 1000), BackgroundColor="White")
        self.initial_coordinates = (0, 0)
        self.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.zoom)
        self.Bind(FloatCanvas.EVT_MOTION, self.dragging)
        self.Canvas.Bind(wx.EVT_MIDDLE_DOWN, self.get_initial_coordinates)

        cir = FloatCanvas.Circle((10, 10), 100)
        self.Canvas.AddObject(cir)
        rect = FloatCanvas.Rectangle((110, 10), (100, 100), FillColor='Red')
        self.Canvas.AddObject(rect)

        self.Canvas.Draw()

    def zoom(self, evt):
        if evt.GetWheelRotation() > 0:
            self.Canvas.Zoom(1 + 0.05)
        else:
            self.Canvas.Zoom(1 - 0.05)

    def get_initial_coordinates(self, evt):
        self.initial_coordinates = evt.GetPosition()

    def dragging(self, evt):
        if evt.Dragging() and evt.MiddleIsDown():
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZENESW))
            self.Canvas.MoveImage((self.initial_coordinates - evt.GetPosition()), 'Pixel')
            self.initial_coordinates = evt.GetPosition()


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
