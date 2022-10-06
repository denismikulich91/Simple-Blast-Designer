import wx
from wx.lib.floatcanvas import FloatCanvas, NavCanvas
import wx.lib.agw.ribbon as RB
from pubsub import pub
import time


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simple Blast Designer')
        self.SetSize(1300, 800)
        self.SetBackgroundColour(wx.Colour(85, 150, 140, 255))
        self.Center()
        main_panel = MainPanel(self)
        self.Show()
        # self.Maximize(True)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_canvas = Canvas(self)
        ribbon = RibbonFrame(self)
        info_panel = InfoPanel(self, main_canvas.coordinates)

        main_sizer.Add(ribbon, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, border=10)
        main_sizer.Add(main_canvas, 5,  flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
        main_sizer.Add(info_panel,  flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        # TODO: Set up a proper sizing
        self.SetSizer(main_sizer)


class InfoPanel(wx.Panel):

    def __init__(self, parent, coordinates):
        super().__init__(parent=parent)
        pub.subscribe(self.update_coordinates_via_pubsub, "update_coordinates")
        pub.subscribe(self.update_info_label_via_pubsub, "update_info_label")

        status_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        x_label = wx.StaticText(self, 1, label='X:')
        status_panel_sizer.Add(x_label, flag=wx.RIGHT | wx.ALIGN_CENTER, border=5)

        self.x_entry = wx.TextCtrl(self, 1, value=str(coordinates[0]), size=(70, -1))
        status_panel_sizer.Add(self.x_entry, flag=wx.RIGHT | wx.ALIGN_CENTER, border=25)

        y_label = wx.StaticText(self, 1,  label='Y:')
        status_panel_sizer.Add(y_label, flag=wx.ALL | wx.ALIGN_CENTER, border=5)

        self.y_entry = wx.TextCtrl(self, 1, value=str(coordinates[1]), size=(70, -1))
        status_panel_sizer.Add(self.y_entry, flag=wx.RIGHT | wx.ALIGN_CENTER, border=25)

        z_label = wx.StaticText(self, 1, label='Z:')
        status_panel_sizer.Add(z_label, flag=wx.ALL | wx.ALIGN_CENTER, border=5)

        z_entry = wx.TextCtrl(self, 1, value='0', size=(70, -1))
        status_panel_sizer.Add(z_entry, flag=wx.RIGHT | wx.ALIGN_CENTER, border=25)

        self.info_label = wx.StaticText(self, label='Nothing is going on.....', size=(-1, -1))
        status_panel_sizer.Add(self.info_label, 1,  flag=wx.ALIGN_CENTER | wx.LEFT, border=500)

        self.SetSizer(status_panel_sizer)

    def update_coordinates_via_pubsub(self, updated_coordinates):
        self.x_entry.SetValue(str(round(updated_coordinates[0], 3)))
        self.y_entry.SetValue(str(round(updated_coordinates[1], 3)))

    def update_info_label_via_pubsub(self, info):
        self.info_label.SetLabel(info)




class RibbonFrame(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent=parent)
        lock_icon = wx.Bitmap('Source/bitmaps/lbdecrypted.png')
        dices = wx.Bitmap('Source/bitmaps/lbroll.png')
        csv_import = wx.Bitmap('Source/bitmaps/csv_import.png')
        str_import = wx.Bitmap('Source/bitmaps/str_import.png')
        self._colour_data = wx.ColourData()

        self._ribbon = RB.RibbonBar(self, wx.ID_ANY, agwStyle=RB.RIBBON_BAR_DEFAULT_STYLE)
        self._bitmap_creation_dc = wx.MemoryDC()
        color_settings = self._ribbon.GetArtProvider()
        self._ribbon.GetArtProvider().SetColourScheme(wx.Colour(85, 150, 140, 255),
                                                      wx.Colour(255, 50, 40, 255),
                                                      wx.Colour(85, 50, 40, 255))

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Main")
        main_toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "Main Tools", wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
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

        label_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
        self._bitmap_creation_dc.SetFont(label_font)

        design_tools = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Empty Page", wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 15)))
        import_tools_panel = RB.RibbonPanel(design_tools, wx.ID_ANY, "Import Tools", wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        import_tools = RB.RibbonToolBar(import_tools_panel)
        import_tools.AddTool(wx.ID_ANY, csv_import)
        import_tools.AddTool(wx.ID_ANY, str_import)
        # import_tools.AddTool(wx.ID_ANY, test)
        # import_tools.AddTool(wx.ID_ANY, test)

        s = wx.BoxSizer(wx.HORIZONTAL)

        s.Add(self._ribbon, 1,  wx.EXPAND, border=0)
        self._ribbon.Realize()
        self.SetSizer(s)
        self.Show()


class Canvas(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.start = (0, 0)
        canvas_sizer = wx.BoxSizer(wx.HORIZONTAL)
        NC = NavCanvas.NavCanvas(self, BackgroundColor="White")
        self.Canvas = NC.Canvas
        NC.ToolBar.Destroy()
        self.initial_coordinates = (0, 0)
        self.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.zoom)
        self.Bind(FloatCanvas.EVT_MOTION, self.dragging)
        self.Bind(FloatCanvas.EVT_MIDDLE_UP, self.update_cursor)
        self.Canvas.Bind(wx.EVT_MIDDLE_DOWN, self.get_initial_coordinates)
        self.Canvas.Bind(wx.EVT_MIDDLE_DCLICK, self.zoom_all)
        self.coordinates = (0, 0)
        canvas_sizer.Add(NC, 4, flag=wx.EXPAND, border=10)

        cir = FloatCanvas.Circle((10, 10), 100)
        self.Canvas.AddObject(cir)
        rect = FloatCanvas.Rectangle((110, 10), (100, 100), FillColor='Red')
        self.Canvas.AddObject(rect)
        self.SetSizer(canvas_sizer)
        self.Canvas.Draw()

    def zoom_all(self, evt):
        self.Canvas.ZoomToBB(NewBB=None, DrawFlag=True)

    def zoom(self, evt):
        if evt.GetWheelRotation() > 0:
            self.Canvas.Zoom(1 + 0.05)
        else:
            self.Canvas.Zoom(1 - 0.05)

    def get_initial_coordinates(self, evt):
        self.initial_coordinates = evt.GetPosition()

    def update_cursor(self, evt):
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        pub.sendMessage("update_info_label", info='Nothing is going on.....')

    def dragging(self, evt):
        self.coordinates = evt.Coords
        pub.sendMessage("update_coordinates", updated_coordinates=self.coordinates)

        if evt.Dragging() and evt.MiddleIsDown():
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
            self.Canvas.MoveImage((self.initial_coordinates - evt.GetPosition()), 'Pixel')
            self.initial_coordinates = evt.GetPosition()
            pub.sendMessage("update_info_label", info='Dragging...')


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
