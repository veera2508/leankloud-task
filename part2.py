import sys
import csv


filename = sys.argv[1]
frow = True
title = []
data = []
with open(filename, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if frow:
            title = row
            frow = False
        else:
            modrow = [row[0]]
            tot = 0
            for i in range(1, len(row)):
                modrow.append(int(row[i]))
                tot += int(row[i])
            modrow.append(tot)
            data.append(modrow)

maxMath = [0, 0]
maxBio = [0, 0]
maxEng = [0, 0]
maxPhy = [0, 0]
maxChem = [0, 0]
maxHindi = [0, 0]
for i in range(len(data)):
    if data[i][1] > maxMath[0]:
        maxMath[0] = data[i][1]
        maxMath[1] = data[i][0]
    if data[i][2] > maxBio[0]:
        maxBio[0] = data[i][2]
        maxBio[1] = data[i][0]
    if data[i][3] > maxEng[0]:
        maxEng[0] = data[i][3]
        maxEng[1] = data[i][0]
    if data[i][4] > maxPhy[0]:
        maxPhy[0] = data[i][4]
        maxPhy[1] = data[i][0]
    if data[i][5] > maxChem[0]:
        maxChem[0] = data[i][5]
        maxChem[1] = data[i][0]
    if data[i][6] > maxHindi[0]:
        maxHindi[0] = data[i][6]
        maxHindi[1] = data[i][0]

print("Topper in Maths is {}".format(maxMath[1]))
print("Topper in Biology is {}".format(maxBio[1]))
print("Topper in English is {}".format(maxEng[1]))
print("Topper in Physics is {}".format(maxPhy[1]))
print("Topper in Chemistry is {}".format(maxChem[1]))
print("Topper in Hindi is {}".format(maxHindi[1]))

first = [0, 0]
second = [0, 0]
third = [0, 0]

for i in range(len(data)):
    if data[i][7] > third[0]:
        if data[i][7] > second[0]:
            if data[i][7]>first[0]:
                second[0] = first[0]
                second[1] = first[1]
                first[0] = data[i][7]
                first[1] = data[i][0]
            else:
                third[0] = second[0]
                third[1] = second[1]
                second[0] = data[i][7]
                second[1] = data[i][0]
        else:
            third[0] = data[i][7]
            third[1] = data[i][0]

print("\nBest students in the class are {}, {}, {} ".format(first[1], second[1], third[1]))
