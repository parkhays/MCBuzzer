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
import os

class PrimaryFrame(wx.Frame):
    """Main Frame holding the Panel."""
    def __init__(self, *args, **kwargs):
        """Create the DemoFrame."""
        wx.Frame.__init__(self, *args, **kwargs)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer( self.Sizer)
        self.Btn = wx.Button(self, label="OK")
        self.Btn.Bind(wx.EVT_BUTTON, self.updateButton )
        self.Sizer.Add( self.Btn)

    def updateButton(self, event=None):
        self.Btn.SetLabel("A Very Long Button Text Entry")
        self.Btn.Fit()

if __name__ == "__main__":
    app = wx.App(False)
    frame = PrimaryFrame(None, wx.ID_ANY, "MATHCOUNTS")
    frame.Show(True)
    app.MainLoop()
