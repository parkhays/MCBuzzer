# MCbuzzer MATHCOUNTS Countdown Round Tool
# Copyright (C) 2020 Park Hays

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import wx
from gdata import dat

class BuzzerConfigPanel(wx.Panel):
    """This Panel holds the widgets to configure the keystrokes used on the buzzers."""
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.contestantAKey = wx.TextCtrl(self, size=(140, -1))
        self.contestantBKey = wx.TextCtrl(self, size=(140, -1))

        # we're using .lower() to make it appear as though the
        # interface uses lowercase letters, in the interest of
        # user-friendliness.
        self.contestantAKey.SetValue(str(dat.getKeycodes()[0] or '').lower())
        self.contestantBKey.SetValue(str(dat.getKeycodes()[1] or '').lower())
        
        self.finishButton = wx.Button(self, label='Finish')
        
        self.sizer = wx.GridBagSizer(4, 3)
        self.sizer.Add(wx.StaticText(self, label="Contestant A Key:"), (0, 0))
        self.sizer.Add(wx.StaticText(self, label="Contestant B Key:"), (0, 1))
        self.sizer.Add(self.contestantAKey, (1, 0))
        self.sizer.Add(self.contestantBKey, (1, 1))

        self.sizer.Add(self.finishButton, pos=(2, 0), span=(1,2), flag=wx.EXPAND)

        self.SetSizerAndFit(self.sizer)

    def updateFont(self, event):
        initialSize = dat.nameFontSize
        try:
            dat.nameFontSize = int( self.fontSizeSpinBox.GetValue())
        except:
            print("problem in getting font")

        if initialSize != dat.nameFontSize:
            self.parent.parent.treePanel.updateTree()
        
class BuzzerConfigFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        """Create the DemoFrame."""
        wx.Frame.__init__(self, *args, **kwargs)

        # Add the Widget Panel
        self.Panel = BuzzerConfigPanel(self)
        self.Panel.finishButton.Bind(wx.EVT_BUTTON, self.finishAndUpdate)
        self.Fit()

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap('resources/main_logo1.ico', wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        
    def finishAndUpdate(self, event):
        dat.setKeycodes(self.Panel.contestantAKey.GetValue(), self.Panel.contestantBKey.GetValue())
        print('set keycodes')
        print(dat.buzzerConfig)
        self.OnQuit()
        
    def OnQuit(self, event=None):
        """Exit application."""
        self.Close()

