# Rover data
This has data from a rover moving 1m every ten minutes.   It is carrying 6 bluetooth advertisers.
There are multiple observers along the path of the rover spaced every twoo meters.

The observers are actually dongles that emit and record bluetooth packets
Here is the layout of dongle

F-2mgap-C-2mgap-E-2mgap-B&A-2mgap-D
[https://docs.google.com/presentation/d/e/2PACX-1vQmKY7YgwkGwYskTLtf_obp6kV4nrsdHd-EI-dQvxE9vlsJUOVtINvgRnCSYnO22aXK_uj2QmCO9Bwg/pub?start=false&loop=false&delayms=3000] diagrams

The rover starts at F and goes to D then back to F.

# File format
*  First two lines are comments
*  First comment line has two numbers, the first number is the time on the dongle in milliseconds.  This corresponds to the 2nd number which is the unix epoch time 
*  Second comment line, labels the columns

## jupyter notebook

* [first_look.ipynb](http://nbviewer.ipython.org/urls/raw.githubusercontent.com/saewoonam/ble_dongles/master/data/saewoo/rover/first_look.ipynb), my attempt to link the notebook
