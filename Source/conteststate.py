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

import random
import math

import contest
import competitor

class InvalidNumberOfCompetitorsError( Exception):
    pass
                     
class ContestState(object):
    """A ContestState is a tree of Contest objects, though it may be only
partially populated.

    """
    def __init__(self):
        self.totalCompetitors = 16
        self.cstate = None
        self.initializeFromCompetitorList(
            [competitor.Competitor() for i in
             range(self.totalCompetitors)])
                                          
        
    def __str__(self):
        #s = "Total competitors: {}\n".format(self.totalCompetitors)
        s = ""
        if self.cstate is None:
            s += "Tree uninitialized"
            return s
        
        for tier in range(len(self.cstate)):
            s += "Tier %d\n"%tier
            for c in self.cstate[tier]:
                s += str(c) + "\n"
                
        return s
    
    def displayStrA(self, tier, pairing):
        if self.cstate[tier][pairing] is None:
            return " "
        if self.cstate[tier][pairing].compA is None:
            return " "
        c = self.cstate[tier][pairing]
        return "%d  "%c.scoreA + c.compA.buttonStr()
        
    def displayStrB(self, tier, pairing):
        if self.cstate[tier][pairing] is None:
            return " "
        if self.cstate[tier][pairing].compB is None:
            return " "
        c = self.cstate[tier][pairing]
        return "%d  "%c.scoreB + c.compB.buttonStr()
        
    def initializeFromCompetitorList(self, clist, shuffle = True):
        """
        Inputs:
        ------
        clist :: list of Competitor objects

        """

        if len( clist) != 16:
            raise InvalidNumberOfCompetitorsError()
        contests = [contest.Contest(clist[i], clist[i+8]) for i in range(8)]
        
        if shuffle:
            random.shuffle(contests)
            
        self.cstate = [contests]
        lvl = 1
        while True:
            n = len(self.cstate[lvl-1])//2
            if n == 0:
                break
            x = [contest.Contest() for i in range(n)]
            self.cstate.append(x)
            lvl += 1
            
        # Add the 3rd place position
        thirdPlace = contest.Contest()
        thirdPlace.isThirdPlace = True
        self.cstate[-1].append( thirdPlace)
            
    def contestByLevelAndIndex(self, lvl, indx):
        return self.cstate[lvl][indx]

    def getContestByTierAndPairing( self, tier, pairing):
        return self.cstate[tier][pairing]
    
    def contestParents(self, lvl, idx):
        if lvl < 1:
            return (None, None)

        # Deal with the third place
        c = self.getContestByTierAndPairing(lvl, idx)
        
        if c.isThirdPlace:
            return(self.cstate[lvl-1][0], self.cstate[lvl-1][1])

        return (self.cstate[lvl-1][idx*2], self.cstate[lvl-1][idx*2+1])

    def updateFromParents(self, lvl, idx):
        """Determines which competitors are in the contest based on who won or
        lost parent competition.

        """
        c = self.contestByLevelAndIndex(lvl, idx)
        
        # Get the parent contests
        a, b = self.contestParents( lvl, idx)

        if c.isThirdPlace:
            if a.loser() != c.compA:
                c.setA(a.loser())
            elif a.loser() is None:
                c.setA(None)

            if b.loser() != c.compB:
                c.setB(b.loser())
            elif b.loser() is None:
                c.setB(None)

        else:
            # This is fairly confusing to reason through. If the
            # parent winner changed, we want to update the
            # corresponding competitor. However, if the winner is the
            # same, we want to preserve the winner and the local
            # score.
            if a.winner() != c.compA:
                c.setA(a.winner())
            elif a.winner() is None:
                c.setA(None)
                
            if b.winner() != c.compB:
                c.setB(b.winner())
            elif b.winner() is None:
                c.setB(None)
            
    def updateAllFromParents(self):
        for lvl in range(1, len(self.cstate)):
            for idx in range( len(self.cstate[lvl])):
                self.updateFromParents(lvl, idx)
                    
