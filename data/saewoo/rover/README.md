# Rover data
This has data from a rover moving 1m every ten minutes.   It is carrying 6 bluetooth advertisers.
There are multiple observers along the path of the rover spaced every twoo meters.

The observers are actually dongles that emit and record bluetooth packets
Here is the layout of dongle

F-2mgap-C-2mgap-E-2mgap-B&A-2mgap-D

The rover starts at F and goes to D then back to F.

# File format
*  First two lines are comments
*  First comment line has two numbers, the first number is the time on the dongle in milliseconds.  This corresponds to the 2nd number which is the unix epoch time 
*  Second comment line, labels the columns
