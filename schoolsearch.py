def main():
    try:
        list = open("list.txt", "r")
        teachers = open("teachers.txt", "r")
    except(FileNotFoundError):
        print("One or more files missing: 'list.txt', 'teachers.txt'!")
        quit()
    tableset = formatList(list)
    teacherset = formatTeachers(teachers)
    list.close()
    teachers.close()
    initiatePrompt(tableset, teacherset)


# list.txt, ex: (COOKUS, XUAN, 3, 107, 52, 3.07)
STUDENT_LAST = 0  # STRING
STUDENT_FIRST = 1  # STRING
GRADE = 2  # INT
STUDENT_CLASSROOM = 3  # INT
BUS = 4  # INT
GPA = 5  # FLOAT

# teachers.txt, ex: (COOL, REUBEN, 101)
TEACHER_LAST = 0 # STRING
TEACHER_FIRST = 1 # STRING
TEACHER_CLASSROOM = 2 # INT


def formatList(file):
    tableset = set([])
    for line in file.readlines():
        splitline = tuple([item.strip() for item in line.split(",")])
        if len(splitline) != 6:
            print("Incorrect file format for 'list.txt'!")
            quit()
        tableset.add(splitline)
    return tableset


def formatTeachers(file):
    teacherset = set([])
    for line in file.readlines():
        splitline = tuple([item.strip() for item in line.split(",")])
        if len(splitline) != 3:
            print("Incorrect file format for 'teachers.txt'!")
            quit()
        teacherset.add(splitline)
    return teacherset


def parseInput(request, tableset, teacherset):
    pair = tuple([item.strip() for item in request.split(":")])
    if len(pair) > 1:
        if pair[0] == "Student" or pair[0] == "S":
            studentHelper([item.strip() for item in pair[1].split(" ")], tableset, teacherset)
        if pair[0] == "Teacher" or pair[0] == "T":
            teacher(tableset, teacherset, pair[1])
        if pair[0] == "Bus" or pair[0] == "B":
            bus(tableset, teacherset, int(pair[1]))
        if pair[0] == "Grade" or pair[0] == "G":
            gradeHelper([item.strip() for item in pair[1].split(" ")], tableset, teacherset)
        if pair[0] == "Average" or pair[0] == "A":
            average(tableset, teacherset, int(pair[1]))


def getTeacher(tableset, teacherset, student_last_name):
    for tup in tableset:
        if tup[STUDENT_LAST].upper() == student_last_name.upper():
            for teach in teacherset:
                if teach[TEACHER_CLASSROOM] == tup[STUDENT_CLASSROOM]:
                    return teach
            break
    return ()


def getStudents(tableset, teacherset, teacher_last_name):
    studentset = set([])
    for teacher in teacherset:
        if teacher[TEACHER_LAST].upper() == teacher_last_name.upper():
            classroom = teacher[TEACHER_CLASSROOM]
            for tup in tableset:
                if tup[STUDENT_CLASSROOM] == classroom:
                    studentset.add(tup)
    return studentset


def studentHelper(tup, tableset, teacherset):
    if len(tup) == 1:
        student(tableset, teacherset, tup[0])
    elif len(tup) == 2:
        student_bus(tableset, teacherset, tup[0])


def gradeHelper(tup, tableset, teacherset):
    if len(tup) == 2:
        if tup[1] == "H" or tup[1] == "High":
            grade_high(tableset, teacherset, int(tup[0]))
        elif tup[1] == "L" or tup[1] == "Low":
            grade_low(tableset, teacherset, int(tup[0]))
        elif tup[1] == "T" or tup[1] == "Teachers":
            grade_teachers(tableset, teacherset, int(tup[0]))
    else:
        grade(tableset, teacherset, tup[0])


def initiatePrompt(tableset, teacherset):
    req = prompt()
    while (req != "I" and req != "Info" and
           req != "Q" and req != "Quit" and
           req[:3] != "A: " and req[:9] != "Average: " and
           req[:3] != "G: " and req[:7] != "Grade: " and
           req[:3] != "B: " and req[:5] != "Bus: " and
           req[:3] != "T: " and req[:9] != "Teacher: " and
           req[:3] != "S: " and req[:9] != "Student: " and
           req[:3] != "C: " and req[:7] != "Class: "):
        req = prompt()
    if req == "Q" or req == "Quit":
        quit()
    elif req == "I" or req == "Info":
        info(tableset, teacherset)
    elif req == "E" or req == "Enrollment":
        enrollment(tableset, teacherset)
    parseInput(req, tableset, teacherset)


def student(tableset, teacherset, last_name):
    for tup in tableset:
        if tup[STUDENT_LAST].upper() == last_name.upper():
            teacher = getTeacher(tableset, teacherset, last_name)
            print(tup[STUDENT_LAST],
                  tup[STUDENT_FIRST],
                  tup[GRADE],
                  tup[STUDENT_CLASSROOM],
                  teacher[TEACHER_LAST],
                  teacher[TEACHER_FIRST]
                  )
    initiatePrompt(tableset, teacherset)


def student_bus(tableset, teacherset, last_name):
    for tup in tableset:
        if tup[STUDENT_LAST].upper() == last_name.upper():
            print(tup[STUDENT_LAST],
                  tup[STUDENT_FIRST],
                  tup[BUS])
    initiatePrompt(tableset, teacherset)


def teacher(tableset, teacherset, last_name):
    for teacher in teacherset:
        if teacher[TEACHER_LAST].upper() == last_name.upper():
            for student in getStudents(tableset, teacherset, last_name):
                print(student[STUDENT_LAST],
                      student[STUDENT_FIRST])
            break
    initiatePrompt(tableset, teacherset)


def grade(tableset, teacherset, grade):
    for tup in tableset:
        if tup[GRADE] == grade:
            print(tup[STUDENT_LAST],
                  tup[STUDENT_FIRST])
    initiatePrompt(tableset, teacherset)


def bus(tableset, teacherset, bus_route):
    for tup in tableset:
        if int(tup[BUS]) == bus_route:
            print(tup[STUDENT_LAST],
                  tup[STUDENT_FIRST],
                  tup[GRADE],
                  tup[STUDENT_CLASSROOM])
    initiatePrompt(tableset, teacherset)


def grade_high(tableset, teacherset, grade):
    highest_gpa = 0.0
    for tup in tableset:
        if int(tup[GRADE]) == grade:
            if float(tup[GPA]) > highest_gpa:
                highest_gpa = float(tup[GPA])
    for tup in tableset:
        if int(tup[GRADE]) == grade and float(tup[GPA]) == highest_gpa:
            teach = getTeacher(tableset, teacherset, tup[STUDENT_LAST])
            print(tup[STUDENT_LAST],
                  tup[STUDENT_FIRST],
                  tup[GPA],
                  teach[TEACHER_LAST],
                  teach[TEACHER_FIRST],
                  tup[BUS])
    initiatePrompt(tableset, teacherset)


def grade_low(tableset, teacherset, grade):
    lowest_gpa = 10.0
    for tup in tableset:
        if int(tup[GRADE]) == grade:
            if float(tup[GPA]) < lowest_gpa:
                lowest_gpa = float(tup[GPA])
    for tup in tableset:
        if int(tup[GRADE]) == grade and float(tup[GPA]) == lowest_gpa:
            teach = getTeacher(tableset, teacherset, tup[STUDENT_LAST])
            print(tup[STUDENT_LAST],
                  tup[STUDENT_FIRST],
                  tup[GPA],
                  teach[TEACHER_LAST],
                  teach[TEACHER_FIRST],
                  tup[BUS])
    initiatePrompt(tableset, teacherset)

def grade_teachers(tableset, teacherset, grade):
    print("Not written yet")
    initiatePrompt(tableset, teacherset)


def average(tableset, teacherset, grade):
    total = 0.0
    num = 0
    for tup in tableset:
        if int(tup[GRADE]) == grade:
            total += float(tup[GPA])
            num += 1
    if num != 0:
        print(grade, total / num)
    initiatePrompt(tableset, teacherset)


def info(tableset, teacherset):
    for i in range(7):
        total = 0
        for tup in tableset:
            if int(tup[GRADE]) == i:
                total += 1
        print(str(i) + ":", str(total))
    initiatePrompt(tableset, teacherset)

def enrollment(tableset, teacherset):
    print("Not written yet")
    initiatePrompt(tableset, teacherset)

def prompt():
    print('''Commands:
        S[tudent]: <lastname> [B[us]]
        T[eacher]: <lastname>
        B[us]: <number>
        G[rade]: <number> [H[igh] | L[ow] | T[eachers]]
        A[verage]: <number>
        C[lass]: <number> [T[eachers] | S[tudents]]
        E[nrollment]
        I[nfo]
        Q[uit]''')
    request = input("Request: ")
    return request


if __name__ == '__main__':
    main()
