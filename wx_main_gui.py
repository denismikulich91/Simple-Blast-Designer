import wx
from side_dialogs import ImportCsvDialog, LayersAndProperties, LayerManager
from wx.lib.floatcanvas import FloatCanvas, NavCanvas
import wx.lib.agw.ribbon as rb
from pubsub import pub
from shapely.geometry import LineString
import os
from csv_settings import CsvDataHandler
from lines_and_points import LinesAndPoints

# Buttons IDs
ID_IMPORT_CSV = wx.ID_HIGHEST + 1
ID_CLEAR_ALL = ID_IMPORT_CSV + 1
ID_DRAW = ID_CLEAR_ALL + 1
ID_DRAW_SETTINGS = ID_DRAW + 1


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simple Blast Designer')
        self.SetSize(1300, 800)
        self.SetBackgroundColour(wx.Colour(85, 150, 140, 255))
        self.Center()
        self.main_panel = MainPanel(self)
        self.Show()
        # self.Maximize(True)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.DEFAULT_CURSOR = wx.Cursor('Source/bitmaps/base_cursor.cur', type=wx.BITMAP_TYPE_CUR)
        self.SetCursor(self.DEFAULT_CURSOR)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.properties_panel = LayersAndProperties(self)

        layer_manager_sizer = wx.BoxSizer(wx.VERTICAL)
        self.layer_manager = LayerManager(self)
        
        layer_manager_sizer.Add(self.properties_panel, 2, wx.EXPAND)
        layer_manager_sizer.Add(self.layer_manager, 1, wx.EXPAND | wx.TOP, border=5)

        self.canvas = Canvas(self, self.properties_panel, self.layer_manager)
        self.info_panel = InfoPanel(self, self.canvas.coordinates)
        self.ribbon = RibbonFrame(self, self.canvas)
        canvas_sizer = wx.BoxSizer(wx.HORIZONTAL)
        canvas_sizer.Add(self.canvas, 5,  flag=wx.RIGHT | wx.EXPAND, border=5)
        canvas_sizer.Add(layer_manager_sizer, 1,  flag=wx.TOP | wx.EXPAND, border=0)
        main_sizer.Add(self.ribbon, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, border=10)
        main_sizer.Add(canvas_sizer, 5,  flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
        main_sizer.Add(self.info_panel,  flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        self.SetSizer(main_sizer)

    def clear_all(self, evt):
        self.canvas.clear_canvas(evt)


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

        self.info_label = wx.StaticText(self, label='Nothing is going on.....', size=(1000, -1))
        status_panel_sizer.Add(self.info_label, 15,  flag=wx.LEFT | wx.ALIGN_CENTER, border=25)

        self.SetSizer(status_panel_sizer)

    def update_coordinates_via_pubsub(self, updated_coordinates):
        self.x_entry.SetValue(str(round(updated_coordinates[0], 3)))
        self.y_entry.SetValue(str(round(updated_coordinates[1], 3)))

    def update_info_label_via_pubsub(self, info):
        self.info_label.SetLabel(info)


class RibbonFrame(wx.Panel):
    IsDrawing = False
    IsSettingsOn = False

    def __init__(self, parent, canvas):
        super().__init__(parent=parent)
        self.canvas = canvas
        lock_icon = wx.Bitmap('Source/bitmaps/lbdecrypted.png')
        dices = wx.Bitmap('Source/bitmaps/lbroll.png')
        csv_import = wx.Bitmap('Source/bitmaps/csv_import.png')
        str_import = wx.Bitmap('Source/bitmaps/str_import.png')
        bin = wx.Bitmap('Source/bitmaps/bin.png')
        file_save = wx.Bitmap('Source/bitmaps/filesave.png')
        settings = wx.Bitmap('Source/bitmaps/settings.png')
        new_file = wx.Bitmap('Source/bitmaps/new_file.png')
        paste = wx.Bitmap('Source/bitmaps/paste.png')
        finder = wx.Bitmap('Source/bitmaps/finder.png')
        info = wx.Bitmap('Source/bitmaps/info.png')
        look_and_feel = wx.Bitmap('Source/bitmaps/look_and_feel.png')
        print_button = wx.Bitmap('Source/bitmaps/print.png')

        draw_settings = wx.Bitmap('Source/bitmaps/draw_settings.png')
        draw_tool = wx.Bitmap('Source/bitmaps/draw_tool.png')
        get_item_info = wx.Bitmap('Source/bitmaps/get_item_info.png')
        get_color_info = wx.Bitmap('Source/bitmaps/get_color_info.png')
        crop = wx.Bitmap('Source/bitmaps/crop.png')
        measurement = wx.Bitmap('Source/bitmaps/measurement.png')
        insert_text = wx.Bitmap('Source/bitmaps/insert_text.png')
        copy_data = wx.Bitmap('Source/bitmaps/copy_data.png')

        self._colour_data = wx.ColourData()
        self._ribbon = rb.RibbonBar(self, wx.ID_ANY, agwStyle=rb.RIBBON_BAR_DEFAULT_STYLE)
        self._bitmap_creation_dc = wx.MemoryDC()
        # color_settings = self._ribbon.GetArtProvider()
        self._ribbon.GetArtProvider().SetColourScheme(wx.Colour(85, 150, 140, 255),
                                                      wx.Colour(255, 50, 40, 255),
                                                      wx.Colour(85, 50, 40, 255))

        home = rb.RibbonPage(self._ribbon, wx.ID_ANY, "Main")
        main_toolbar_panel = rb.RibbonPanel(home, wx.ID_ANY, "Main Tools", wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, agwStyle=rb.RIBBON_PANEL_NO_AUTO_MINIMISE)
        toolbar = rb.RibbonToolBar(main_toolbar_panel)

        toolbar.AddTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddTool(wx.ID_NEW, wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(32, 32)))
        toolbar.AddSeparator()

        toolbar.AddTool(wx.ID_NEW, paste)
        toolbar.AddTool(wx.ID_ANY, new_file)
        toolbar.AddTool(wx.ID_ANY, file_save)
        toolbar.AddSeparator()
        toolbar.AddTool(wx.ID_UNDO, finder)
        toolbar.AddTool(wx.ID_UNDO, info)
        toolbar.AddTool(ID_CLEAR_ALL, bin)
        toolbar.AddSeparator()
        toolbar.AddTool(wx.ID_ANY, print_button)
        toolbar.AddTool(wx.ID_ANY, look_and_feel)
        toolbar.AddTool(wx.ID_ANY, settings)

        properties_panel = rb.RibbonPanel(home, wx.ID_ANY, "Properties (Double-click on item to generate)")

        label_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
        self._bitmap_creation_dc.SetFont(label_font)

        design_tools = rb.RibbonPage(self._ribbon, wx.ID_ANY, "Design", wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 15)))
        import_tools_panel = rb.RibbonPanel(design_tools, wx.ID_ANY, "Import Tools", wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, agwStyle=rb.RIBBON_PANEL_NO_AUTO_MINIMISE)
        import_tools = rb.RibbonToolBar(import_tools_panel)
        import_tools.AddTool(ID_IMPORT_CSV, csv_import)

        design_panel = rb.RibbonPanel(design_tools, wx.ID_ANY, "Design Tools", wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, agwStyle=rb.RIBBON_PANEL_NO_AUTO_MINIMISE)
        design_tools = rb.RibbonToolBar(design_panel)
        design_tools.AddTool(ID_DRAW_SETTINGS, draw_settings, kind=rb.RIBBON_BUTTON_TOGGLE)
        design_tools.AddTool(ID_DRAW, draw_tool, kind=rb.RIBBON_BUTTON_TOGGLE)
        design_tools.AddTool(wx.ID_ANY, get_item_info)
        design_tools.AddTool(wx.ID_ANY, get_color_info)
        design_tools.AddTool(wx.ID_ANY, crop)
        design_tools.AddTool(wx.ID_ANY, measurement)
        design_tools.AddTool(wx.ID_ANY, insert_text)
        design_tools.AddTool(wx.ID_ANY, copy_data)

        import_tools.AddTool(wx.ID_ANY, str_import)
        # import_tools.AddTool(wx.ID_ANY, test)
        # import_tools.AddTool(wx.ID_ANY, test)

        s = wx.BoxSizer(wx.HORIZONTAL)

        s.Add(self._ribbon, 1,  wx.EXPAND, border=0)
        self._ribbon.Realize()
        self.SetSizer(s)
        self.BindEvents(import_tools, toolbar, design_tools)
        self.Show()

    def BindEvents(self, import_tools, toolbar, design_tools):
        import_tools.Bind(rb.EVT_RIBBONTOOLBAR_CLICKED, self.import_csv_button, id=ID_IMPORT_CSV)
        toolbar.Bind(rb.EVT_RIBBONTOOLBAR_CLICKED, self.canvas.clear_canvas,  id=ID_CLEAR_ALL)
        design_tools.Bind(rb.EVT_RIBBONTOOLBAR_CLICKED, self.check, id=ID_DRAW)

    def check(self, evt):
        if not self.IsDrawing:
            RibbonFrame.IsDrawing = True
            spaces = ' ' * 20
            pub.sendMessage("update_info_label",
                            info=f'Drawing Line...{spaces}Left click to draw, Shift + Right Click '
                                 f'to close or Right Click to start new line')
            self.canvas.SetCursor(self.canvas.CAD_CURSOR)
        else:
            RibbonFrame.IsDrawing = False
            self.canvas.update_lines_and_points()
            pub.sendMessage("update_info_label", info='Nothing is going on.....')
            self.canvas.SetCursor(self.canvas.DEFAULT_CURSOR)


    def import_csv_button(self, evt):
        ImportCsvDialog()


class Canvas(wx.Panel):
    temp_drawing_coords = []
    # temp_line = LineString(temp_drawing_coords)
    # temp_length = temp_line.length

    def __init__(self, parent, properties_panel, layer_panel):
        cad_image = wx.Image('Source/Cursors/main_cad_cursor.cur')
        dragging_image = wx.Image('Source/bitmaps/dragging_cursor.cur')

        for image in [cad_image, dragging_image]:
            image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 18)
            image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 18)

        self.lines_and_points = LinesAndPoints()
        self.DEFAULT_CURSOR = wx.Cursor('Source/bitmaps/base_cursor.cur', type=wx.BITMAP_TYPE_CUR)
        self.CAD_CURSOR = wx.Cursor(cad_image)
        self.DRAGGING_CURSOR = wx.Cursor(dragging_image)

        pub.subscribe(self.draw_data_on_canvas, "draw_data_on_canvas")
        super().__init__(parent=parent)
        self.start = (0, 0)
        canvas_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.NC = NavCanvas.NavCanvas(self, BackgroundColor="White")
        self.main_canvas = self.NC.Canvas
        self.NC.ToolBar.Destroy()
        self.initial_coordinates = (0, 0)
        self.Bind(FloatCanvas.EVT_MOUSEWHEEL, self.zoom)
        self.Bind(FloatCanvas.EVT_MOTION, self.dragging)
        self.Bind(FloatCanvas.EVT_MIDDLE_UP, self.update_cursor)
        self.main_canvas.Bind(wx.EVT_MIDDLE_DOWN, self.get_initial_coordinates)
        self.main_canvas.Bind(wx.EVT_MIDDLE_DCLICK, self.zoom_all)
        self.main_canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.drawing)
        self.main_canvas.Bind(FloatCanvas.EVT_RIGHT_DOWN, self.drawing)
        self.coordinates = (0, 0)
        canvas_sizer.Add(self.NC, 4, flag=wx.EXPAND, border=10)
        self.SetSizer(canvas_sizer)

        self.properties = properties_panel
        self.layer_manager_panel = layer_panel

        self.layers = list(self.layer_manager_panel.layer_states.keys())


    def clear_canvas(self, evt):
        print(self.lines_and_points.lines_dict)
        self.lines_and_points.clear_all()  # TODO: Create a 'are you sure' dialog

        # Not sure if this needed when I can achieve permanent link between canvas and Lines and Points dict
        self.main_canvas.ClearAll(evt)
        self.main_canvas.Update()
        self.main_canvas.ZoomToBB(NewBB=None, DrawFlag=True)
        print(self.lines_and_points.lines_dict)

    def draw_data_on_canvas(self, import_instance, data_dict):  # Imported CSV data!!!!
        [self.main_canvas.AddObject(x) for x in import_instance.prepare_data_to_draw_in_canvas(
            FloatCanvas.Line, data_dict['color'], data_dict['style'], data_dict['width'])]

        [self.main_canvas.AddObject(x) for x in import_instance.prepare_data_to_draw_in_canvas(
            FloatCanvas.PointSet, data_dict['color'], 3, data_dict['width'])]

        self.main_canvas.ZoomToBB(NewBB=None, DrawFlag=True)
        self.main_canvas.Draw()
        self.lines_and_points.add_new_line(import_instance.is_multi, import_instance.get_data, data_dict['color'],
                                           data_dict['style'], data_dict['width'],
                                           layer=self.layer_manager_panel.get_active_layer)

        # self.lines_and_points.get_info(self.lines_and_points.object_id)


    def zoom_all(self, evt):
        self.main_canvas.ZoomToBB(NewBB=None, DrawFlag=True)

    def zoom(self, evt):
        if evt.GetWheelRotation() > 0:
            self.main_canvas.Zoom(1 + 0.05)
        else:
            self.main_canvas.Zoom(1 - 0.05)

    def get_initial_coordinates(self, evt):
        self.initial_coordinates = evt.GetPosition()

    def update_cursor(self, evt):
        if RibbonFrame.IsDrawing:
            self.SetCursor(self.CAD_CURSOR)
            pub.sendMessage("update_info_label", info='Drawing Line...')
        else:
            self.SetCursor(self.DEFAULT_CURSOR)
            pub.sendMessage("update_info_label", info='Nothing is going on.....')

    def dragging(self, evt):
        self.coordinates = evt.Coords
        pub.sendMessage("update_coordinates", updated_coordinates=self.coordinates)

        if evt.Dragging() and evt.MiddleIsDown():
            self.SetCursor(self.DRAGGING_CURSOR)
            self.main_canvas.MoveImage((self.initial_coordinates - evt.GetPosition()), 'Pixel')
            self.initial_coordinates = evt.GetPosition()
            pub.sendMessage("update_info_label", info='Dragging...')

    def drawing(self, evt):
        spaces = ' ' * 20
        if not RibbonFrame.IsDrawing:  # Function for selecting data
            print('Selecting data...')
        elif RibbonFrame.IsDrawing and evt.Button(1):
            temp_drawing = FloatCanvas.Point(evt.Coords, self.properties.get_color, Diameter=3)
            Canvas.temp_drawing_coords.append(evt.Coords)
            pub.sendMessage("update_info_label", info=f'Drawing Line...{spaces}Current length: {spaces}'
                                                      f'Left click to draw, Shift + Right Click to close '
                                                      f'or Right Click to start new line')
            if len(Canvas.temp_drawing_coords) > 1:
                pub.sendMessage("update_info_label", info=f'Drawing Line...{spaces}Current length: '
                                                          f'{round (LineString(Canvas.temp_drawing_coords).length, 1)}'
                                                          f'{spaces}Left click to draw, Shift + Right Click to close or '
                                                          f'Right Click to start new line')
                temp_line_drawing = FloatCanvas.Line(Canvas.temp_drawing_coords,
                                                     self.properties.get_color,
                                                     self.properties.get_style,
                                                     self.properties.get_width)
                self.main_canvas.AddObject(temp_line_drawing)
            self.main_canvas.AddObject(temp_drawing)
            self.main_canvas.Draw(True)

        elif RibbonFrame.IsDrawing and evt.Button(3) and evt.ShiftDown() and len(Canvas.temp_drawing_coords) > 2:
            Canvas.temp_drawing_coords.append(Canvas.temp_drawing_coords[0])
            temp_line_drawing = FloatCanvas.Line(Canvas.temp_drawing_coords, self.properties.get_color,
                                                 self.properties.get_style, self.properties.get_width)
            self.main_canvas.AddObject(temp_line_drawing)
            self.main_canvas.Draw(True)
            pub.sendMessage("update_info_label",
                            info=f'Drawing Line...{spaces}Shift + Right Click to close or Right Click to start new line')
            self.update_lines_and_points()
        elif RibbonFrame.IsDrawing and evt.Button(3) and len(Canvas.temp_drawing_coords) > 1:
            pub.sendMessage("update_info_label",
                            info=f'Drawing Line...{spaces}Shift + Right Click to close or Right Click to start new line')
            self.update_lines_and_points()

    def update_lines_and_points(self):
        if Canvas.temp_drawing_coords:
            coordinates = [list(x) for x in Canvas.temp_drawing_coords]
            self.lines_and_points.add_new_line(False, coordinates, self.properties.get_color, self.properties.get_style,
                                               self.properties.get_width, self.layer_manager_panel.get_active_layer)
            self.lines_and_points.get_info_of_last_object()
            Canvas.temp_drawing_coords = []


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
