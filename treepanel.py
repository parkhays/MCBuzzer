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
import wx.lib.scrolledpanel
import os

from gdata import dat
import competitorGrid
import contestframe

class TreePanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent, *args, **kwargs):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, *args, **kwargs)#
#        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.buttons = []
        
        self.font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        self.hgrid = wx.BoxSizer(wx.HORIZONTAL)
        self.vgridList = []
        self.SetSizer(self.hgrid)
        
        vboxes = []
        lastTierIdx = len(dat.contestState.cstate) - 1
        for tier in range(len(dat.contestState.cstate)):
            buttonsInTier = []
            w = wx.BoxSizer(wx.VERTICAL)
            self.vgridList.append(w)

            # In the first tier, no spacer at the top or bottom
            if tier > 0:
                w.AddStretchSpacer(1)
            
            self.hgrid.Add(w, flag=wx.EXPAND|wx.ALL)
            lastPairingIdx = len( dat.contestState.cstate[tier]) -1
            for pairing in range( len( dat.contestState.cstate[tier])):
                btn = self.ButtonFromTierPairing( tier, pairing)
                btn.tierPairing = (tier, pairing)
                btn.SetFont(self.font)
                buttonsInTier.append( btn)

                if tier == lastTierIdx:
                    if pairing == lastPairingIdx:
                        # add text
                        txt = wx.StaticText(self, wx.ID_ANY, "\nThird Place")
                        w.Add(txt, proportion=0, flag=wx.ALL)
                        w.Add(btn, proportion=0, flag=wx.EXPAND)
                        w.AddStretchSpacer(1)
                    else:
                        w.Add(btn, proportion=0)
                elif tier == 0:
                    # In the left-most tier, no stretch spacers at the
                    # top and bottom. In the first condition, a spacer
                    # is added except at the end.

                    w.Add(btn,proportion=1,flag=wx.ALL|wx.EXPAND)
                    if pairing < lastPairingIdx:
                        w.AddStretchSpacer(1)
                else:
                    w.Add(btn,proportion=0,flag=wx.ALL|wx.EXPAND)
                    w.AddStretchSpacer(1)
                    
            self.buttons.append( buttonsInTier)
            self.hgrid.SetSizeHints(self)
            if tier != len(dat.contestState.cstate) -1:
                self.hgrid.AddStretchSpacer(1)
                
        self.hgrid.SetSizeHints(self)
        self.SetSizer(self.hgrid)

        self.SetupScrolling()

        self.Fit()
        
    def updateTree(self):
        """Update button text to reflect current state of the competition"""
        dat.contestState.updateAllFromParents()
        dat.autoSave()
        for tier in range( len( dat.contestState.cstate)):
            for pairing in range( len( dat.contestState.cstate[tier])):
                btn = self.buttons[tier][pairing]
                btn.SetLabel(dat.contestState.displayStrA(tier, pairing)
                              + "\n" +
                              dat.contestState.displayStrB(tier, pairing))
        wx.Yield()
        self.Layout()
        
    def ButtonFromTierPairing(self, tier, pairing):
        txt = " \n "
        
        btn = wx.Button(self, wx.ID_ANY, txt, style=wx.BU_LEFT)
        btn.Bind(wx.EVT_BUTTON, self.OnClicked)
        btn.tierPairing = (tier, pairing)
        return btn
        
    def OnClicked(self, event):
        button = event.GetEventObject()

        # We don't want to open the contest window unless our
        # competitors are set, so check.
        ctst = dat.getContestByTierAndPairing(
            button.tierPairing[0], button.tierPairing[1])

        if (ctst.compA is None
            or ctst.compA.name is None
            or ctst.compB is None
            or ctst.compB.name is None):
            return
        
        cframe = contestframe.ContestFrame(
            self.parent, wx.ID_ANY, "Compete",
            tier=button.tierPairing[0], pairing=button.tierPairing[1], tree=self)
        cframe.Centre()
        cframe.Show(True)
