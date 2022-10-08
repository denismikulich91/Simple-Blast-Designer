import wx
from wx.lib.floatcanvas import FloatCanvas, NavCanvas
import wx.lib.agw.ribbon as RB
from pubsub import pub
import os
from csv_settings import CsvDataHandler

# Buttons IDs
ID_IMPORT_CSV = wx.ID_HIGHEST + 1
ID_CLEAR_ALL = ID_IMPORT_CSV + 1
ID_DRAW = ID_CLEAR_ALL + 1

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simple Blast Designer')
        myCursor = wx.Cursor('Source/bitmaps/base_cursore.cur', type=wx.BITMAP_TYPE_CUR)
        self.SetCursor(myCursor)
        self.SetSize(1300, 800)
        self.SetBackgroundColour(wx.Colour(85, 150, 140, 255))
        self.Center()
        self.main_panel = MainPanel(self)
        self.Show()
        # self.Maximize(True)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas = Canvas(self)

        self.ribbon = RibbonFrame(self, self.canvas)
        self.info_panel = InfoPanel(self, self.canvas.coordinates)

        main_sizer.Add(self.ribbon, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, border=10)
        main_sizer.Add(self.canvas, 5,  flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
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

        self.info_label = wx.StaticText(self, label='Nothing is going on.....', size=(500, -1))
        status_panel_sizer.Add(self.info_label, 1,  flag=wx.ALIGN_CENTER | wx.LEFT, border=500)

        self.SetSizer(status_panel_sizer)

    def update_coordinates_via_pubsub(self, updated_coordinates):
        self.x_entry.SetValue(str(round(updated_coordinates[0], 3)))
        self.y_entry.SetValue(str(round(updated_coordinates[1], 3)))

    def update_info_label_via_pubsub(self, info):
        self.info_label.SetLabel(info)


class RibbonFrame(wx.Panel):
    IsDrawing = False

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
        self._ribbon = RB.RibbonBar(self, wx.ID_ANY, agwStyle=RB.RIBBON_BAR_DEFAULT_STYLE)
        self._bitmap_creation_dc = wx.MemoryDC()
        # color_settings = self._ribbon.GetArtProvider()
        self._ribbon.GetArtProvider().SetColourScheme(wx.Colour(85, 150, 140, 255),
                                                      wx.Colour(255, 50, 40, 255),
                                                      wx.Colour(85, 50, 40, 255))

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Main")
        main_toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "Main Tools", wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        toolbar = RB.RibbonToolBar(main_toolbar_panel)

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

        properties_panel = RB.RibbonPanel(home, wx.ID_ANY, "Properties (Double-click on item to generate)")

        label_font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
        self._bitmap_creation_dc.SetFont(label_font)

        design_tools = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Design", wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 15)))
        import_tools_panel = RB.RibbonPanel(design_tools, wx.ID_ANY, "Import Tools", wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        import_tools = RB.RibbonToolBar(import_tools_panel)
        import_tools.AddTool(ID_IMPORT_CSV, csv_import)

        design_panel = RB.RibbonPanel(design_tools, wx.ID_ANY, "Design Tools", wx.NullBitmap, wx.DefaultPosition,
                                            wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        design_tools = RB.RibbonToolBar(design_panel)
        design_tools.AddTool(wx.ID_ANY, draw_settings)
        design_tools.AddTool(ID_DRAW, draw_tool, kind=RB.RIBBON_BUTTON_TOGGLE)
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
        import_tools.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.import_csv_button, id=ID_IMPORT_CSV)
        toolbar.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.canvas.clear_canvas,  id=ID_CLEAR_ALL)
        design_tools.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.check, id=ID_DRAW)

    def check(self, evt):
        if not self.IsDrawing:
            RibbonFrame.IsDrawing = True
            pub.sendMessage("update_info_label", info="Let's draw something nice!")
        else:
            RibbonFrame.IsDrawing = False
            pub.sendMessage("update_info_label", info='Nothing is going on.....')

    def import_csv_button(self, evt):
        ImportCsvDialog()


class Canvas(wx.Panel):
    all_data_on_canvas = []
    temp_drawing_coords = []

    def __init__(self, parent):
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
        self.coordinates = (0, 0)
        canvas_sizer.Add(self.NC, 4, flag=wx.EXPAND, border=10)
        self.SetSizer(canvas_sizer)

    def clear_canvas(self, evt):
        self.main_canvas.ClearAll(evt)
        Canvas.all_data_on_canvas = []
        self.temp_drawing_coords = []
        self.main_canvas.ZoomToBB(NewBB=None, DrawFlag=True)

    def draw_data_on_canvas(self, import_instance, data_dict):
        [self.main_canvas.AddObject(x) for x in import_instance.prepare_data_to_draw_in_canvas(
            FloatCanvas.Line, data_dict['color'], data_dict['style'], data_dict['width'])]

        self.main_canvas.ZoomToBB(NewBB=None, DrawFlag=True)
        self.main_canvas.Draw()
        Canvas.all_data_on_canvas.append(data_dict)

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
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        if RibbonFrame.IsDrawing:
            pub.sendMessage("update_info_label", info="Let's draw something nice!")
        else:
            pub.sendMessage("update_info_label", info='Nothing is going on.....')

    def dragging(self, evt):
        self.coordinates = evt.Coords
        pub.sendMessage("update_coordinates", updated_coordinates=self.coordinates)

        if evt.Dragging() and evt.MiddleIsDown():
            self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
            self.main_canvas.MoveImage((self.initial_coordinates - evt.GetPosition()), 'Pixel')
            self.initial_coordinates = evt.GetPosition()
            pub.sendMessage("update_info_label", info='Dragging...')

    def drawing(self, evt):
        if RibbonFrame.IsDrawing:
            temp_drawing = FloatCanvas.Point(evt.Coords, Diameter=3)
            Canvas.temp_drawing_coords.append(evt.Coords)
            if len(self.temp_drawing_coords) > 1:
                temp_line_drawing = FloatCanvas.Line(Canvas.temp_drawing_coords)
                self.main_canvas.AddObject(temp_line_drawing)
            self.main_canvas.AddObject(temp_drawing)
            self.main_canvas.Draw(True)


class MainCsvImportPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        myCursor = wx.Cursor('Source/bitmaps/base_cursore.cur', type=wx.BITMAP_TYPE_CUR)
        self.SetCursor(myCursor)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        file_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_report_open = wx.Button(self, label='Выбрать файл', size=(-1, -1))
        button_report_open.Bind(wx.EVT_BUTTON, self.open_report_file_to_write)
        self.data_to_import_name = wx.TextCtrl(self)
        file_sizer.Add(self.data_to_import_name, proportion=4, flag=wx.RIGHT | wx.TOP | wx.ALIGN_CENTER, border=5)
        file_sizer.Add(button_report_open, proportion=1, flag=wx.TOP | wx.ALIGN_CENTER, border=5)

        object_id_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.object_id_field = wx.ComboBox(self, wx.ID_ANY)
        self.object_id = wx.TextCtrl(self, size=(50, -1))
        object_id_label = wx.StaticText(self, label='Field and object ID')
        object_id_sizer.Add(self.object_id_field, proportion=4, flag=wx.RIGHT | wx.TOP | wx.ALIGN_CENTER, border=5)
        object_id_sizer.Add(self.object_id, proportion=-1, flag=wx.TOP | wx.RIGHT | wx.ALIGN_CENTER, border=5)
        object_id_sizer.Add(object_id_label, proportion=-1, flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, border=5)

        x_coordinate_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.object_x_field = wx.ComboBox(self, wx.ID_ANY)
        object_x_label = wx.StaticText(self, label='X coordinate field')
        x_coordinate_sizer.Add(self.object_x_field, proportion=4, flag=wx.RIGHT | wx.TOP | wx.ALIGN_CENTER, border=5)
        x_coordinate_sizer.Add(object_x_label, proportion=1, flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, border=5)

        y_coordinate_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.object_y_field = wx.ComboBox(self, wx.ID_ANY)
        object_y_label = wx.StaticText(self, label='Y coordinate field')
        y_coordinate_sizer.Add(self.object_y_field, proportion=4, flag=wx.RIGHT | wx.TOP | wx.ALIGN_CENTER, border=5)
        y_coordinate_sizer.Add(object_y_label, proportion=1, flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, border=5)

        width_slider_sizer = wx.BoxSizer(wx.HORIZONTAL)
        width_slider_label = wx.StaticText(self, label='Choose line width')
        self.width_slider = wx.Slider(self, maxValue=5)
        self.line_color = wx.ColourPickerCtrl(self)
        width_slider_sizer.Add(width_slider_label, 1, flag=wx.RIGHT | wx.TOP | wx.ALIGN_CENTER, border=5)
        width_slider_sizer.Add(self.width_slider, 3,  flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, border=5)
        width_slider_sizer.Add(self.line_color, 1, flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, border=5)
        self.line_type = wx.RadioBox(self, choices=['Solid', 'Dashed', 'Dotted', 'Dash - Dotted'], majorDimension=0)

        bottom_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, label='OK')
        ok_button.Bind(wx.EVT_BUTTON, self.collect_imported_to_canvas)
        cancel_button = wx.Button(self, label='Cancel')
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_pressed)
        bottom_buttons_sizer.Add(ok_button, flag=wx.TOP | wx.ALIGN_CENTER, border=5)
        bottom_buttons_sizer.Add(cancel_button, flag=wx.TOP | wx.LEFT | wx.ALIGN_CENTER, border=5)

        main_sizer.Add(file_sizer, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        main_sizer.Add(object_id_sizer, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        main_sizer.Add(x_coordinate_sizer, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        main_sizer.Add(y_coordinate_sizer, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=15)
        main_sizer.Add(width_slider_sizer, proportion=1, flag=wx.LEFT | wx.RIGHT, border=15)
        main_sizer.Add(self.line_type, proportion=-1, flag=wx.LEFT | wx.RIGHT, border=15)
        main_sizer.Add(bottom_buttons_sizer, proportion=-1, flag=wx.LEFT | wx.BOTTOM | wx.RIGHT | wx.TOP | wx.ALIGN_RIGHT, border=15)

        self.SetSizer(main_sizer)
        self.Layout()

    def open_report_file_to_write(self, evt):
        wildcard = "CSV (*.csv)|*.csv|" \
                   "All files (*.*)|*.*"

        with wx.FileDialog(self, message="Choose a file", defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.data_to_import_name.Clear()
                self.data_to_import_name.WriteText(dlg.GetPath())
                fields_from_file = CsvDataHandler.get_csv_file_fields_static(dlg.GetPath())
                self.object_y_field.Append(fields_from_file)
                self.object_x_field.Append(fields_from_file)
                self.object_id_field.Append(fields_from_file)

    def cancel_pressed(self, evt):
        self.GetParent().Destroy()

    def collect_imported_to_canvas(self, evt):
        imported_csv_data = CsvDataHandler(self.data_to_import_name.GetValue(),
                                           self.object_id_field.GetValue(),
                                           self.object_id.GetValue())

        imported_csv_data.import_csv_data(self.object_x_field.GetValue(),
                                          self.object_y_field.GetValue())
        line_type_selections = {0: 'Solid', 1: 'LongDash', 2: 'Dot', 3: 'DotDash'}
        data_from_import = {'coordinates': imported_csv_data.get_data, 'color': self.line_color.GetColour()[:-1],
                            'width': int(self.width_slider.GetValue()), 'style': line_type_selections[self.line_type.GetSelection()]}
        pub.sendMessage("draw_data_on_canvas", import_instance=imported_csv_data, data_dict=data_from_import)
        self.GetParent().Destroy()


class ImportCsvDialog(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Import CSV')
        self.SetBackgroundColour(wx.Colour(62, 224, 202, 255))
        self.SetSize(430, 400)
        panel = MainCsvImportPanel(self)
        self.Center()
        self.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
