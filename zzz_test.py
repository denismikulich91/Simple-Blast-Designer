import wx

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simple Blast Designer')
        self.SetSize(1200, 800)
        main_panel = MainPanel(self)
        self.Show()
        self.Maximize(True)


class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        canvas_sizer = wx.BoxSizer(wx.VERTICAL)

        status_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        x_label = wx.StaticText(self, label='X:')
        status_panel_sizer.Add(x_label, flag=wx.ALL | wx.ALIGN_LEFT, border=10)

        x_entry = wx.TextCtrl(self, value='kkk')
        status_panel_sizer.Add(x_entry, 1, flag=wx.ALL | wx.ALIGN_LEFT, border=10)

        y_label = wx.StaticText(self, label='Y:')
        status_panel_sizer.Add(y_label, 1, flag=wx.ALL | wx.ALIGN_LEFT, border=10)

        y_entry = wx.TextCtrl(self, value='lll')
        status_panel_sizer.Add(y_entry, 1, flag=wx.ALL | wx.ALIGN_LEFT, border=10)

        z_label = wx.StaticText(self, label='Z:')
        status_panel_sizer.Add(z_label, 1, flag=wx.ALL | wx.ALIGN_LEFT, border=10)

        z_entry = wx.TextCtrl(self, value='0')
        status_panel_sizer.Add(z_entry, 1, flag=wx.ALL | wx.ALIGN_LEFT, border=10)



        canvas_sizer.Add(status_panel_sizer, 1, flag=wx.ALL| wx.BOTTOM, border=10)
        self.SetSizer(canvas_sizer)
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()