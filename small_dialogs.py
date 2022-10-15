import wx


class AddLayerDialog(wx.Dialog):
    def __init__(self, parent, layer_box, layer_dict):
        super().__init__(parent)
        self.SetSize((200, 130))
        self.Center()

        self.layer_states = layer_dict
        self.layer_box = layer_box
        self.SetBackgroundColour(wx.Colour(62, 224, 202, 255))
        text = wx.StaticText(self, label='Enter new layer name')
        self.name_enter_field = wx.TextCtrl(self, size=(170, -1))
        self.button = wx.Button(self, label='OK', size=(70,20))
        self.button.Bind(wx.EVT_BUTTON, self.add_layer)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([
            (text, 1, wx.ALIGN_CENTER | wx.ALL, 5),
            (self.name_enter_field, 2, wx.ALIGN_CENTER | wx.ALL, 5),
            (self.button, 2, wx.ALIGN_CENTER | wx.ALL, 5)
        ])
        self.SetSizer(sizer)
        self.Show()

    def add_layer(self, evt):
        if self.name_enter_field.GetValue() not in self.layer_states:
            self.layer_box.Append(self.name_enter_field.GetValue())
            self.layer_states[self.name_enter_field.GetValue()] = {'locked': False, 'hidden': False}
            self.Destroy()
        else:
            dlg = wx.MessageDialog(self, f'{self.name_enter_field.GetValue()} is already exist', 'Layer exists',
                                   wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()


