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

class FontSizeFrame(wx.Frame):
    """Frame for setting the font size of the name buttons in the TreePanel.
    """
    def __init__(self, parent, *args, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.fontSizeSpinBox = wx.SpinCtrl(self)
        self.fontSizeSpinBox.SetValue( dat.nameFontSize)
        self.fontSizeSpinBox.Bind(wx.EVT_SPINCTRL, self.updateTestFont)
        self.fontSizeTest = wx.StaticText(self, label='Test')
        
        self.finishButton = wx.Button(self, label='Finish')
        self.finishButton.Bind(wx.EVT_BUTTON, self.finish)

        self.font = wx.Font(dat.nameFontSize, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.fontSizeTest.SetFont(self.font)
        
        self.sizer = wx.GridBagSizer(3, 1)
        self.sizer.Add(self.fontSizeTest, (0, 0))
        self.sizer.Add(self.fontSizeSpinBox, (1, 0))
        self.sizer.Add(self.finishButton, pos=(2, 0), flag=wx.EXPAND)

        self.SetSizerAndFit(self.sizer)

        self.initialFontSize = dat.nameFontSize

        self.Layout()
        self.SetAutoLayout( True)

    def updateTestFont(self, event):
        self.font.SetPointSize(self.fontSizeSpinBox.GetValue())
        self.fontSizeTest.SetFont(self.font)
        self.fontSizeTest.SetLabel('Test')
        self.Fit()
        
    def finish(self, event):
        """Compares the font set in the widget to the previous setting, and if
        it is different, update all the buttons.

        """
        try:
            dat.nameFontSize = int( self.fontSizeSpinBox.GetValue())
        except:
            print("problem in getting font")

        if self.initialFontSize != dat.nameFontSize:
            self.parent.treePanel.updateTree()
            self.parent.treePanel.Layout()
            
        self.Close()

