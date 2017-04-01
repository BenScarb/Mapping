#!/usr/bin/python3

import random
import math

class CreateMap():
    def __init__(self):
        # Set default map size
        self.wantedMinX = -10
        self.wantedMaxX = 10
        self.wantedMinY = -10
        self.wantedMaxY = 10

        # Can have it show the tile ID if wanted
        self.show_tile_id = False

        # Set up the Tiles and Exits
        self.tiles = dict()
        self.exits = dict()
        self.ConfigureTiles()
        self.ConfigureExits()

        # Place to store the map
        self.map = None

        # Vars for how to handle the end of a route
        self.TerminateRoute = 0
        self.MergeRoute = 1
        self.RandomSelect = 2

        # Set up how to end a route.
        self.EndRoute = self.TerminateRoute

        # Vars for looking at the exit dict.
        self.exitTiles = 0
        self.exitRemove = 1
        self.exitCoord = 2
        self.exitValue = 3

    def gettiles(self):
        return self.tiles

    def ConfigureTiles(self):
        # These tiles are two parts:
        # The first is a 4 part tuple, with a 1 for an opening, 0 for closed, in the pattern (W, S, E, N)
        # The second if another tuple, with the number of exits as a string, example ("N", "E")
        self.tiles[0] = ((0, 0, 0, 0), ())
        self.tiles[1] = ((0, 0, 0, 1), ("N"))
        self.tiles[2] = ((0, 0, 1, 0), ("E"))
        self.tiles[3] = ((0, 0, 1, 1), ("N", "E"))
        self.tiles[4] = ((0, 1, 0, 0), ("S"))
        self.tiles[5] = ((0, 1, 0, 1), ("N", "S"))
        self.tiles[6] = ((0, 1, 1, 0), ("E", "S"))
        self.tiles[7] = ((0, 1, 1, 1), ("N", "E", "S"))
        self.tiles[8] = ((1, 0, 0, 0), ("W"))
        self.tiles[9] = ((1, 0, 0, 1), ("N", "W"))
        self.tiles[10] = ((1, 0, 1, 0), ("E", "W"))
        self.tiles[11] = ((1, 0, 1, 1), ("N", "E", "W"))
        self.tiles[12] = ((1, 1, 0, 0), ("S", "W"))
        self.tiles[13] = ((1, 1, 0, 1), ("N", "S", "W"))
        self.tiles[14] = ((1, 1, 1, 0), ("E", "S", "W"))
        self.tiles[15] = ((1, 1, 1, 1), ("N", "S", "E", "W"))

    def ConfigureExits(self):
        self.exits["N"] = ((4, 5, 6, 7, 12, 13, 14, 15), "S", (0, -1), 1)
        self.exits["E"] = ((8, 9, 10, 11, 12, 13, 14, 15), "W", (1, 0), 2)
        self.exits["S"] = ((1, 3, 5, 7, 9, 11, 13, 15), "N", (0, 1), 4)
        self.exits["W"] = ((2, 3, 6, 7, 10, 11, 14, 15), "E", (-1, 0), 8)


    def CreateMap(self, lX=None, mX=None, lY=None, mY=None):
        if lX is None:
            lX = self.wantedMinX
        else:
            self.wantedMinX = lX

        if mX is None:
            mX = self.wantedMaxX
        else:
            self.wantedMaxX = mX

        if lY is None:
            lY = self.wantedMinY
        else:
            self.wantedMinY = lY

        if mY is None:
            mY = self.wantedMaxY
        else:
            self.wantedMaxY = mY

        # Default start for testing
        map = dict()
        map[(0, 0)] = 6
        pathLeft = dict()
        pathLeft[(0, 0)] = ["E", "S"]

        # Set the defaults
        minX, maxX, minY, maxY = (0, 0, 0, 0)

        # Keep going until there are no more paths to follow
        while len(pathLeft.keys()) > 0:
            # Get the X and Y coords of the first uncleared path
            x, y = list(pathLeft.keys())[0]

            # make sure we're not done with this coord
            while (x, y) in pathLeft and len(pathLeft[(x, y)]) > 0:
                # Go through all the unchecked exits
                exit = pathLeft[(x, y)][0]
                # Pick a random tile to move to
                newTile = self.exits[exit][self.exitTiles][random.randint(0, 7)]

                # Create new X, Y coords
                newX = x + self.exits[exit][self.exitCoord][0]
                newY = y + self.exits[exit][self.exitCoord][1]

                # Var to check if there is a need to make a new path entry
                addNewPath = False

                # Are the new coords out of bounds, as it were
                if newX > mX or newX < lX or newY > mY or newY < lY:
                    # Remove the exit from current x, y
                    # Replace the current x, y tile with one that doesn't have the current exit
                    map[(x, y)] = map[(x, y)] - self.exits[exit][self.exitValue]
                else:
                    # Check to see a title already exists there
                    if (newX, newY) in map:
                    # 	If there is, check config and replace randomly selected tile or adjust new X,Y tile
                        if self.EndRoute == self.TerminateRoute:
                            # Replace the current x, y tile with one that doesn't have the current exit
                            map[(x, y)] = map[(x, y)] - self.exits[exit][self.exitValue]
                        elif self.EndRoute == self.MergeRoute:
                            # Make sure destination tile gets this entry added, if needed
                            if map[(newX, newY)] & self.exits[exit][self.exitValue] == 0:
                                map[(newX, newY)] = map[(newX, newY)] + self.exits[exit][self.exitValue]
                                # Remove this way from the path if it's in there
                                pathLeft[newX, newY].remove(self.exits[exit][self.exitRemove])
                        elif self.EndRoute == self.RandomSelect:
                            pass
                    else:
                    #	If not, place new tile in "map" at new X,Y
                        map[(newX, newY)] = newTile
                        # Make sure we add the pathLeft
                        addNewPath = True

                # Do we need to add a new pathLeft
                if addNewPath:
                    # Add/Adjust pathLeft for the new tile at new X, Y.  WITHOUT the direction we just came from
                    newPath = []
                    toIgnore = self.exits[exit][self.exitRemove]
                    for item in self.tiles[newTile][1]:
                        # don't add if it's where we came from
                        if item != toIgnore:
                            newPath.append(item)

                    # If it was a one entry tile, there will be no path to follow.
                    if len(newPath) > 0:
                        # add to the paths to follow
                        pathLeft[(newX, newY)] = newPath

                    # Update the min/max coords
                    if newX < minX:
                        minX = newX
                    elif newX > maxX:
                        maxX = newX

                    if newY < minY:
                        minY = newY
                    elif newY > maxY:
                        maxY = newY

                # Remove the processed exit
                pathLeft[(x, y)].remove(exit)
                # Check to see if there are any exits left on this point
                if len(pathLeft[(x, y)]) == 0:
                    # If not, remove it from the dict
                    pathLeft.pop((x, y), None)
        # Store the map away
        self.map = map

        # Return the map
        return map

    # Merge lines, taking out spaces of one, replace with the other#
    def MergeLines(self, lineone, linetwo):
        end = len(lineone)

        if (len(linetwo) > end):
            lineone += " "*(len(linetwo) - end)
            end = len(linetwo)
        elif (len(linetwo) < end):
            linetwo += " "*(len(linetwo) - end)

        outline = ""
        for pos in range(0, end):
            if lineone[pos] == linetwo[pos]:
                outline += lineone[pos]
            elif lineone[pos] == " ":
                outline += linetwo[pos]
            else:
                outline += lineone[pos]

        return outline

    # Make an ASCII tile from tile Id
    def ACSIITile(self, tileId):
        if tileId is None or tileId == 0 or tileId > 15 or tileId < 0:
            return ("   ", "   ", "   ")

        westExit, southExit, eastExit, northExit = self.tiles[tileId][0]
        topLine = ""
        midLine = ""
        botLine = ""

        # Do the top line
        topLine += "+"
        if northExit == 1:
            topLine += " "
        else:
            topLine += "-"
        topLine += "+"

        # Do the mid line
        if westExit == 1:
            midLine += " "
        else:
            midLine += "|"
        # Add the centre item, normally a space but can be
        # the tile ID for debugging
        if self.show_tile_id:
            midLine += str("%x" % tileId)
        else:
            midLine += " "

        if eastExit == 1:
            midLine += " "
        else:
            midLine += "|"

        # Do the bottom line
        botLine += "+"
        if southExit == 1:
            botLine += " "
        else:
            botLine += "-"
        botLine += "+"

        # Send it all back
        return (topLine, midLine, botLine)

    # Using the current instance of the class, make a large map
    def largeasciimap(self):
        output = []

        offset = 0 - self.wantedMinY

        if self.map != None:
            for y in range(self.wantedMinY, self.wantedMaxY+1):
                # Add three new lines to append data to (range is y*3 to (y*3)+2)
                output.append("")
                output.append("")
                output.append("")

                # Go left to righ in the x range
                for x in range(self.wantedMinX, self.wantedMaxX+1):
                    if (x, y) not in self.map:
                        asciiTile = self.ACSIITile(0)
                    else:
                        asciiTile = self.ACSIITile(self.map[(x, y)])

                    # Set the row number up
                    rowNumb = ((y + offset) * 3)

                    # Put the ascii lines in to the output
                    for line in range(0, 3):
                        output[rowNumb+line] += asciiTile[line]

        #return the complete "picure"
        return output

    # Using the current instance of the class, make a compressed map
    def compressedmap(self):
        output = []

        rowStart = -2
        output.append("")
        for y in range(self.wantedMinY, self.wantedMaxY+1):
            # Add three new lines to append data to (range is y*3 to (y*3)+2)
            output.append("")
            output.append("")

            # Move on to the appropriate row number
            rowStart += 2
            topLine = ""

            # Go left to righ in the x range
            for x in range(self.wantedMinX, self.wantedMaxX+1):
                start = 1
                if x == self.wantedMinX:
                    start = 0

                # Get an ASCII tile
                if (x, y) not in self.map:
                    asciiTile = self.ACSIITile(0)
                else:
                    asciiTile = self.ACSIITile(self.map[(x, y)])

                # When the top line is not blank, and ends with a space,add all the tile to the line
                # Otherwise just the use the last two chars
                if len(topLine) > 0 and topLine[-1] == " ":
                    topLine = topLine[:-1] + asciiTile[0]
                else:
                    topLine += asciiTile[0][start:3]

                # Repeat for the second row
                if len(output[rowStart+1]) > 0 and output[rowStart+1][-1] == " ":
                    output[rowStart+1] = output[rowStart+1][:-1] + asciiTile[1]
                else:
                    output[rowStart+1] += asciiTile[1][start:3]

                # And repeat for the last row
                if len(output[rowStart+2]) > 0 and output[rowStart+2][-1] == " ":
                    output[rowStart+2] = output[rowStart+2][:-1] + asciiTile[2]
                else:
                    output[rowStart+2] += asciiTile[2][start:3]

            # Now that all of the Row has been done, merge the two lines
            output[rowStart] = self.MergeLines(output[rowStart], topLine)

        # Return the compressed map
        return output
