# visitor_missions_optimizer
You have a bunch of visitor missions in Elite: Dangerous and want to finish them asap? This program helps you to find an optimal order of destinations.

## Problem:
You carry tourists around in Elite:Dangerous and all of them want to different locations? At the same time some of them want to the same location as others but not before they've been somewhere else? It annoys you that the destinations of a tourist have to be visited in the correct order or otherwise they don't count? You'd like to fly the shortest route possible but with the given restriction and many passengers this takes too much time to figure out?

## Solution:
This program will find for you either the shortest or a good enough route for a given number of visitor destinations.

## What you'll get:
This python 3 program gets the coordinates of the destination systems from EDSM.net. It than automatically figures out which route is the shortest, under the given restriction that the destinations of each traveler have to be visited in the order as stated by the tourist. See below for some caveats.

# Usage
Preparations:
- State your origin-system (start and end for all tourists) in the "000_missions.txt"-file. Directly in the line that starts with "I'm at".  
- For each tourist state the destination-systems in the same file. The order needs to be as stated by the tourist in the in-game mission description!
- Use tabs to separate system names from each other.
- See said file for more hints.

Once this is done …
```
python3 visitor_mission_optimizer.py -h
usage: visitor_mission_optimizer.py [-h] [--maximum-time seconds]
                                    [--infile INFILE]

optional arguments:
  -h, --help            show this help message and exit
  --maximum-time seconds, -mt seconds
                        The maximum time the whole path finding process is
                        allowed to take. Default is 123 seconds.
  --infile INFILE, -f INFILE
                        Complete path to the file with the mission data (incl.
                        filename AND file-extension!). Default is the current
                        directory with "000_missions.txt" as filename.
```

## Example
Basic usage if the default parameters are OK.

    python3 visitor_mission_optimizer.py

Basic usage in which more time is allowed to find a good path and the file with the mission description was re-named to "My_missions.txt" and put into a different directory.

    python3 trade_mission_optimizer.py -mt 230 -f "/different/path/to/My_missions.txt"

# ATTENTION:
- Since the process time to find the exact solution grows factorial I've decided to do this just for the case that 12 or less different destinations need to be visited. In that case the whole process time is approx. one minute.
- For more destinations a good enough solution will be found by randomizing the order stations to be visited first (under the given restrictions) and the maximum allowed time is used to find an acceptable solution. See comments in the source-code for details.
- It is UNlikely that the latter will find the shortest path, but testing has shown that the solution found is good enough for the purpose of this program and usually not very much longer than the shortest path. At the same time, processing time is kept acceptable.
- The standard maximum allowed time is 123 seconds and was determined empirically to be a good trade-off between finding a good enough solution and not waiting too long for it. However, it can be changed.
