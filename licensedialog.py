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

from mcbuzzer import resource_path

class LicenseFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        """Create the DemoFrame."""
        wx.Frame.__init__(self, *args, **kwargs)
        self.SetTitle("MCbuzzer License")
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        tc = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE|wx.TE_READONLY)
        tc.LoadFile(resource_path( "resources/LICENSE.txt"),
                    fileType=wx.TEXT_TYPE_ANY)
        sizer.Add(tc, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        

