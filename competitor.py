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

class UnrecognizedCompetitorError( Exception):
    pass

class Competitor(object):
    def __init__(self, name=None, school=None):
        self.name = name
        self.school = school
        
    def __str__(self):
        return "{} at {}".format( self.name, self.school)

    def buttonStr(self):
        if self.name is None:
            return ""
        return self.name
