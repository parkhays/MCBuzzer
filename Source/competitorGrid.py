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

import wx, wx.grid
from gdata import dat
import competitor

from resource import resource_path

class CompetitorPanel(wx.Panel):
    """This Panel holds the competitor grid display and an 'OK' button"""
    
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.parent = parent 
        
        OKBtn = wx.Button(self, label="Finish")
        OKBtn.Bind(wx.EVT_BUTTON, self.SetListAndClose )

        OKAndInitializeBtn = wx.Button(self, label="Accept and Initialize")
        OKAndInitializeBtn.Bind(wx.EVT_BUTTON, self.SetListAndInitializeTree)
        # Create a wxGrid object
        grid = wx.grid.Grid(self, -1)
        self.grid = grid
        
        # Then we call CreateGrid to set the dimensions of the grid
        grid.CreateGrid(16, 2)

        # We can set the sizes of individual rows and columns
        # in pixels
        grid.SetColSize(0, 220)
        grid.SetColSize(1, 220)
       
        # And set grid cell contents as strings
        grid.SetColLabelValue(0, 'Student Name')
        grid.SetColLabelValue(1, 'School')

        if dat.competitorList is not None:
            for i,comp in enumerate(dat.competitorList):
                grid.SetCellValue(i, 0, comp.name)
                grid.SetCellValue(i, 1, comp.school)
        
        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(OKBtn, 0, wx.EXPAND|wx.ALL, 5)
        Sizer.Add(OKAndInitializeBtn, 0, wx.EXPAND|wx.ALL, 5)
        Sizer.Add(grid, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizerAndFit(Sizer)

    def SetList(self):
        # Convert the grid to a list of competitors
        z = [competitor.Competitor(
            self.grid.GetCellValue(i, 0),
            self.grid.GetCellValue(i, 1))
             for i in range(16)]
        dat.competitorList = z
        
    def SetListAndClose(self, event=None):
        self.SetList()
        dat.setContestState()
        self.parent.Close()
        
    def SetListAndInitializeTree(self, event=None):
        self.SetList()
        dat.setContestState(shuffle=True)
        self.parent.Close()
        
class CompetitorFrame(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        """Create the DemoFrame."""
        wx.Frame.__init__(self, *args, **kwargs)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(
            resource_path('resources/main_logo1.ico'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        # Add the Widget Panel
        self.Panel = CompetitorPanel(self)

        self.Fit()

    def OnQuit(self, event=None):
        """Exit application."""
        self.Close()
