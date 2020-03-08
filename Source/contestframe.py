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
import competitorGrid
import contest
import answerframe
import treepanel
import buzzertestframe

from resource import resource_path

class ContestFrame(wx.Frame):
    def __init__(self, parent, *args, tier=None, pairing=None, tree=None, **kwargs):
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
        self.SetBackgroundColour(wx.Colour( 255, 255, 255 ))        
        # copy over since we need other questions too
        self.questionTimer = dat.questionTimer

        self.tree = tree

        self.callLater = None

        container = wx.BoxSizer(wx.HORIZONTAL)
        stack = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer( container)
        container.Add( stack, 1, wx.EXPAND|wx.ALL, 10)
        
        startBtn = wx.Button(self, wx.ID_ANY, 'Start')
        buzzerTestBtn = wx.Button(self, wx.ID_ANY, 'Test Buzzers')
        stack.Add(buzzerTestBtn, 0, wx.CENTER|wx.EXPAND)
        stack.Add(startBtn, 0, wx.CENTER|wx.EXPAND)
        startBtn.Bind(wx.EVT_BUTTON, self.OnStartClicked)
        buzzerTestBtn.Bind(wx.EVT_BUTTON, self.OnBuzzerTestClicked)
        
        resetBtn = wx.Button(self, wx.ID_ANY, 'Reset Timer')
        stack.Add(resetBtn, 0, wx.CENTER|wx.EXPAND, 10)
        resetBtn.Bind(wx.EVT_BUTTON, self.OnResetClicked)

        self.timertext = wx.StaticText(self, wx.ID_ANY, '%d'%self.questionTimer)
        self.timertext.SetFont(self.bigFont)
        stack.Add( self.timertext, 0, wx.CENTER, 10)
        self.timerEnabled = False
        
        # Add elements about the contestants
        contestantBox = wx.BoxSizer(wx.HORIZONTAL)
        stack.Add( contestantBox, 0, wx.EXPAND|wx.CENTER)

        aStack = wx.BoxSizer(wx.VERTICAL)
        bStack = wx.BoxSizer(wx.VERTICAL)

        contestantBox.Add( aStack, 1)
        contestantBox.AddStretchSpacer()
        contestantBox.Add( bStack, 1)

        ctst = dat.getContestByTierAndPairing( tier, pairing)

        self.tier = tier
        self.pairing = pairing
        self.ctst = ctst
        self.cmpA = ctst.compA
        self.cmpAEnabled = True
        self.cmpB = ctst.compB
        self.cmpBEnabled = True
        
        if ctst.compA is None or ctst.compA.name is None:
            t = '--Competitor A unset--'
        else:
            t = ctst.compA.name

        competitorName = wx.StaticText(self, wx.ID_ANY, t)
        competitorName.SetFont(self.font)
        aStack.Add( competitorName, 1)
        self.aScoreBox = wx.SpinCtrl(self)
        aStack.Add( self.aScoreBox, 1)
        self.aScoreBox.Bind(wx.EVT_SPINCTRL, self.updateAScore)
        
        if ctst.compB is None or ctst.compB.name is None:
            t = '--Competitor B unset--'
        else:
            t = ctst.compB.name

        competitorName = wx.StaticText(self, wx.ID_ANY, t)
        competitorName.SetFont(self.font)
        bStack.Add(competitorName, 1)
        self.bScoreBox = wx.SpinCtrl(self)
        bStack.Add( self.bScoreBox, 1)
        self.bScoreBox.Bind(wx.EVT_SPINCTRL, self.updateBScore)

        finishBtn = wx.Button(self, wx.ID_ANY, 'Finish Round')
        stack.Add(finishBtn, 0, wx.CENTER|wx.EXPAND)
        finishBtn.Bind(wx.EVT_BUTTON, self.OnFinishClicked)
        
        self.aScoreBox.SetValue('%d'%ctst.scoreA)
        self.bScoreBox.SetValue('%d'%ctst.scoreB)
        self.MakeModal()
        startBtn.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        container.SetSizeHints(self)
        self.SetSizer( container)
        self.Layout()
        self.SetAutoLayout( True)

        self.Bind( wx.EVT_CLOSE, self.OnClose)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(
            resource_path('resources/main_logo1.ico'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def updateAScore(self, event):
        self.ctst.scoreA = int(self.aScoreBox.GetValue())
        
    def updateBScore(self, event):
        self.ctst.scoreB = int(self.bScoreBox.GetValue())

    def OnKeyPress(self, event):
        letter = chr(event.GetKeyCode())

        if dat.buzzerConfig.keycodeA == letter and self.cmpAEnabled:
            if self.callLater is not None:
                self.callLater.Stop()
            #print('got buzzer code for competitor A')
            a = answerframe.AnswerFrame(self, contest=self.ctst, competitor=self.cmpA,
                                    scorebox=self.aScoreBox, competitorAorB = 'a',
                                    title=(self.cmpA.name or '')+ ' For The Answer!')
            a.Centre()
            a.Show(True)
            
        elif dat.buzzerConfig.keycodeB == letter and self.cmpBEnabled:
            if self.callLater is not None:
                self.callLater.Stop()
            #print('got buzzer code for competitor B')
            a = answerframe.AnswerFrame(self, contest=self.ctst, competitor=self.cmpB,
                                    scorebox=self.bScoreBox, competitorAorB = 'b',
                                    title=(self.cmpB.name or '') + ' For The Answer!')
            a.Centre()
            a.Show(True)
            
        else:
            print("something's wrong, got letter '%s' that wasn't registered in dat" % letter)
        
    def OnStartClicked(self, event):
        self.SetBackgroundColour(wx.Colour(255,255,255))
        if self.questionTimer > 0:
            self.callLater = wx.CallLater(100, self.on_timer)
            
    def OnBuzzerTestClicked(self, event):
        bframe = buzzertestframe.BuzzerTestFrame(
            self, tier=self.tier, pairing=self.pairing)
        bframe.Centre()
        bframe.Show()
        
    def OnFinishClicked(self, event):
        if self.callLater is not None:
            self.callLater.Stop()
            del self.callLater
            
        self.ctst.declareWinner()
        if self.ctst.winningCompetitor is not None:
            wx.MessageBox((self.ctst.winningCompetitor.name or '') + ' Is The Winner!', 'Info',
                          wx.OK | wx.ICON_INFORMATION)
            
        self.parent.treePanel.updateTree()
        self.parent.SetFocus()
        self.Close()

    def OnResetClicked(self, event):
        self.SetBackgroundColour(wx.Colour(255,255,255))
        try:
            self.callLater.Stop()
        except AttributeError:
            pass
        self.questionTimer = dat.questionTimer
        self.timertext.SetLabel(str(self.questionTimer))
        self.cmpAEnabled = True
        self.cmpBEnabled = True
        
    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def displayTime(self):
        self.timertext.SetLabel('%d'%self.questionTimer)
        
    def on_timer(self, *args, **kwargs):
        self.questionTimer -= 0.1

        # the background color code needs to go in a seperate /if/
        # statement to make it turn red when it should. 
        if self.questionTimer < 1:
            self.SetBackgroundColour(wx.Colour(255,0,0))
            
        if self.questionTimer <= 0:
            self.timerEnabled = False
            return
        
        self.displayTime()
        self.callLater.SetArgs( 100, self.on_timer)
        self.callLater.Start()
        
    def OnClose(self, event):
        try:
            self.callLater.Stop()
        except AttributeError:
            pass
            
        self.parent.Raise()
        event.Skip()
