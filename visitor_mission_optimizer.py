#    "visitor_mission_optimizer" (v1.0)
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

# This program is meant to be used to find one possible route for visitor 
# missions in Elite Dangerous so that as few jumps as possible are needed
# to finish the missions.
# 
# This includes the important restiction that on a list of travel destinations, 
# all locations have to be a visited as given in the order in the list.
# This makes it difficult optimizing if several visitor missions are taken upon.
# Hence, the existance of this sprogram.
# 
# If 14 or less destinations need to be visited the exact solution is 
# calculated. The number 14 includes start and endpoint as two different 
# locations; even though it is the same. This takes approx. 1 minute.
# 
# Since the number of solutions grows factorial means adding just one more 
# destination, that the program needs an impractical amount of time to 
# calculate the exact solution. 
# In this case the order of destinations is shuffled (under the given 
# restiction) and the program is allowed the maximum allowed time 
# (default: 123 s, or defined by the user) to search for a (good enough) route.
# 
# ATTENTION: The mission data needs to be provided in a separate file 
# called "000_missions.txt". See this file for how to state mission data.


import class_datagrabber as cd
import class_routefinder as cr
import additional_functions as ad

if __name__ == '__main__':
	args = ad.get_args()

	# The infile with the mission data. Default is the current directory and
	# ""000_missions.txt" as filename.
	infile = args.infile

	# The maximum time the program is allowed to search for a route. Default 
	# is 123 seconds.
	maximum_allowed_time = args.maximum_time

	# Fetch the mission information and data necessary to calculate the length
	# of a route.
	datagrabber = cd.DataGrabber(infile)

	# Find a suitable route with the data gathered above.
	routefinder = cr.Routefinder(datagrabber, maximum_allowed_time)

	print("\nThis is the best route that could be found.")
	print("Route:", routefinder.record_path)
	# Stating the precision automatically rounds.
	print("Total distance: {0:.2f} ly\n".format(routefinder.record_length))






















