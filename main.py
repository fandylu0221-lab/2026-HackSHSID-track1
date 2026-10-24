
def distance(a, b):
    f1 = int(a[0])
    r1 = int(a[1:])
    f2 = int(b[0])
    r2 = int(b[1:])

    if f1 == f2:
        return abs(r1 - r2)

    best = 999

    for s1 in [1, 20]:
        for s2 in [1, 20]:
            d = abs(r1 - s1) + abs(f1 - f2) * 20 + abs(r2 - s2)

            if d < best:
                best = d

    return best


course = []
oldroom = []
rooms = []

for i in range(7):
    course.append(input("Course name: "))
    oldroom.append(input("Current classroom: "))

for i in range(7):
    rooms.append(input("Available classroom: "))

start = input("Starting classroom: ")

newcourse = []
newroom = []
total = 0
current = start

for i in range(7):
    best = 999
    ci = 0
    ri = 0

    for j in range(len(course)):
        for k in range(len(rooms)):
            d = distance(current, rooms[k])

            if d < best:
                best = d
                ci = j
                ri = k
            elif d == best:
                if distance(oldroom[j], rooms[k]) < distance(oldroom[ci], rooms[ri]):
                    ci = j
                    ri = k

    newcourse.append(course[ci])
    newroom.append(rooms[ri])

    total = total + distance(current, rooms[ri])
    current = rooms[ri]

    course.pop(ci)
    oldroom.pop(ci)
    rooms.pop(ri)

print("\nOptimized timetable")

for i in range(7):
    if i == 0:
        print("Morning")
    if i == 4:
        print("Afternoon")

    print("Period", i + 1, newcourse[i], newroom[i])

print("Total walking score:", total)