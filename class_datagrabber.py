#    "class_datagrabber" (v1.0)
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

# This file contains the class definition for the object that does everything
# to get the mission information and all data needed to calculate the length
# of a route.
# 
# The latter es fetched from EDSM.net via its api.


from math import sqrt
import requests
import json


# This class is doing all get the mission information and all data needed to 
# calculate the length of a route.
# It is instantiated in the main program.
class DataGrabber(object):
	# < infile > is the complete path to the mission data file. This includes
	# the filename and its extension! By default the path is the current
	# directory and the filename is "000_missions.txt".
	def __init__(self, infile):
		self.mission_file = infile
		# The system in which the travelers are picked up and to which they
		# have to be brought back to. Will be set in _get_missions()
		self.origin = None
		# A list that contains lists that contain the destinations for each
		# traveler in the correct order. Will be set in _get_missions()
		self.travelers = []
		# This will be a dict that contains each destination as a main-key. The 
		# values are the coordinates of this destination and a subdict that
		# again contains each destination as a sub-key. The values of the 
		# sub-dict are the distances between the main-key destination and the 
		# sub-key destination. Will be filled in _get_coordinates() 
		# and _get_distances().
		self.distances = {}

		self._get_missions()
		self._get_coordinates()
		self._get_distances()


	# This method reads the relevant mission data (and the point of origin)
	# from the respective file.
	def _get_missions(self):
		mission_data = False

		with open(self.mission_file, 'r') as f:
			for line in f:
				splitted = line.strip().split('\t')

				if "I'm at" in line:
					self.origin = splitted[1]
				elif '< Missions START >' in line:
					mission_data = True
					continue

				# .strip() removes fortunately all leading (and trailing)
				# whitespaces (incl. tabs). Thus the first element will always
				# have content if it is valid mission data.
				if mission_data and splitted[0] != '':
					# With this I'll try to accomodate for too many tabs
					# in the data provided by the user.
					destinations = [x for x in splitted if len(x.strip()) > 0]

					self.travelers.append(destinations)


	# To calculate the distances between two systems I'll need the coordinates.
	# This method get's them and puts them all into < self.distances >.
	def _get_coordinates(self):
		self.distances[self.origin] = self._request_coords(self.origin)

		for destinations_per_traveler in self.travelers:
			for destination in destinations_per_traveler:
				# Different travelers might want to go to the same destination.
				# No need to request the coordinates for them again.
				try:
					self.distances[destination]
				except KeyError:
					self.distances[destination] = self._request_coords(destination)


	# This method does the actual request to EDSM to get ... well, what its 
	# name says: the coordinates of a given < destination >.
	def _request_coords(self, destination):
		print("Fetching coordinates for", destination)
		url = 'https://www.edsm.net/api-v1/system'

		while True:
			payload = {'systemName':destination, 'showCoordinates':1}
			system = requests.get(url, params = payload)

			if system.status_code != requests.codes.ok:
				continue

			# The content I'm actualy interested in is a binary string.
			return json.loads(system._content.decode())['coords']


	# This method actually calculates the distance between two given points.
	# < first > and < second > are the names of the points the distance shall 
	# be calculated for.
	def _calculate_distance(self, first, second):
		x_1 = self.distances[first]['x']
		y_1 = self.distances[first]['y']
		z_1 = self.distances[first]['z']

		x_2 = self.distances[second]['x']
		y_2 = self.distances[second]['y']
		z_2 = self.distances[second]['z']

		return sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2 + (z_1 - z_2)**2)


	# This method puts the actual distances into < self.distances >. 
	# The distances between ALL destinations are calculated. This takes some 
	# time to do it once, but has the advantage that I don't need to do the 
	# calculations again when going through all possible routes but can just 
	# look the values up in < self.distances >. Doing it that way saves almost
	# 25 percent of the overall process time!
	def _get_distances(self):
		print("\nCalculating distances ...\n")

		# The distances between ALL points are calculated.
		for first in self.distances:
			for second in self.distances:
				# Since this is a symmetrical problem had I originally a check 
				# if a distance was already calculated to avoid double
				# calculations. It then turned out that this here is certainly 
				# NOT a bottleneck and to make the code a bit easier I simply 
				# calculate everything twice.
				distance = self._calculate_distance(first, second)
				self.distances[first][second] = distance






















