
pub.subscribe(self.update_info_label_via_pubsub, "update_info_label")

def update_info_label_via_pubsub(self, info):
    self.info_label.SetLabel(info)


def update_cursor(self, evt):
    self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
    pub.sendMessage("update_info_label", info='Nothing is going on.....')


