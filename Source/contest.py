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

from competitor import UnrecognizedCompetitorError

class Contest(object):
    """Representation of a pair-off between two Competitors.
    """
    def __init__(self, compA=None, compB=None):
        self.compA = compA
        self.compB = compB
        self.scoreA = 0
        self.scoreB = 0
        self.isThirdPlace = False
        self.winningCompetitor = None

    def __str__(self):
        s = str(self.compA) + " score %d, "%self.scoreA
        s += str(self.compB) + " score %d, "%self.scoreB
        if self.winningCompetitor is None:
            s += "no winner determined"
        else:
            s += "winner is " + self.winningCompetitor.name
            
        return s
    
    def setA(self, comp):
        self.compA = comp
        self.scoreA = 0
        self.winningCompetitor = None

    def setB(self, comp):
        self.compB = comp
        self.scoreB = 0
        self.winningCompetitor = None

    def loser(self):
        """Return the contestant with the lowerscore. Returns None in case
of tie, including when both scores are 0.

        """
        if self.winningCompetitor is None:
            self.setWinner()
        
        if self.winningCompetitor is None:
            return None

        elif self.compA == self.winningCompetitor:
            return self.compB
        else:
            return self.compA

    def winner(self):
        """Return the contestant with the higher score. Returns None in case
of tie, including when both scores are 0.

        """
        self.setWinner()
        return self.winningCompetitor
        
    def setWinner(self):
        """Sets, and will override the established winner"""
        if self.scoreA == self.scoreB:
            self.winningCompetitor = None
        elif self.scoreA > self.scoreB:
            self.winningCompetitor = self.compA
        elif self.scoreA < self.scoreB:
            self.winningCompetitor = self.compB
        
    def increment(self, comp, amount=1):
        if comp == self.compA:
            self.scoreA += amount
        elif comp == self.compB:
            self.scoreB += amount
        else:
            raise UnrecognizedCompetitorError(comp)

    def set(self, comp=None, value=0):
        print("Competitor: ", comp)
        if comp == self.compA:
            self.scoreA = value
        elif comp == self.compB:
            self.scoreB = value
        elif comp is not None:
            raise UnrecognizedCompetitorError(comp)
        else:
            self.scoreA = value
            self.scoreB = value

    def reset(self):
        self.set()
        self.winningCompetitor = None

    def declareWinner(self, competitor=None):
        """Sets the winner to the specified competitor.

        If no competitor is specified, then set to result of
        self.winner(). Note that this can result in no winner being
        set because winner() can fail with a tie.

        """
        if competitor is not None:
            self.winningCompetitor = competitor
            return

        self.setWinner()
        self.winningCompetitor = self.winner()
