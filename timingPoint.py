# Modules to import
import math

# Input the offset of the first timing point. It will be used later
first = input("Input the offset of the first timing point: ")

# Import the list of time stamps.
points = []

# Function importing two time stamps and calculating BPM.
def point2(p1, p2, bpm_old):
    diff = p2 - p1
    bpm_new = 0
    snap = 0

    # If statement for 1/4s
    if diff < 100:
        bpm_new = round(15 * (1 / (diff / 1000)), 3)
        snap = 4
    
    # If statement for 1/2s
    else:
        bpm_new = round(30 * (1 / (diff / 1000)), 3)
        snap = 2

    # Comparing BPMs to decide if it's necessary and returning tuple with offset, bpm, and true/false
    if compare_BPM(bpm_old, bpm_new, snap) == 'false':
        return (p1, bpm_old, 'false')
    else:
        return (p1, bpm_new, 'true')
    
def compare_BPM(bpm1, bpm2, snap):
    len1 = 0
    len2 = 0
    diff = 0

    if snap == 4:
        len1 = round(1000 * (60 / (bpm1 * 4)))
        len2 = round(1000 * (60 / (bpm2 * 4)))
    
    if snap == 2:
        len1 = round(1000 * (60 / (bpm1 * 2)))
        len2 = round(1000 * (60 / (bpm2 * 2)))
    
    diff = len2 - len1

    # False is no need for a new timing point
    # True is yes create a new timing point
    if diff in range(-10, 11):
        return 'false'
    else:
        return 'true'

# Class that is for the timing points in the final list
class Point:
    def __init__(self):
        self.offset = 0
        self.bpm = float(0)
        self.num = 'None'

# Function using the list from midi import and creating a list with all the BPMs and offsets
def createList(lis, first):
    final = []
    i = 0
    old = 1

    while i < (len(lis) - 1):
        apps = Point()
        tup = point2(lis[i] + first, lis[i + 1] + first, old)
        if tup[2] == 'true':
            apps.offset = tup[0]
            apps.bpm = tup[1]
            apps.num = str(i)
            final.append(apps)
            i += 1

        else:
            i += 1

        old = tup[2]

    return final

# Function calculating the bpm number for the .osu file
def calc(bpm):
    num = 60000 / bpm
    return num

# Function writing to the .txt file
def writeFile(lis):
    f = open('points.txt', 'w')
    i = 0
    while i < len(lis):
        bpm = calc(lis[i].bpm)
        f.write(lis[i].offset, ',', bpm, ',4,2,1,100,1,0\n')

# Executing the actual program
writeFile(createList(points, first))
