import re
import random

weights = {"college": 0.8, "interests": 0.8, "roles": 0.8, "location": 0.8}
pastMatches = []
pastMatchedLils = []
bigs = []
lils = []

def isBig(bigName, matches):
    filtered = []
    for match in matches:
        if match[0] == bigName:
            filtered.append(match)
    return filtered

def isLil(lilName, matches):
    filtered = []
    for match in matches:
        if match[1] == lilName:
            filtered.append(match)
    return filtered

def getPastMatches():
    lines = []
    f = open("finalmatches.txt", "r")
    for x in f:
        lines.append(x)
    for ind in range(0, len(lines)):
        if ind % 2 == 0:
            sublist = lines[ind].split(", ")
            sublist[-1] = 0
            sublist[-1] = getScore(sublist[0], sublist[1])
            pastMatches.append(sublist)
            pastMatchedLils.append(sublist[1])

def getScore(person1, person2):
    g = open("data2.tsv", "r")
    for y in g:
        line = re.split("\\t", y)
        if line[1] == person1:
            big = line
    h = open("data2.tsv", "r")
    for x in h:
        line = re.split("\\t", x)
        if line[1] == person2:
            lil = line
    score = 0
    # college
    if big[4] == lil[4]:
        score += (1 * weights["college"])
    # interests
    for interest1 in big[5].split(","):
        for interest2 in lil[5].split(","):
            if interest1 == interest2:
                score += (1 * weights["interests"])
    # roles
    for role1 in big[6].split(","):
        for role2 in lil[6].split(","):
            if role1 == role2:
                if role1 == " Graduate School" or role1 == " Research" or role1 == " Design":
                    score += (1 * 1)
                else:
                    score += (1 * weights["roles"])
    # location
    for loc1 in big[7].split(","):
        for loc2 in lil[7].split(","):
            if loc1 == loc2:
                score += (1 * weights["location"])
    return score

def createMatches():
    # will return a dictionary of each person mapped to each other person and their corresponding score
    matches = []
    upperclass = ["Senior", "Junior", "Grad Student"]
    f = open("data2.tsv", "r")
    for x in f:
        line = re.split("\\t",x)
        name = line[1]
        year = line[3]
        if year in upperclass:
            bigs.append(name)
        else:
            lils.append(name)
    for big in bigs:
        for lil in lils:
            score = getScore(big, lil)
            matches.append([big, lil, score])
    print("big len ", len(bigs))
    print("lil len ", len(lils))
    random.shuffle(matches)
    #print(matches)
    return matches

def process(lis):
    f = open("output.txt", "w")
    matchedLils = []
    ind = bigs.index("Rebecca Smith")
    temp = bigs[0]
    bigs[0] = "Rebecca Smith"
    bigs[ind] = temp
    matches = []
    for big in bigs:
        filtered = isBig(big, lis)
        scores = []
        sortedByBig = []
        for item in filtered:
            scores.append(item[2])
        scores.sort()
        scores.reverse()
        for score in scores:
            for item in filtered:
                if item[2] == score:
                    sortedByBig.append(item)
                    filtered.remove(item)
        count = 0
        for item in sortedByBig:
            if item[1] not in matchedLils and count < 2 and item not in pastMatches:
                count += 1
                matchedLils.append(item[1])
                matches.append(item)
    # get the lils that need a match because they are new
    unmatchedLils = []
    for lil in lils:
        if lil not in matchedLils:
            unmatchedLils.append(lil)
    for lil in unmatchedLils:
        if lil not in pastMatchedLils:
            filtered = isLil(lil, lis)
            scores = []
            sortedByLil = []
            for item in filtered:
                scores.append(item[2])
            scores.sort()
            scores.reverse()
            for score in scores:
                for item in filtered:
                    if item[2] == score:
                        sortedByLil.append(item)
                        filtered.remove(item)
            decision = isBig(sortedByLil[0][0], matches)
            count = 0
            for isPast in decision:
                if isPast[1] in pastMatchedLils and count < 1:
                    count += 1
                    print("success")
                    matches.remove(isPast)
                    matchedLils.remove(isPast[1])
            matches.append(sortedByLil[0])
            matchedLils.append(sortedByLil[0][1])
            # remove a past matched lil from the big
    unmatchedLils = []
    for lil in lils:
        if lil not in matchedLils:
            unmatchedLils.append(lil)
    for lil in unmatchedLils:
        if lil not in pastMatchedLils:
            print("error ", lil)
    for item in matches:
        s = str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + "\n"
        f.write(s)
    f.close()
    print("end lil len ", len(matchedLils))
    print("unmatched lils ", unmatchedLils)
    print("past matched lils ", pastMatchedLils)

def process1():
    lines = []
    f = open("output.txt", "r")
    w = open("output1.txt", "w")
    for x in f:
        lines.append(x)
    lines.sort()
    for line in lines:
        w.write(line)
    w.close()

def process2():
    f = open("output1.txt", "r")
    w = open("output2.txt", "w")
    for x in f:
        line = x.split(", ")
        w.write(x)
        w.write(getThingsInCommon(line[0], line[1]))
    w.close()

def getThingsInCommon(person1, person2):
    g = open("data2.tsv", "r")
    for y in g:
        line = re.split("\\t", y)
        if line[1] == person1:
            big = line
    h = open("data2.tsv", "r")
    for x in h:
        line = re.split("\\t", x)
        if line[1] == person2:
            lil = line
    thingsInCommon = ""
    # college
    if big[4] == lil[4]:
        thingsInCommon += big[4] + ", "
    # interests
    for interest1 in big[5].split(","):
        for interest2 in lil[5].split(","):
            if interest1 == interest2:
                thingsInCommon += interest1 + ", "
    # roles
    for role1 in big[6].split(","):
        for role2 in lil[6].split(","):
            if role1 == role2:
                thingsInCommon += role1 + ", "
    # location
    for loc1 in big[7].split(","):
        for loc2 in lil[7].split(","):
            if loc1 == loc2:
                thingsInCommon += loc1 + ", "
    thingsInCommon += "\n"
    return thingsInCommon

getPastMatches()
print(pastMatches)
matches = createMatches()
process(matches)
process1()
process2()
#print(pastMatches)

#print(getThingsInCommon("Rebecca Smith", "Rashi Bose"))
#print(getThingsInCommon("Jamie Tan", "Scarlett Spindler"))

# def sortMatches1(lis):
#     scores = []
#     sorted = []
#     for item in lis:
#         scores.append(item[2])
#     scores.sort()
#     scores.reverse()
#     for score in scores:
#         for item in lis:
#             if item[2] == score:
#                 sorted.append(item)
#                 lis.remove(item)
#     #print("length score ", len(scores))
#     #print("length lis ", len(lis))
#     #print("length sorted ", len(sorted))
#     #print(sorted)
#     return sorted
#
# def processOld(lis):
#     matchedBigs = {}
#     matchedLils = []
#     mutating = list.copy(lis)
#     f = open("output.txt", "w")
#     # first pass
#     for item in mutating:
#         if item[0] not in matchedBigs and item[1] not in matchedLils:
#             s = str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + "\n"
#             f.write(s)
#             mutating.remove(item)
#             matchedBigs[item[0]] = 1
#             matchedLils.append(item[1])
#         elif item[1] in matchedLils:
#             mutating.remove(item)
#     # second pass
#     for item in mutating:
#         if item[1] in matchedLils:
#             mutating.remove(item)
#         elif matchedBigs[item[0]] < 2:
#             s = str(item[0]) + ", " + str(item[1]) + ", " + str(item[2]) + "\n"
#             f.write(s)
#             mutating.remove(item)
#             matchedBigs[item[0]] += 1
#             matchedLils.append(item[1])
#     f.close()
#     print("end big len ", len(matchedBigs.keys()))
#     print("end lil len ", len(matchedLils))
#     return 0