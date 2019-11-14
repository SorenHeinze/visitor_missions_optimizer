#    "class_routefinder" (v1.0)
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

# This file contains the class definition for the object that actually finds 
# a route that is optimal (or at least good enough) and satisfies all mission
# givers.
# When a route is calculated, the most important restriction is, that on a 
# ist of travel destinations, all locations have to be a visited as given in 
# the order in the list.


from copy import deepcopy
from time import time
from math import factorial
from itertools import permutations

# The object that contains all methods that are necessary to determine a
# route.
class Routefinder(object):
	# < datagrabber > is the class DataGrabber instance. It contains the data
	# class Routefinder will work with.
	# < maximum_allowed_time > is the maximum time that shall be used to find 
	# an optimal solution. If this time is exceeded the best solution so far 
	# will be used. Needs to be in seconds. Default is 123 seconds but can
	# be provided by the user.
	def __init__(self, datagrabber, maximum_allowed_time):
		# The list that contains the lists that contain the destinations for
		# all travelers in the correct order.
		self.travelers = datagrabber.travelers
		# The dict that contains all destinations as main keys and sub-dicts as
		# values. Said sub-dict again contains each destination as a sub-key and 
		# the values of the  sub-dict are the distances between the main-key 
		# destination and the sub-key destination.
		self.distances = datagrabber.distances
		# It's handy to have the origin (or home location) separate.
		self.origin = datagrabber.origin

		# To be able to measure how much time the search process needed so far.
		self.start_time = time()
		# The maximum time the user is willing to wait for a solution.
		self.maximum_allowed_time = maximum_allowed_time
		# A really high default value to make sure that any route is always
		# shorter. The value of the first route found will replace this value.
		# Afterwards just smaller values (due to shorter routes) will be stored
		# in here.
		self.record_length = 999999999999999999999.9
		# The best route (so far). Will change many times during the search
		# process but will contain the truly best route (that was found within 
		# the given maximum time) in the end.
		# The length of the route stored in here corresponds is 
		# < self.record_length >. The best route will be presented to the user.
		self.record_path = None

		# Well, this just does everything to find the best route.
		self._do_all()


	# This is the method that calls all methods that call methods (etc. pp.)
	# to find the best solution for all missions. It exists mainly to keep 
	# __init__() more tidy
	def _do_all(self):
		# This is the number of unique destinations to be visited and thus the 
		# minimum amount of points in the route.
		# This does NOT include origin.
		minimum_destinations = len(set([x for traveler in self.travelers for x in traveler]))

		# With 12 destinations (EXCLUDING the start and end (origin)) 
		# calculating the  exact solution takes approx. one minute. More than 
		# that needs an impractical amount of time. 12 was determined 
		# empirically. 
		if minimum_destinations <= 12:
			self._find_exact_solution()
		else:
			self._find_good_enough_solution()


	# This function is called if the enumber of destinations is small enough so
	# that it is unlikely that it exceeds < self.maximum_allowed_time >. It
	# exists mainly to keep _do_all() more tidy.
	def _find_exact_solution(self):
		this = "Number of destinations small enough. I'll try to calculate "
		that = "the exact solution ... \n"
		print(this + that)

		# Start and end of the journey are the same. The rest will be 
		# filled in in _find_best_route().
		path = [self.origin, self.origin]

		# It is still possible that the search process needs too much time.
		# Most likely because the user provided a small value for how long
		# he or she is willing to wait. Hence, the return value of 
		# _find_best_route() is called < aborted > and ...
		aborted = self._find_best_route(path, self.travelers)

		# ... if the search process was aborted the user will be told so.
		if aborted:
			this = "\nThe search algorithm was aborted because the process "
			that = "time exceeded {} s. ".format(self.maximum_allowed_time)
			siht = "The following is the best solution found."
			print(this + that + siht)


	# Dito just for the case that searching for the exact solution likely will
	# need too much time.
	# In here the program starts to go through all possible combinations of 
	# destinations to travel to for a given order of travelers. 
	# _find_best_route() aborts if it exceeds the allotted time for a given 
	# order of travelers. Afterwards _find_best_route() is called again with 
	# a different order of travelers. 
	# It is UNlikely that this function finds the exact solution. But it 
	# probably finds a solution which is good enough considering that several 
	# different orders of travelers are checked in the for-loop below.
	# See the comment before the said for-loop for further details.
	# 
	# ATTENTION: The bad situation described for _find_best_route() is likely 
	# to occur here.
	def _find_good_enough_solution(self):
		this = "Number of destinations too large. Calculating the exact solution "
		that = "takes more than {} s. ".format(self.maximum_allowed_time)
		siht = "Thus 'just' a good enough route will be calculated ... \n"
		print(this + that + siht)

		# To tell the user how far the algorithm has come I need to know how
		# many permutations there are at all. 
		number_of_permutations = factorial(len(self.travelers))

		# < self.maximum_allowed_time > is the maximum time allowed for the 
		# whole process. This needs to be shared over all possible permutations.
		self.maximum_allowed_time = self.maximum_allowed_time / number_of_permutations

		# ATTENTION: In the worst case the very first point to be visited might 
		# be a very bad choice which will lead to a very long processing time. 
		# Hence, _find_best_route() aborts if it takes too much time.
		# This is also one of the reasons why in here the order of travelers is 
		# permuted. Just to get different starting points for the permutations. 
		# This is effectively like randomizing the order of points to visit 
		# under the given constraint, that I MUST visit the destinations of a 
		# given traveler in the given order.
		for i, order_of_travelers in enumerate(permutations(self.travelers)):
			# The time from which "counting" starts needs to be new for each 
			# permutation.
			self.start_time = time()

			path = [self.origin, self.origin]

			aborted = self._find_best_route(path, order_of_travelers)

			if aborted:
				this = "This needs too much time. Trying a radically new order of "
				that = "locations to travel to "
				siht = "({} of {}) ... ".format(i + 1, number_of_permutations)
				print(this + that + siht)


	# This function sums up the distances between all points in a given < path >.
	def _length_of_path(self, path):
		length = 0

		for i in range(len(path) - 1):
			first = path[i]
			second = path[i + 1]

			length += self.distances[first][second]

		return length


	# With this recursive function the program goes through all possible 
	# combinations of points to be visited and calculates for each the exact 
	# path-length. The best solution is saved as attribute of this class.
	# 
	# ATTENTION: The shortest path may require to visit one point twice (or 
	# even more often). An example that illustrates this may be the following.
	# One destination may e.g. be close to the start and first to be visited 
	# for one traveler but last for another. In that case it doesn't make sense 
	# to wait to visit the first point for the first visitor until the 2nd 
	# is "processed".
	# ATTENTION: For more than 14 points (including twice the start / end) 
	# this takes too much time. Thus _find_good_enough_solution() exists which 
	# returns a route which shouldn't be too bad either.
	# See comments to said method for more details.
	# 
	# This method returns True if it is aborted because the process time
	# is larger than < self.maximum_allowed_time >.
	# If the number of destinations is small enough this should not happen too 
	# often (if at all). If it isn't _do_all() contains the second condition
	# which will call _find_good_enough_solution() and then this will become
	# relevant.
	def _find_best_route(self, this_path, travelers):
		# I need to take the very first elements in the points of interests of 
		# the travelers because they don't want to see a destination if they 
		# haven't seen the previous one.
		points = []
		for traveler in travelers:
			# Some travelers might want to visit fewer locations than others.
			# Since I'm deleting the already visited locations, this may lead to 
			# errors.
			try:
				points.append(traveler[0])
			except IndexError:
				pass

		for point in points:
			# The check how much time the search process needed so far.
			if (time() - self.start_time) > self.maximum_allowed_time:
				return True

			# For each iteration I need a fresh start from the original 
			# configuration of points of interest.
			# To < local_path > I will add and ...
			local_path = deepcopy(this_path)
			# ... from < local_travelers > I will subtract an element. These 
			# two modified lists go then as new original configuration into the 
			# next recursive call of _find_best_route().
			local_travelers = deepcopy(travelers)
			# .insert(-1, point) inserts at the second to last position in the 
			# list. This is correct, since the last element is fixed and in 
			# each recursive call of _find_best_route() the order of the 
			# previous elements shall not change.
			local_path.insert(-1, point)

			# Now remove < point > from the list of the travelers if it is
			# the next destination to be visited for them, because with adding 
			# to < local_path > it is visited.
			# I do NOT break the loop once I found < point > in one of the 
			# travelers lists because several travelers could want to visit the
			# same point.
			for traveler in local_travelers:
				try:
					# ATTENTION: JUST the next point of interest can be 
					# considered when looking up if < point > is a point of
					# interest for < traveler >. This is because I'm not 
					# allowed to visit points further down < travelers > list
					# if I haven't been to the previous ones.
					if point in traveler[0]:
						traveler.pop(0)
				except IndexError:
					pass

			# This is to check below if there is more to visit.
			more_to_visit = sum([len(traveler) for traveler in local_travelers])

			length_local_path = self._length_of_path(local_path)

			# Some paths may be so bad that even before recursively going 
			# through all remaning possibilities it is longer than the 
			# shortest path (so far). In this case don't call yourself 
			# because it is meaningless. Rather continue with the next 
			# point in the list. This speeds the whole process considerably 
			# up! With this it needs up to 5 times less time!
			if length_local_path > self.record_length:
				continue

			# Once there is nothing else to visit, ...
			if more_to_visit == 0:
				# ... check how long the path is and set it as new best path 
				# if it is shorter.
				if length_local_path < self.record_length:
					self.record_length = length_local_path
					self.record_path = local_path

					this = "The shortest route found so far has a distance "
					# Stating the precision automatically rounds float values.
					that = "of: {0:.2f} ly. ".format(self.record_length)
					siht = "Continue searching for a better route ..."
					print(this + that + siht)

			# But if there are still points to be visited, ...
			else:
				# ... call yourself.
				self._find_best_route(local_path, local_travelers)






















