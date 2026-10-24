
def distance(a, b):
    f1 = int(a[0])
    r1 = int(a[1:])
    f2 = int(b[0])
    r2 = int(b[1:])

    if f1 == f2:
        return abs(r1 - r2)

    d1 = abs(r1 - 1) + abs(r2 - 1)
    d2 = abs(r1 - 20) + abs(r2 - 20)

    return min(d1, d2) + abs(f1 - f2) * 20


aliases = {
    "math": "Math", "数学": "Math",
    "english": "English", "英文": "English", "英语": "English",
    "physics": "Physics", "物理": "Physics",
    "chemistry": "Chemistry", "化学": "Chemistry",
    "chinese": "Chinese", "语文": "Chinese", "中文": "Chinese"
}

levels = {
    "Math": {
        "s": "S",
        "s+": "S+",
        "ap calculus ab": "AP Calculus AB",
        "ap calculus bc": "AP Calculus BC"
    },
    "English": {
        "s": "S",
        "s+": "S+",
        "h": "H",
        "h+": "H+"
    },
    "Physics": {
        "s": "S",
        "h": "H"
    },
    "Chemistry": {
        "s": "S",
        "s+": "S+",
        "h": "H"
    },
    "Chinese": {
        "ap chinese": "AP Chinese",
        "non-native": "Non-native",
        "non native": "Non-native"
    }
}


def read_course(text):
    if ":" not in text:
        return None

    subject, level = text.split(":", 1)
    subject = subject.strip()
    level = level.strip()

    if subject == "" or level == "":
        return None

    subject = aliases.get(subject.lower(), subject)

    if subject in levels:
        key = level.lower()

        if key not in levels[subject]:
            return None

        level = levels[subject][key]

    return (subject, level)


rooms = []

for f in [1, 2, 3]:
    for r in range(1, 21):
        rooms.append(str(f * 100 + r))


students = []
courses = []

print("Enter each student's name and 7 courses.")
print("Format: Math:S, English:H, Chinese:AP Chinese")
print("Use commas between courses.")
print("Enter yes or no when asked if there is another student.")

while True:
    name = input("\nStudent name: ").strip()

    while name == "":
        name = input("Please enter a student name: ").strip()

    while True:
        line = input("Enter 7 courses: ")
        parts = line.split(",")

        if len(parts) != 7:
            print("Please enter exactly 7 courses.")
            continue

        temp = []
        valid = True

        for part in parts:
            c = read_course(part.strip())

            if c is None:
                valid = False
                break

            temp.append(c)

        if not valid:
            print("Invalid course or level. Please try again.")
            print("Use the format Subject:Level.")
            continue

        if len(set(temp)) != 7:
            print("The same course and level cannot appear twice.")
            continue

        break

    students.append(name)
    courses.append(temp)

    answer = input("Is there another student? (yes/no): ").strip().lower()

    while answer not in ["yes", "no", "y", "n"]:
        answer = input("Please enter yes or no: ").strip().lower()

    if answer in ["no", "n"]:
        break


groups = {}

for i in range(len(students)):
    for subject, level in courses[i]:
        key = (subject, level)

        if key not in groups:
            groups[key] = []

        groups[key].append(i)


sections = []
student_sections = [[] for i in range(len(students))]

for key in groups:
    members = groups[key]

    for start in range(0, len(members), 25):
        part = members[start:start + 25]

        section = {
            "subject": key[0],
            "level": key[1],
            "students": part,
            "period": -1,
            "room": ""
        }

        sections.append(section)
        sid = len(sections) - 1

        for i in part:
            student_sections[i].append(sid)


conflicts = [set() for i in range(len(sections))]

for ids in student_sections:
    for i in ids:
        for j in ids:
            if i != j:
                conflicts[i].add(j)


period_sections = [[] for i in range(7)]


def schedule(done):
    if len(done) == len(sections):
        return True

    best = -1
    best_used = -1
    best_degree = -1

    for i in range(len(sections)):
        if i not in done:
            used = set()

            for j in conflicts[i]:
                if sections[j]["period"] != -1:
                    used.add(sections[j]["period"])

            if (len(used) > best_used or
                (len(used) == best_used and
                 len(conflicts[i]) > best_degree)):
                best = i
                best_used = len(used)
                best_degree = len(conflicts[i])

    used = set()

    for j in conflicts[best]:
        if sections[j]["period"] != -1:
            used.add(sections[j]["period"])

    for p in range(7):
        if p not in used and len(period_sections[p]) < len(rooms):
            sections[best]["period"] = p
            period_sections[p].append(best)
            done.add(best)

            if schedule(done):
                return True

            done.remove(best)
            period_sections[p].remove(best)
            sections[best]["period"] = -1

    return False


print("\nGenerating timetable...")

if not schedule(set()):
    print("No valid timetable found.")
    print("Try checking the input or reducing the number of class sections.")

else:
    previous = {}

    for p in range(7):
        ids = period_sections[p]

        ids.sort(
            key=lambda i: len(sections[i]["students"]),
            reverse=True
        )

        available = rooms[:]

        for sid in ids:
            section = sections[sid]
            best_room = available[0]
            best_score = 999999

            for room in available:
                score = 0

                for i in section["students"]:
                    if i in previous:
                        score += distance(previous[i], room)

                if score < best_score:
                    best_score = score
                    best_room = room

            section["room"] = best_room
            available.remove(best_room)

        for sid in ids:
            for i in sections[sid]["students"]:
                previous[i] = sections[sid]["room"]


    print("\n" + "=" * 70)
    print("                    MASTER TIMETABLE")
    print("=" * 70)

    for p in range(7):
        if p == 0:
            print("\nMORNING - 4 PERIODS")

        if p == 4:
            print("\nAFTERNOON - 3 PERIODS")

        print("\nPeriod", p + 1)
        print("-" * 70)

        ids = sorted(
            period_sections[p],
            key=lambda i: int(sections[i]["room"])
        )

        for sid in ids:
            s = sections[sid]

            print("Room:", s["room"])
            print("Course:", s["subject"], "-", s["level"])
            print("Students:", len(s["students"]), "/ 25")

            names = [students[i] for i in s["students"]]

            print("Class list:", ", ".join(names))
            print("-" * 40)


    print("\n" + "=" * 70)
    print("                  INDIVIDUAL TIMETABLES")
    print("=" * 70)

    total = 0

    for i in range(len(students)):
        ids = sorted(
            student_sections[i],
            key=lambda sid: sections[sid]["period"]
        )

        print("\nStudent:", students[i])
        print("-" * 70)
        print("{:<10}{:<18}{:<22}{}".format(
            "Period", "Subject", "Level", "Room"
        ))

        last_room = ""
        person_total = 0

        for sid in ids:
            s = sections[sid]
            p = s["period"]

            if p == 0:
                print("MORNING")

            if p == 4:
                print("AFTERNOON")

            print("{:<10}{:<18}{:<22}{}".format(
                p + 1,
                s["subject"],
                s["level"],
                s["room"]
            ))

            if last_room != "":
                d = distance(last_room, s["room"])
                person_total += d

            last_room = s["room"]

        total += person_total
        print("Estimated walking score:", person_total)

    print("\n" + "=" * 70)
    print("Total estimated walking score:", total)
    print("=" * 70)