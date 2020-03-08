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
import contest

from resource import resource_path


class AnswerFrame(wx.Frame):
    """Dialog for a single competitor to answer his or her question"""
    
    def __init__(self, parent, *args, contest=None, competitor=None, scorebox=None, competitorAorB = '', **kwargs):
        """Contest frame creation
        
        kwargs:
        -----
        contest
        competitor

        """
        wx.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.contest = contest
        self.competitor = competitor
        self.scorebox = scorebox
        self.callLater = None
        self.competitorAorB = competitorAorB
        self.answerTimer = dat.answerTimer
        self.font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) ) 
        stack = wx.GridBagSizer(3, 2)

        self.timerEnabled = True

        # a little code to prevent NoneType errors
        competitorText = wx.StaticText(self, wx.ID_ANY, str(competitor.name or '--Competitor unset--'), style=wx.ALIGN_CENTER)
        competitorText.SetFont( self.font)
        stack.Add(competitorText, pos=(0,0), span=(1,2), flag=wx.ALIGN_CENTER)

        self.timerText = wx.StaticText(self, wx.ID_ANY, "%d"%self.answerTimer, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.timerText.SetFont(self.font)

        container = wx.BoxSizer(wx.HORIZONTAL)
        container.Add( stack, 1, wx.EXPAND|wx.ALL, 10)
        
        stack.Add(self.timerText, pos=(1,0), span=(1,2), flag=wx.ALIGN_CENTER)

        btnCorrect = wx.Button(self, wx.ID_ANY, "Correct")
        btnIncorrect = wx.Button(self, wx.ID_ANY, "Incorrect")

        btnCorrect.Bind(wx.EVT_BUTTON, self.correct)
        btnIncorrect.Bind(wx.EVT_BUTTON, self.incorrect)
        
        stack.Add(btnCorrect, (2, 0), flag=wx.ALL)
        stack.Add(btnIncorrect, (2, 1), flag=wx.ALL)
        container.SetSizeHints(self)
        self.SetSizer(container)
        self.Layout()
        self.SetAutoLayout(True)
        self.Bind( wx.EVT_CLOSE, self.OnClose)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(
            resource_path('resources/main_logo1.ico'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.OnTimer()

    def correct(self, event):
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.contest.increment(self.competitor)
        if self.callLater is not None:
            self.callLater.Stop()
            # Disable the parent window's countdown
            self.parent.questionTimer = dat.questionTimer
            self.parent.callLater = None
            self.parent.displayTime()
            self.parent.cmpAEnabled = True
            self.parent.cmpBEnabled = True
            
        if self.competitorAorB == 'a':
            self.scorebox.SetValue("%d"%self.contest.scoreA)
        elif self.competitorAorB == 'b':
            self.scorebox.SetValue("%d"%self.contest.scoreB)
        del self.callLater
        self.Destroy()

    def incorrect(self, event):
        self.SetBackgroundColour(wx.Colour(255,255,255))
        if self.callLater is not None:
            self.callLater.Stop()
            del self.callLater
            
        # Reregister the parent to continue
        self.parent.callLater.SetArgs(100, self.parent.on_timer)
        self.parent.callLater.Start()
        if self.competitorAorB == 'a':
            self.parent.cmpAEnabled = False
        elif self.competitorAorB == 'b':
            self.parent.cmpBEnabled = False

        self.Destroy()
        
    def OnTimer(self):
        if not self.timerEnabled:
            return
        
        self.answerTimer -= 0.1

        # this is done slightly differently than contestframe because
        # the timer code is more complex
        if self.answerTimer <= 0.05:
            self.SetBackgroundColour(wx.Colour(255,0,0))
            
        if self.answerTimer <= 0:
            self.timerEnabled = False
            return
        
        if 0.95 < self.answerTimer%1 or self.answerTimer%1 <= 0.05:
            self.timerText.SetLabel("%d"%self.answerTimer)

        self.callLater = wx.CallLater(100, self.OnTimer)

    def OnClose(self, event):
        if self.callLater is not None:
            self.callLater.Stop()
