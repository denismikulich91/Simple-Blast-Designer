import wx
import wx.propgrid as wxpg
import os
from csv_settings import CsvDataHandler
from pubsub import pub
from small_dialogs import AddLayerDialog
from lines_and_points import LinesAndPoints


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
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.property_table = wxpg.PropertyGrid(self,
                                               style=wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_TOOLBAR)
        self.property_table.Append(wxpg.PropertyCategory('Current drawing settings', name='drawing'))
        self.property_table.Append(wxpg.ColourProperty(label='Color', name='d_color', value=wx.BLUE))
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
        self.property_table.Append(wxpg.LongStringProperty(label='Comments', name='comment'))
        self.property_table.HideProperty('properties', True)
        sizer.Add(self.property_table, 2, wx.EXPAND, border=10)

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

    @property
    def get_comment(self):
        return self.property_table.GetPropertyValue('comment')

    def set_property_table(self, object_id, object_dict):
        style_dict = {'Solid': 0, 'LongDash': 1, 'Dot': 2, 'DotDash': 3}
        self.property_table.ChangePropertyValue('id', object_id)
        self.property_table.ChangePropertyValue('coordinates', str(object_dict['coordinates']))
        self.property_table.ChangePropertyValue('length', object_dict['2d_length'])
        self.property_table.ChangePropertyValue('area', object_dict['area'])
        self.property_table.ChangePropertyValue('closed', object_dict['closed'])
        self.property_table.ChangePropertyValue('color', object_dict['color'])
        self.property_table.ChangePropertyValue('style', style_dict[object_dict['style']])
        self.property_table.ChangePropertyValue('width', object_dict['width'])
        self.property_table.ChangePropertyValue('comment', object_dict['comment'])

class LayerManager(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        new_layer = wx.Bitmap('Source/bitmaps/new_layer.png')
        self.lock_layer = wx.Bitmap('Source/bitmaps/lock_layer.png')
        self.unlock_layer = wx.Bitmap('Source/bitmaps/unlock_layer.png')
        self.bulp_off = wx.Bitmap('Source/bitmaps/bulp_off.png')
        self.bulp_on = wx.Bitmap('Source/bitmaps/bulp_on.png')
        delete_layer = wx.Bitmap('Source/bitmaps/delete_layer.png')

        self.font = wx.Font(wx.FontInfo(10).Bold(True))
        self.initial_font = wx.Font(wx.FontInfo(9).Bold(False))

        self.layer_states = {'temp_layer': {'locked': False, 'hidden': False}}
        self.active_layer = 'temp_layer'

        self.SetBackgroundColour((200, 200, 200))

        layer_manager_sizer = wx.BoxSizer(wx.VERTICAL)
        layer_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.layer_box = wx.ListBox(self, choices=list(self.layer_states.keys()), style=wx.LB_OWNERDRAW)
        self.layer_label = wx.StaticText(self, label=f'Active:   {self.active_layer}')
        layer_buttons_sizer.Add(self.layer_label, 5, wx.ALIGN_CENTER | wx.LEFT, border=5)
        self.layer_box.Bind(wx.EVT_LISTBOX_DCLICK, self.set_active_layer)
        self.layer_box.Bind(wx.EVT_LISTBOX, self.get_layer_states)
        self.layer_box.SetItemBackgroundColour(0, 'Green')
        self.layer_box.SetItemFont(0, self.font)

        new_layer_button = wx.Button(self, size=(30, 30))
        new_layer_button.SetBitmap(wx.BitmapBundle(new_layer))
        self.Bind(wx.EVT_BUTTON, self.add_new_layer, new_layer_button)
        layer_buttons_sizer.Add(new_layer_button, 1, wx.ALIGN_CENTER, border=0)

        self.hide_layer_button = wx.ToggleButton(self, size=(30, 30))
        self.hide_layer_button.SetBitmap(wx.BitmapBundle(self.bulp_on))
        self.hide_layer_button.SetValue(True)
        self.hide_layer_button.SetBackgroundColour((234, 244, 166))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.hide_show_layer, self.hide_layer_button)
        layer_buttons_sizer.Add(self.hide_layer_button, 1, wx.ALIGN_CENTER, border=0)

        self.lock_layer_button = wx.ToggleButton(self, size=(30, 30))
        self.lock_layer_button.SetBitmap(wx.BitmapBundle(self.unlock_layer))
        self.Bind(wx.EVT_TOGGLEBUTTON, self.lock_show_layer, self.lock_layer_button)
        layer_buttons_sizer.Add(self.lock_layer_button, 1, wx.ALIGN_CENTER, border=0)

        delete_layer_button = wx.Button(self, size=(30, 30))
        delete_layer_button.SetBitmap(wx.BitmapBundle(delete_layer))
        self.Bind(wx.EVT_BUTTON, self.delete_layer, delete_layer_button)
        layer_buttons_sizer.Add(delete_layer_button, 1, wx.ALIGN_CENTER, border=0)

        layer_manager_sizer.Add(layer_buttons_sizer, 1, wx.EXPAND, 0)
        layer_manager_sizer.Add(self.layer_box, 6, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(layer_manager_sizer)

    def hide_show_layer(self, evt):
        selected_layer = self.layer_box.GetString(self.layer_box.GetSelection())
        if evt.GetSelection() == 1:
            self.hide_layer_button.SetBackgroundColour((234, 244, 166))
            self.hide_layer_button.SetBitmap(wx.BitmapBundle(self.bulp_on))
            self.layer_states[selected_layer]['hidden'] = False
            # self.show_data_on_canvas(self.layer_box.GetSelection())
            pub.sendMessage("hide_show_layer", layer=selected_layer, state=False, delete=False)
        else:
            self.hide_layer_button.SetBackgroundColour((225, 225, 225))
            self.hide_layer_button.SetBitmap(wx.BitmapBundle(self.bulp_off))
            self.layer_states[selected_layer]['hidden'] = True
            # self.hide_data_on_canvas(self.layer_box.GetSelection())
            pub.sendMessage("hide_show_layer", layer=selected_layer, state=True, delete=False)
        print(self.layer_states)
        evt.Skip()

    def lock_show_layer(self, evt):
        if evt.GetSelection() == 1:
            self.lock_layer_button.SetBitmap(wx.BitmapBundle(self.lock_layer))
            self.layer_states[self.layer_box.GetString(self.layer_box.GetSelection())]['locked'] = True
        else:
            self.lock_layer_button.SetBitmap(wx.BitmapBundle(self.unlock_layer))
            self.layer_states[self.layer_box.GetString(self.layer_box.GetSelection())]['locked'] = False
        print(self.layer_states)

    def add_new_layer(self, evt):
        AddLayerDialog(None, self.layer_box, self.layer_states)

    def delete_layer(self, evt):  # TODO: Add active layer deletion handler
        layer = self.layer_box.GetString(self.layer_box.GetSelection())
        if self.layer_box.GetCount() <= 1:
            dlg = wx.MessageDialog(self, f'You need at least one layer!', 'Warning',
                                   wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
        else:
            dlg = wx.MessageDialog(self, f'Delete this layer? \n{layer}', 'Are you sure?',
                                   wx.YES_NO | wx.ICON_EXCLAMATION)

            if dlg.ShowModal() == wx.ID_YES:
                self.layer_states.pop(self.layer_box.GetString(self.layer_box.GetSelection()))
                self.layer_box.Set(list(self.layer_states.keys()))
                pub.sendMessage("update_info_label", info=f'Layer {layer} has been deleted')
                pub.sendMessage("hide_show_layer", layer=layer, state=True, delete=True)
                if layer == self.active_layer:
                    self.layer_label.SetLabel(f'Active:   {self.layer_box.GetString(0)}')
                    self.layer_box.SetItemBackgroundColour(0, 'Green')
                    self.layer_box.SetItemFont(0, self.font)
                    self.active_layer = self.layer_box.GetString(0)
                    print(self.get_active_layer)

    def set_active_layer(self, evt):
        item = evt.GetSelection()
        for line in range(self.layer_box.GetCount()):
            self.layer_box.SetItemBackgroundColour(line, (225, 225, 225))
            self.layer_box.SetItemFont(line, self.initial_font)

        self.active_layer = self.layer_box.GetString(item)
        self.layer_label.SetLabel(f'Active:   {self.active_layer}')
        self.layer_box.SetItemBackgroundColour(item, 'Green')
        self.layer_box.SetItemFont(item, self.font)

        # TODO: find the way to update colors and fonts of the listbox without selection iteration
        for line in range(self.layer_box.GetCount()):
            self.layer_box.SetSelection(line)
        self.layer_box.SetSelection(item)

    def get_layer_states(self, evt):
        item = evt.GetSelection()
        if self.layer_states[self.layer_box.GetString(item)]['locked']:
            self.lock_layer_button.SetValue(1)
            self.lock_layer_button.SetBitmap(wx.BitmapBundle(self.lock_layer))
        else:
            self.lock_layer_button.SetValue(0)
            self.lock_layer_button.SetBitmap(wx.BitmapBundle(self.unlock_layer))

        if self.layer_states[self.layer_box.GetString(item)]['hidden']:
            self.hide_layer_button.SetValue(0)
            self.hide_layer_button.SetBitmap(wx.BitmapBundle(self.bulp_off))
            self.hide_layer_button.SetBackgroundColour((225, 225, 225))
        else:
            self.hide_layer_button.SetValue(1)
            self.hide_layer_button.SetBitmap(wx.BitmapBundle(self.bulp_on))
            self.hide_layer_button.SetBackgroundColour((234, 244, 166))

    @property
    def get_active_layer(self):
        return self.active_layer

    def get_layer_state(self, layer):
        return self.layer_states[layer]

    def clear_all(self):
        self.layer_box.Set(['temp_layer'])
        self.layer_states = {'temp_layer': {'locked': False, 'hidden': False}}
        self.active_layer = 'temp_layer'
        self.layer_box.SetItemBackgroundColour(0, 'Green')
        self.layer_box.SetItemFont(0, self.font)





















