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
import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "Source"))

import contest
import conteststate
import competitor

def canonicalCompetitorList():
    return [ competitor.Competitor('Student %02d'%i, 'School %02d'%i)
             for i in range( 16)]

def canonicalContestList():
    clist = canonicalCompetitorList()
    return [contest.Contest(clist[i], clist[i+8]) for i in range(8)]
    
def test_ContestState_inializeFromCompetitorList():
    
    cs = conteststate.ContestState()
    cs.initializeFromCompetitorList( canonicalCompetitorList(), shuffle=False)
    conlist = canonicalContestList()
    assert len(cs.cstate[0]) == len(conlist)
    
    for i in range(8):
        assert str(cs.cstate[0][i]) == str(conlist[i])

def test_contestParents():
    conlist = canonicalContestList()
    complist = canonicalCompetitorList()
    cs = conteststate.ContestState()
    
    cs.initializeFromCompetitorList( complist, shuffle=False)

    a, b = cs.contestParents(1,0)
    assert str(a) == str(cs.cstate[0][0])
    assert str(b) == str(cs.cstate[0][1])

    a, b = cs.contestParents(1,3)
    assert str(a) == str(cs.cstate[0][6])
    assert str(b) == str(cs.cstate[0][7])

def test_updateFromParents():
    conlist = canonicalContestList()
    complist = canonicalCompetitorList()
    cs = conteststate.ContestState()
    
    cs.initializeFromCompetitorList( complist, shuffle=False)

    # Initially unset
    cn = cs.contestByLevelAndIndex(1,0)
    assert cn.compA is None
    assert cn.compB is None
    
    a, b = cs.contestParents(1,0)
    a.increment( a.compA, 1)
    b.increment( b.compA, 1)
    cs.updateFromParents(1,0)

    assert str(cn.compA) == str(conlist[0].compA)
    assert str(cn.compB) == str(conlist[1].compA)

def test_updateAllFromParents():
    conlist = canonicalContestList()
    complist = canonicalCompetitorList()
    cs = conteststate.ContestState()
    
    cs.initializeFromCompetitorList( complist, shuffle=False)

    # Initially unset
    cn = cs.contestByLevelAndIndex(1,0)
    assert cn.compA is None
    assert cn.compB is None
    
    a, b = cs.contestParents(1,0)
    a.increment(a.compA, 1)
    b.increment(b.compA, 1)
    cs.updateAllFromParents()
    
    assert str(cn.compA) == str(conlist[0].compA)
    assert str(cn.compB) == str(conlist[1].compA)

    # Spot check that nothing else is set
    assert cs.contestByLevelAndIndex(2,0).compA is None
    assert cs.contestByLevelAndIndex(2,0).compB is None
    
def test_contestByLevelAndIndex():
    conlist = canonicalContestList()
    
    cs = conteststate.ContestState()
    cs.initializeFromCompetitorList( canonicalCompetitorList(), shuffle=False)

    assert str(cs.contestByLevelAndIndex(0,0)) == str(conlist[0])
    assert str(cs.contestByLevelAndIndex(0,7)) == str(conlist[7])


