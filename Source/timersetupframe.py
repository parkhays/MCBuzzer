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

class TimerSetupPanel(wx.Panel):
    """This Panel holds the widgets to configure the times used for the countdown."""
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.questionTimerCtrl = wx.TextCtrl(self, size=(140, -1))
        self.answerTimerCtrl = wx.TextCtrl(self, size=(140, -1))

        self.questionTimerCtrl.SetValue(str(dat.questionTimer))
        self.answerTimerCtrl.SetValue(str(dat.answerTimer))
        
        self.finishButton = wx.Button(self, label='Finish')
        
        self.sizer = wx.GridBagSizer(3, 3)
        self.sizer.Add(wx.StaticText(self, label="Question Timer:"), (0, 0))
        self.sizer.Add(wx.StaticText(self, label="Answer Timer:"), (0, 1))
        self.sizer.Add(self.questionTimerCtrl, (1, 0))
        self.sizer.Add(self.answerTimerCtrl, (1, 1))

        self.sizer.Add(self.finishButton, pos=(2, 0), span=(1,2), flag=wx.EXPAND)

        self.SetSizerAndFit(self.sizer)

class TimerSetupFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        """Create the DemoFrame."""
        wx.Frame.__init__(self, *args, **kwargs)

        # Add the Widget Panel
        self.Panel = TimerSetupPanel(self)
        self.Panel.finishButton.Bind(wx.EVT_BUTTON, self.finishAndUpdate)
        self.Fit()

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap('resources/main_logo1.ico', wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        
    def finishAndUpdate(self, event):
        dat.questionTimer = int(self.Panel.questionTimerCtrl.GetValue())
        dat.answerTimer = int(self.Panel.answerTimerCtrl.GetValue())
        self.OnQuit()
        
    def OnQuit(self, event=None):
        """Exit application."""
        self.Close()

