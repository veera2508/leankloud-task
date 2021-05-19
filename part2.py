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
print("Topper in each subject:")
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

print("Maths topper is {} with marks {}".format(maxMath[1], maxMath[0]))
print("Biology topper is {} with marks {}".format(maxBio[1], maxBio[0]))
print("English topper is {} with marks {}".format(maxEng[1], maxEng[0]))
print("Physics topper is {} with marks {}".format(maxPhy[1], maxPhy[0]))
print("Chemistry topper is {} with marks {}".format(maxChem[1], maxChem[0]))
print("Hindi topper is {} with marks {}".format(maxHindi[1], maxHindi[0]))

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

print("\nThe top 3 students in class based on all subjects: ")
print("Rank 1: {} with total {}".format(first[1], first[0]))
print("Rank 2: {} with total {}".format(second[1], second[0]))
print("Rank 3: {} with total {}".format(third[1], third[0]))