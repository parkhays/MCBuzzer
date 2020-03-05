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

"""Global data storage and manager"""

import pickle

import competitor
import conteststate
class UnsetFilenameError(Exception):
    pass

class BuzzerConfig(object):
    def __init__(self):
        self.keycodeA = None
        self.keycodeB = None

    def __str__(self):
        s = "Keycode A: {}\n".format(self.keycodeA)
        s += "Keycode B: {}\n".format(self.keycodeB)
        return s
    
class GData(object):
    def __init__(self):
        self.competitorList = None
        self.contestState = conteststate.ContestState()
        self.buzzerConfig = BuzzerConfig()
        self.fileName = None
        self.questionTimer = 60
        self.answerTimer = 7

    def __str__(self):
        s = ""
        if self.competitorList is None:
            s += "Competitor list is unitialized\n"
        else:
            s += "Competitor list:\n"
            for c in self.competitorList:
                s += str(c) + "\n"

        if self.contestState is None:
            s += "Contest state is uninitialized\n"
        else:
            s += "Contest state:\n"
            s += str(self.contestState)

        if self.buzzerConfig is None:
            s += "Buzzer configuration is uninitialized\n"
        else:
            s += "Buzzer configuration:\n"
            s += str(self.buzzerConfig)
            s += "\n"
            
        if self.fileName is None:
            s += "Filename is uninitialized\n"
        else:
            s += "Filename: " + self.fileName + "\n"
            
        return s

    def getContestByTierAndPairing( self, tier, pairing):
        return self.contestState.getContestByTierAndPairing( tier, pairing)
    
    def setContestState(self, shuffle=False):
        # Create a new ContestState
        self.contestState = conteststate.ContestState()
        
        self.contestState.initializeFromCompetitorList( self.competitorList, shuffle=shuffle)
        print("----------------- set contest state -------------")
        print(self)
        
    def save(self, fid):
        pickle.dump( {'competitorList': self.competitorList,
                      'contestState': self.contestState,
                      'buzzerConfig': self.buzzerConfig,
                      'questionTimer': self.questionTimer,
                      'answerTimer': self.answerTimer},
                     fid)

    def saveToFile(self, fn = None):
        if fn == None and self.fileName is None:
            raise UnsetFilenameError()
        
        if fn is not None:
            self.fileName = fn
            self.save(open(fn, 'wb'))

        else:
            self.save(open(self.fileName, 'wb'))

    def open(self, fn):
        self.load( open(fn, 'rb'))
        self.fileName = fn
        
    def load(self, fid):
        d = pickle.load(fid)
        self.competitorList = d['competitorList']
        self.contestState = d['contestState']
        self.buzzerConfig = d['buzzerConfig']
        try:
            self.questionTimer = d['questionTimer']
        except KeyError:
            pass
        
        try:
            self.answerTimer = d['answerTimer']
        except KeyError:
            pass

    def setKeycodes(self, keya, keyb):
        # The wx keycode system seems to return capital letters,
        # so the string comparison needs uppercase letters.
        #
        # Also, these should have been encapsulated from the start.
        self.buzzerConfig.keycodeA = keya.upper()
        self.buzzerConfig.keycodeB = keyb.upper()

    def getKeycodes(self):
        return (self.buzzerConfig.keycodeA, self.buzzerConfig.keycodeB)

dat = GData()
