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

"""Main application for the MCbuzzer MathCounts Countdown
code. Designed to work with buzzers that behave like a keystroke.

"""

import wx
import os
import sys

from gdata import dat
import competitorGrid
from treepanel import TreePanel
import contestframe
import buzzersetupframe
import timersetupframe
import licensedialog
import aboutdialog

from resource import resource_path

class BuzzerTest(wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        wx.Dialog.__init__(self, parent, *args, **kwargs)
        
class MCBuzzer(wx.Frame):
    """Main Frame holding the Panel."""
    def __init__(self, *args, **kwargs):
        """Create the DemoFrame."""
        wx.Frame.__init__(self, *args, **kwargs)
        
        self.font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        OptionsMenu = wx.Menu()
        ContestMenu = wx.Menu()
        AboutMenu = wx.Menu()
        
        item = FileMenu.Append(wx.ID_OPEN, "&Open")
        self.Bind(wx.EVT_MENU, self.Open, item)
        
        item = FileMenu.Append(wx.ID_SAVE, "&Save")
        self.Bind(wx.EVT_MENU, self.Save, item)

        item = FileMenu.Append(wx.ID_SAVEAS, "Save &As")
        self.Bind(wx.EVT_MENU, self.OnSaveAs, item)

        item = FileMenu.Append(wx.ID_EXIT, "&Quit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)


        item = OptionsMenu.Append(wx.ID_PREFERENCES, "Setup &Buzzer")
        self.Bind(wx.EVT_MENU, self.OnBuzzerSetup, item)

        item = OptionsMenu.Append(wx.ID_ANY, "Setup &Timer")
        self.Bind(wx.EVT_MENU, self.OnTimerSetup, item)


        item = ContestMenu.Append(wx.ID_REPLACE, "Contestant &List")
        self.Bind(wx.EVT_MENU, self.editContestants, item)

        item = ContestMenu.Append(wx.ID_REFRESH, "&Update Tree")
        self.Bind(wx.EVT_MENU, self.updateTree, item)

        item = AboutMenu.Append(wx.ID_ANY, "&About")
        self.Bind(wx.EVT_MENU, self.About, item)

        item = AboutMenu.Append(wx.ID_ANY, "&License")
        self.Bind(wx.EVT_MENU, self.License, item)

        MenuBar.Append(FileMenu, '&File')
        MenuBar.Append(ContestMenu, '&Contest')
        MenuBar.Append(OptionsMenu, '&Options')
        MenuBar.Append(AboutMenu, '&Help')
        
        self.SetMenuBar(MenuBar)

        stack = wx.BoxSizer(wx.VERTICAL)
        
        self.setTree(None)

        # Load the image
        img = wx.Image(resource_path('resources/main_banner.jpg'), wx.BITMAP_TYPE_ANY)
        scale = 0.3
        img.Rescale(scale*img.GetWidth(), scale*img.GetHeight(), wx.IMAGE_QUALITY_HIGH)
        self.bannerBmp = img.ConvertToBitmap()
        self.banner = wx.StaticBitmap(self, wx.ID_ANY, self.bannerBmp)
        stack.Add(self.banner, flag=wx.ALIGN_CENTER)
        stack.Add(self.treePanel, flag=wx.EXPAND|wx.ALL)

        stack.SetSizeHints(self)
        self.SetSizer(stack)

    def updateTree(self, event=None):
        """Updates the tree display based on the data currently in the data structure."""
        self.treePanel.updateTree()
        
    def setTree(self, event=None):
        self.treePanel = TreePanel(self)
        self.treePanel.Refresh()
        self.Layout()

    def OnBuzzerSetup(self, event):
        buzzerConfigFrame = buzzersetupframe.BuzzerConfigFrame(None, title="Set Buzzer Keys")
        buzzerConfigFrame.Show(True)

    def OnTimerSetup(self, event):
        timerSetupFrame = timersetupframe.TimerSetupFrame(None, title="Set Timer Lengths")
        timerSetupFrame.Show(True)
        
    def Save(self, event):
        if dat.fileName is None:
            print("Save dat.fileName", dat.fileName)
            self.OnSaveAs(event)
            
        else:
            print("Saving to already-set filename", dat.fileName)
            dat.saveToFile()
            
    def OnSaveAs(self, event):
        with wx.FileDialog(self, "Save pkl file", wildcard="Pickle files (*.pkl)|*.pkl",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            print("OnSaveAs pathname", pathname)
            try:
                dat.saveToFile( fn=pathname)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

        
    def Open(self, event):
        with wx.FileDialog(self, "Open pkl file", wildcard="Pickle files (*.pkl)|*.pkl",
                           style=wx.FD_OPEN) as fileDialog:
            
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            print("Open Got a pathname", pathname)
            try:
                dat.open( fn=pathname)
                dat.fileName = pathname
                print("Open...", dat.fileName)
            except IOError:
                wx.LogError("Cannot open or read current data in file '%s'." % pathname)

        self.updateTree()
        
    def OnQuit(self, event=None):
        """Exit application."""
        self.Close()
        
    def editContestants(self, event=None):
        competitorFrame = competitorGrid.CompetitorFrame(None, title="Competitor Entry", style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        competitorFrame.Show(True)

    def About(self, event=None):
        ad = aboutdialog.AboutFrame(self)
        ad.Show()
    
    def License(self, event=None):
        ld = licensedialog.LicenseFrame(self)
        ld.Show()
        
if __name__ == "__main__":
    app = wx.App(False)
    frame = MCBuzzer(None, wx.ID_ANY, "MATHCOUNTS")
    frame.Show(True)
    app.MainLoop()
