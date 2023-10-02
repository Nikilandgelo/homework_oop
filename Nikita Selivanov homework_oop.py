class Mentor:

    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):

    def __init__(self, name: str, surname: str):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {object_medium_grade(self.grades)}"
    
    def __gt__(self, other):
        if isinstance(other, Lecturer):
            return object_medium_grade(self.grades) > object_medium_grade(other.grades)
        else:
            return "Неккоректное сравнение"


class Student:

    def __init__(self, name: str, surname: str, gender: str):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.courses_in_progress = []
        self.finished_courses = []
        self.grades = {}

    def __str__(self):
        return (f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {object_medium_grade(self.grades)}\n"
        f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\nЗавершенные курсы: {', '.join(self.finished_courses)}")
    
    def __gt__(self, other):
        if isinstance(other, Student):
            return object_medium_grade(self.grades) > object_medium_grade(other.grades)
        else:
            return "Неккоректное сравнение"

    def rate_lecture(self, lecturer: Lecturer, course: str, grade: int):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            print("Произошла ошибка при оценивании лектора")
            return


class Reviewer(Mentor):
    
    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"
    
    def rate_homework(self, student: Student, course: str, grade: int):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print("Произошла ошибка при выставлении оценки")
            return


def object_medium_grade(dictionary: dict):
    sum_grades = 0
    for key, value in dictionary.items():
        key_medium_grade = 0
        for number in value:
            key_medium_grade += number
        sum_grades += key_medium_grade / len(value)
    sum_grades = sum_grades / len(dictionary)
    return sum_grades

def course_medium_grade(list_course_grades: list):                      # не смог придумать как интегрировать предыдущий подсчет средней оценки в рамках одного курса, поэтому...
    sum_grades = 0
    for grades_people in list_course_grades:
        medium_people_grade = 0
        for grades in grades_people:
            medium_people_grade += grades
        sum_grades += medium_people_grade / len(grades_people)
    sum_grades = sum_grades / len(list_course_grades)
    return sum_grades

def homework_medium_grade(list_students: list, course_name: str):
    all_grades_course = [student.grades.get(course_name) for student in list_students if student.grades.get(course_name) and isinstance(student, Student)]
    return course_medium_grade(all_grades_course)

def lections_medium_grade(list_lectors: list, course_name: str):
    all_grades_course = [lector.grades.get(course_name) for lector in list_lectors if lector.grades.get(course_name) and isinstance(lector, Lecturer)]
    return course_medium_grade(all_grades_course)

git_lector = Lecturer("Maxim", "Medvedev")
git_lector.courses_attached.append("Git")

python_lector = Lecturer("Alexey", "Alexeev")
python_lector.courses_attached.append("Python")

git_student = Student("Elizaveta", "Vasilieva", "Female")
git_student.courses_in_progress.append("Git")
git_student.finished_courses.append('3D моделирование в Blender')
git_student.rate_lecture(git_lector, "Git", 7)
git_student.rate_lecture(git_lector, "Git", 9)

python_student = Student("Vasiliy", "Ivanov", "Male")
python_student.courses_in_progress.append("Python")
python_student.finished_courses.append('Бизнес тренинг "Как стать миллиардером с нуля за 1 минуту"')
python_student.rate_lecture(python_lector, "Python", 10)
python_student.rate_lecture(python_lector, "Python", 9)

reviewer = Reviewer("Alena", "Petrova")
reviewer.courses_attached.extend(["Git", "Python"])
reviewer.rate_homework(git_student, "Git", 6)
reviewer.rate_homework(git_student, "Git", 7)
reviewer.rate_homework(python_student, "Python", 8)
reviewer.rate_homework(python_student, "Python", 9)

print()
print("Проверяющие:")
print(reviewer)
print()
print("Лекторы:")
print(git_lector)
print()
print(python_lector)
print()
print(git_lector > python_lector)
print(git_lector > python_student)
print()
print("Студенты:")
print(git_student)
print()
print(python_student)
print()
print(git_student < python_student)
print(git_student < git_lector)
print()
print(f'{homework_medium_grade([git_student, python_student], "Python")} средняя оценка студентов за ДЗ по указанному курсу')
print(f'{lections_medium_grade([git_lector, python_lector], "Git")} средняя оценка лекторов за лекции по указанному курсу')
print()