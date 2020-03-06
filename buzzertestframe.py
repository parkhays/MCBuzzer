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

from gdata import dat
import contest

class BuzzerTestFrame(wx.Frame):
    def __init__(self, parent, *args, tier=None, pairing=None, **kwargs):
        """Contest frame creation
        
        kwargs:
        -----
        tier
        pairing
        """
        wx.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.bigFont = wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )        

        ctst = dat.getContestByTierAndPairing( tier, pairing)

        self.compIdx = 0
        self.comps = [(ctst.compA.name or "Competitor A Unset"),
                      (ctst.compB.name or "Competitor B Unset")]
        self.buzzercodes = [dat.buzzerConfig.keycodeA,
                            dat.buzzerConfig.keycodeB]

        self.competitorName = wx.StaticText(
            self, wx.ID_ANY, "", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.competitorName.SetFont(self.font)

        container = wx.BoxSizer(wx.HORIZONTAL)

        self.sizer = wx.GridBagSizer(4, 2)
        container.Add( self.sizer, 1, wx.EXPAND|wx.ALL, 10)
        self.sizer.Add(self.competitorName, pos=(0,0), span=(1,2),
                       flag=wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.Add(wx.StaticText(self, label=self.comps[0]), pos=(1, 0))
        self.sizer.Add(wx.StaticText(self, label=self.comps[1]), pos=(2, 0))

        self.okButton = wx.Button(self, wx.ID_ANY, "OK")
        self.sizer.Add(self.okButton, pos=(3,0), span=(1,2), flag=wx.EXPAND)
        self.okButton.Bind( wx.EVT_BUTTON, self.OnClose)
        
        self.statusTexts = [
            wx.StaticText(self, label="untested", style=wx.ALIGN_RIGHT),
            wx.StaticText(self, label="untested", style=wx.ALIGN_RIGHT)]
        self.sizer.Add(self.statusTexts[0], pos=(1, 1), flag=wx.ALIGN_RIGHT)
        self.sizer.Add(self.statusTexts[1], pos=(2, 1), flag=wx.ALIGN_RIGHT)
        
        self.MakeModal()
        
        self.okButton.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.UpdateText()
        
        container.SetSizeHints(self)
        self.SetSizer( container)
        self.Layout()
        self.SetAutoLayout( True)

    def UpdateText(self):
        if self.compIdx > 1:
            self.competitorName.SetLabel("Complete")
        else:
            self.competitorName.SetLabel( self.comps[self.compIdx] + "\ntest your buzzer")
        
    def OnKeyPress(self, event):
        letter = chr(event.GetKeyCode())
        if self.compIdx > 1:
            return
        
        if letter == self.buzzercodes[ self.compIdx]:
            self.statusTexts[ self.compIdx].SetLabel("OK")
            self.compIdx += 1
            self.UpdateText()
        
    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def OnClose(self, event):
        self.parent.Raise()
        self.Destroy()
