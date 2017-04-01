import map
import math

if __name__ == "__main__":
    # Maximum wanted size
    minX = 0
    maxX = 10
    minY = 0
    maxY = 10

    # Get an instnace of the class
    my_map = map.CreateMap()

    # Generate a map for the size
    the_map = my_map.CreateMap(minX, maxX, minY, maxY)

    # Get compressed ASCII map
    output = my_map.compressedmap()

    # Dump the output to a file and write it to the screen
    print("start")
    lineTotals = ""
    f = open('Map.txt', 'w')
    for line in output:
        f.write(line + '\n')
        print(line)
        lineTotals += str(len(line)) + ","

    f.close()

    # Turn on the IDs in the middles of the tiles, good for debugging
    my_map.show_tile_id = True
    output = my_map.compressedmap()

    # Print the larger map to the screen and append to the file
    print("start again")
    lineTotals = ""
    f = open('Map.txt', 'a')
    for line in output:
        f.write(line + '\n')
        print(line)
        lineTotals += str(len(line)) + ","

    f.close()


    # Debug stuff, lengths of lines
    print(lineTotals)
    print("End")
    #-----------------------------------------------
    output = []
    entryRow = 0

    # Make a comma seperated list of the map, using Hex to make everything one char
    print("Generating output")

    for y in range(minY, maxY+1):
        output.append("%i," % math.fabs(y))
        for x in range(minX, maxX+1):
            if (x, y) in my_map:
                output[entryRow] += "," + "%x" % map[(x, y)]
            else:
                output[entryRow] += ", "
        entryRow += 1

    topLine = ","
    for x in range(minX, maxX+1):
        topLine += ",%i" % math.fabs(x)

    print("start")
    print(topLine)
    for line in output:
        print(line)
    print("End")
