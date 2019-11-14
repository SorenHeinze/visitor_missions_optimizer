#    "additional_functions" (v1.0)
#    Copyright 2019 Soren Heinze
#    soerenheinze (at) gmx (dot) de
#    5B1C 1897 560A EF50 F1EB 2579 2297 FAE4 D9B5 2A35
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This file contains functions used in visitor_mission_optimizer.py which did 
# not fit into any of the other files or the classes.


import argparse

# This function gets the command line arguments. It exists mainly to keep the 
# main file more tidy.
def get_args():
	parser = argparse.ArgumentParser()

	keyword = '--maximum-time'
	short = '-mt'
	this = 'The maximum time the whole path finding process is allowed to '
	that = 'take. Default is 123 seconds.'
	parser.add_argument(keyword, short, metavar = 'seconds', type = float, \
											default = 123, help = this + that)

	keyword = '--infile'
	short = '-f'
	this = 'Complete path to the file with the mission data (incl. filename '
	that = 'AND file-extension!). Default is the current directory with '
	siht = '"000_missions.txt" as filename.'
	parser.add_argument(keyword, short, type = str, \
					default = './000_missions.txt', help = this + that + siht)

	args = parser.parse_args()

	return args






















