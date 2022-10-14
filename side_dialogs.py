import wx
import wx.propgrid as wxpg
import os
from csv_settings import CsvDataHandler
from pubsub import pub


class ImportCsvDialog(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Import CSV')
        self.SetBackgroundColour(wx.Colour(62, 224, 202, 255))
        self.SetSize(430, 400)
        self.panel = MainCsvImportPanel(self)
        self.Center()
        self.Show()


class MainCsvImportPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        myCursor = wx.Cursor('Source/bitmaps/base_cursor.cur', type=wx.BITMAP_TYPE_CUR)
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
        main_sizer.Add(bottom_buttons_sizer, proportion=-1,
                       flag=wx.LEFT | wx.BOTTOM | wx.RIGHT | wx.TOP | wx.ALIGN_RIGHT, border=15)

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
        data_from_import = {'coordinates': imported_csv_data.get_data,
                            'color': self.line_color.GetColour()[:-1],
                            'width': int(self.width_slider.GetValue()),
                            'style': line_type_selections[self.line_type.GetSelection()]}

        pub.sendMessage("draw_data_on_canvas", import_instance=imported_csv_data, data_dict=data_from_import)
        self.GetParent().Destroy()


class LayersAndProperties(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour((200, 200, 200))
        sizer = wx.BoxSizer()
        self.property_table = wxpg.PropertyGrid(self,
                                               style=wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_TOOLBAR)
        self.property_table.Append(wxpg.PropertyCategory('Current drawing settings', name='drawing'))
        self.property_table.Append(wxpg.ColourProperty(label='Color', name='d_color', value=wx.BLACK))
        self.property_table.Append(wxpg.EnumProperty(label='Style', labels=['Solid', 'Dashed', 'Dotted', 'Dash-Dotted'],
                                                     name='d_style', values=[0, 1, 2, 3]))
        self.property_table.Append(wxpg.EnumProperty(label='Width', labels=['Thin', 'Not so thin', 'Rather thick', 'Rather fat', 'Fat'],
                                                     name='d_width', values=[0, 1, 2, 3, 4], value=0))

        self.property_table.Append(wxpg.PropertyCategory('Object properties', name='properties'))
        self.property_table.Append(wxpg.IntProperty(label='Object ID', name='id'))
        self.property_table.Append(wxpg.LongStringProperty(label='Coordinates', name='coordinates'))
        self.property_table.Append(wxpg.FloatProperty(label='2D Length', name='length'))
        self.property_table.Append(wxpg.FloatProperty(label='2D Area', name='area'))
        self.property_table.Append(wxpg.BoolProperty(label='Closed', name='closed'))
        self.property_table.SetPropertyAttribute("closed", "UseCheckbox", True)
        color = wxpg.ColourProperty(label='Color', name='color', value=wx.BLACK)
        color.GetEditorDialog()
        self.property_table.Append(color)
        self.property_table.Append(wxpg.EnumProperty(label='Style', labels=['Solid', 'Dashed', 'Dotted', 'Dash-Dotted'],
                                                     name='style', values=[0, 1, 2, 3]))
        self.property_table.Append(
            wxpg.EnumProperty(label='Width', labels=['Thin', 'Not so thin', 'Rather thick', 'Rather fat', 'Fat'],
                              name='width', values=[0, 1, 2, 3, 4], value=0))
        self.property_table.Append(wxpg.LongStringProperty(label='Comments', name='comments'))
        self.property_table.HideProperty('properties', True)
        sizer.Add(self.property_table, 1, wx.EXPAND, border=10)
        self.SetSizer(sizer)

    def show_properties(self, show: bool) -> None:
        self.property_table.HideProperty('properties', show)

    @property
    def get_color(self):
        return self.property_table.GetPropertyValue('d_color')[:-1]

    @property
    def get_style(self):
        style_dict = {0: 'Solid', 1: 'LongDash', 2: 'Dot', 3: 'DotDash'}
        return style_dict[self.property_table.GetPropertyValue('d_style')]

    @property
    def get_width(self):
        return int(self.property_table.GetPropertyValue('d_width'))

