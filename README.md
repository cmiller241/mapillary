# mapillary
Because Mapillary only allows you to pull traffic signs in a given latitude/longitude window with a limit of 2000 signs, and because Mapillary doesn't include pagination as of July 2024, we created a program to set up our window into quadrants and review each quadrant for signs. If a single quadrant has more than 2000 signs, then it breaks up that quadrant into quadrants, and so on and so forth recursively until there are less than 2000 signs. Then it takes the output and plops it into a file. 