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

import sys
import os
sys.path.append(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "Source"))

import contest
import competitor

def test_init():
    """Test initialization of  of Contest class"""
    a = competitor.Competitor("A", "a-school")
    b = competitor.Competitor("B", "b-school")
    
    c = contest.Contest(a,b)

    assert c.compA == a
    assert c.compB == b
    assert c.scoreA == 0
    assert c.scoreB == 0
    assert c.winningCompetitor == None

def test_increment():
    """Test that incrementing the score of competitors in a contest"""
    a = competitor.Competitor("A", "a-school")
    b = competitor.Competitor("B", "b-school")
    
    c = contest.Contest(a,b)

    assert c.scoreA == 0
    assert c.scoreB == 0
    
    c.increment(a, 1)
    assert c.scoreA == 1
    assert c.scoreB == 0
    
    c.increment(a, 1)
    assert c.scoreA == 2
    assert c.scoreB == 0
    
    c.increment(a, 2)
    assert c.scoreA == 4
    assert c.scoreB == 0
    
    c.increment(b)
    assert c.scoreA == 4
    assert c.scoreB == 1

    c.increment(a)
    assert c.scoreA == 5
    assert c.scoreB == 1
    
def test_winner():
    """Test that the winner is returned correctly"""
    a = competitor.Competitor("A", "a-school")
    b = competitor.Competitor("B", "b-school")
    
    c = contest.Contest(a,b)
    
    assert c.winner() is None
    
    c.increment(a)
    assert c.winner() == a

    c.increment(b, 2)
    assert c.winner() == b

    c.reset()
    assert c.winner() is None

def test_set():
    """Test that incrementing the score of competitors in a contest"""
    a = competitor.Competitor("A", "a-school")
    b = competitor.Competitor("B", "b-school")
    c = contest.Contest(a,b)
    c.set(comp=a, value=10)
    c.set(comp=b, value=3)
    assert c.scoreA == 10
    assert c.scoreB == 3
