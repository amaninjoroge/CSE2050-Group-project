import csv

class Course: #Amani
    def __init__(self, course_code, credits):
        """function representing a single course in the university catalog"""
        self.course_code = str(course_code)
        self.credits = int(credits)
        self.students = []
    def add_student(self, student):
       """adds a student obkect to the course roster"""
       if student not in self.students:
            self.students.append(student)
    def get_student_count(self):
        """returns the number of students currently enrolled"""
        return len(self.students)


class Student: #Mei Mei
    """A class to respresent an student and their courses with grades"""
    
    GRADE_POINTS = { 
        'A' : 4.0, 'A-' : 3.7, 
        'B+': 3.3, 'B' : 3.0, 'B-' : 2.7, 
        'C+': 2.3, 'C' : 2.0, 'C-' : 1.7, 
        'D' : 1.0, 
        'F' : 0.0 
    }
    
    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.courses = {}

    def enroll(self, course, grade:str): 
        self.courses[course] = grade
        if self not in course.students:
            course.students.append(self)
    
    def update_grade(self, course, grade:str):
        if course in self.courses:
            self.courses[course] = grade
    
    def calculate_gpa(self):
        """Compute weighted GPA using course credits."""
        total_points = 0
        total_credits = 0

        for course, grade in self.courses.items():
            if grade in Student.GRADE_POINTS:
                points = Student.GRADE_POINTS[grade]
                total_points += points * course.credits
                total_credits += course.credits

        if total_credits == 0:
            raise ValueError

        return total_points / total_credits
    
    def get_courses(self):
        return list(self.courses.keys())
    
    def get_course_info(self): 
        table = []
    
        header = f"{'Course Code':<15}{'Credits':<10}{'Grade':<10}"
        separator = "-" * 35
    
        table.append(header)
        table.append(separator)

        for course, grade in self.courses.items():
            row = f"{course.course_code:<15}{course.credits:<10}{grade:<10}"
            table.append(row)

        return "\n".join(table)
     
class University: #Amani
    def __init__(self):
        """stores all students and courses"""
        self.students = {}
        self.courses = {}

    def add_course(self, course_code, credits):
        """adds courses and returns them as objects"""
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits)
        return self.courses[course_code]

    def add_student(self, student_id, name):
        """creates and returns student objects"""
        if len(student_id) != 8:
            raise ValueError("Id's are 8 character length")
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]

    def get_student(self, student_id):
        """returns the student object for that ID"""
        return self.students.get(student_id)

    def get_course(self, course_code):
        """returns the course object"""
        return self.courses.get(course_code)

    def get_course_enrollment(self, course_code):
        """returns the number of students enrolled in the given course"""
        course = self.get_course(course_code)
        if course is None:
            return 0
        return len(course.students)

    def get_students_in_course(self, course_code):
        """returns the number of students enrolled in the given course"""
        course = self.get_course(course_code)
        if course is None:
            return []
        return list(course.students)
    
    def students_in_course(self, course_code):
        """Gets the list of students enrolled in a course"""
        course = self.get_course(course_code)

        if not course:
            print("Course not found")
            return[]
        return [student.name for student in course.students]

    def print_student_gpa(self, student_id):
        """Prints GPA of a student"""
        student = self.get_student(student_id)
        if student:
            return student.calculate_gpa()
        return None
    
    def print_student_courses(self, student_id):
        """prints course info for a student"""
        student = self.get_student(student_id)
        if student:
            return student.get_course_info()
        return None
    
    def course_grade_stats(self, course_code):
        """returns mean median and mode of grades for a course"""
        course = self.get_course(course_code)
        if not course:
            return None

        grades = []

        for student in course.students:
            grade = student.courses.get(course)
            if grade in Student.GRADE_POINTS:
                grades.append(Student.GRADE_POINTS[grade])

        if len(grades) == 0:
            return None
        
        mean = sum(grades) / len(grades)
        grades.sort()
        n = len(grades)

        if n % 2 == 1:
            median = grades[n // 2]
        else:
            median = (grades[n//2 - 1] + grades[n//2]) / 2

        counts = {}
        for g in grades:
            counts[g] = counts.get(g, 0) + 1

        mode = max(counts, key=counts.get)
        return {"mean": mean, "median": median, "mode": mode}
    
    def university_gpa_stats(self):
        """Mean and median GPA of all students"""
        gpas = []

        for student in self.students.values():
            if len(student.courses) > 0:
                gpas.append(student.calculate_gpa())

        if len(gpas) == 0:
            return None
        
        mean = sum(gpas) / len(gpas)
        gpas.sort()
        n = len(gpas)

        if n % 2 == 1:
            median = gpas[n // 2]
        else:
            median = (gpas[n//2 - 1] + gpas[n//2]) / 2
        return {"mean": mean, "median": median}
    
    
    
    def common_students(self, course_code1, course_code2):
        """returns common students in two different courses"""
        course1 = self.get_course(course_code1)
        course2 = self.get_course(course_code2)

        if not course1 or not course2:
            return[]
        students1 = set(course1.students)
        students2 = set(course2.students)

        common = students1.intersection(students2)
        return [student.name for student in common]


    
    #Mei Mei
    """functions to open and read the csv files"""
    def load_courses_csv(self):
        with open("course_catalog.csv", mode = "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                course_code = row["course_code"]
                credits = int(row["credits"])
                self.add_course(course_code, credits)

    def load_university_data_csv(self):
        with open("university_data.csv", mode = "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                student_id = row["student_id"]
                name = row["name"]
                courses_string = row["courses"]

                student = self.add_student(student_id, name)

                if courses_string:
                    courses_pairs = courses_string.split(";")

                    for pair in courses_pairs:
                        course_code, grade = pair.split(":")

                        course = self.get_course(course_code)

                        if course:
                            student.enroll(course, grade)

if __name__ == "__main__": #Amani (demo)

    uni = University()
    uni.load_courses_csv()
    uni.load_university_data_csv()

    print("Total students:", len(uni.students))
    print("Total courses:", len(uni.courses))

    for student in uni.students.values():
        print(student.name, "enrolled in:")
        for course, grade in student.courses.items():
            print("  ", course.course_code, "-", grade)

    course_code = "CSE1010"
    students = uni.get_students_in_course(course_code)

    print("\nStudents enrolled in", course_code)
    for s in students:
        print(s.name)

    student_id = list(uni.students.keys())[0]
    student = uni.get_student(student_id)

    print("\nGPA of", student.name, ":", student.calculate_gpa())

    print("\nCourses for", student.name)
    print(student.get_course_info())

    stats = uni.course_grade_stats(course_code)

    print("\nGrade statistics for", course_code)
    print("Mean:", stats["mean"])
    print("Median:", stats["median"])
    print("Mode:", stats["mode"])

    gpa_stats = uni.university_gpa_stats()

    print("\nUniversity GPA statistics")
    print("Mean GPA:", gpa_stats["mean"])
    print("Median GPA:", gpa_stats["median"])

    course1 = "CSE1010"
    course2 = "CSE2050"

    common = uni.common_students(course1, course2)

    print("\nCommon students in", course1, "and", course2)
    for name in common:
        print(name)

            

