import wx
from side_dialogs import LayerManager


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simple Blast Designer')
        self.SetSize(1300, 800)
        self.SetBackgroundColour(wx.Colour(85, 150, 140, 255))
        self.Center()
        self.main_panel = MainPanel(self)

        self.Show()

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetSize(200,300)
        # self.manager = LayerManager(self)
        self.listbox = TestListBox(self)
        # self.manager.Fit()
        self.listbox.Fit()



import wx

#---------------------------------------------------------------------------

# This listbox subclass lets you type the starting letters of what you want to
# select, and scrolls the list to the match if it is found.



#---------------------------------------------------------------------------

class TestListBox(wx.Panel):
    def __init__(self, parent,):
        wx.Panel.__init__(self, parent, -1)

        sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
                      'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
                      'twelve', 'thirteen', 'fourteen']

        wx.StaticText(self, -1, "This example uses the wx.ListBox control.", (45, 10))
        wx.StaticText(self, -1, "Select one:", (15, 50))
        self.lb1 = wx.ListBox(self, 60, (100, 50), (90, 120), sampleList, wx.LB_SINGLE|wx.LB_OWNERDRAW)
        self.Bind(wx.EVT_LISTBOX, self.EvtListBox, self.lb1)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.EvtListBoxDClick, self.lb1)
        self.lb1.Bind(wx.EVT_RIGHT_UP, self.EvtRightButton)
        self.lb1.SetSelection(3)
        self.lb1.Append("with data", "This one has data")
        self.lb1.SetClientData(2, "This one has data")

        # These only work on Windows
        self.lb1.SetItemBackgroundColour(1, "yellow")
        self.lb1.SetItemForegroundColour(2, "red")

        wx.StaticText(self, -1, "Select many:", (220, 50))
        self.lb2 = wx.ListBox(self, 70, (320, 50), (90, 120), sampleList, wx.LB_EXTENDED)
        self.Bind(wx.EVT_LISTBOX, self.EvtMultiListBox, self.lb2)
        self.lb2.Bind(wx.EVT_RIGHT_UP, self.EvtRightButton)
        self.lb2.SetSelection(0)

        sampleList = sampleList + ['test a', 'test aa', 'test aab',
                                   'test ab', 'test abc', 'test abcc',
                                   'test abcd' ]
        sampleList.sort()
        wx.StaticText(self, -1, "Find Prefix:", (15, 250))



    def EvtListBox(self, event):


        lb = event.GetEventObject()
        # data = lb.GetClientData(lb.GetSelection())

        # if data is not None:
            # self.log.WriteText('\tdata: %s\n' % data)

    def EvtListBoxDClick(self, event):

        self.lb1.Delete(self.lb1.GetSelection())

    def EvtMultiListBox(self, event):
        pass


    def EvtRightButton(self, event):
        if event.GetEventObject().GetId() == 70:
            selections = list(self.lb2.GetSelections())
            selections.reverse()

            for index in selections:
                self.lb2.Delete(index)



if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()

