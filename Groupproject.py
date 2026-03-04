import csv

class Course: #Amani
    def __init__(self, course_code, credits):
        """function representing a single course in the university catalog"""
        self.course_code = str(course_code)
        self.credits = int(credits)
        self.students = []
    def add_student(self, student):
       if student not in self.students:
            self.students.append(student)
    def get_student_count(self):
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
        if course not in self.courses:
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
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits)
        return self.courses[course_code]

    def add_student(self, student_id, name):
        if len(student_id) != 8:
            raise ValueError("Id's are 8 character length")
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]

    def get_student(self, student_id):
        return self.students.get(student_id)

    def get_course(self, course_code):
        return self.courses.get(course_code)

    def get_course_enrollment(self, course_code):
        course = self.get_course(course_code)
        if course is None:
            return 0
        return len(course.students)

    def get_students_in_course(self, course_code):
        course = self.get_course(course_code)
        if course is None:
            return []
        return list(course.students)
    
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

if __name__ == "__main__":
    uni = University()

    uni.load_courses_csv()
    uni.load_university_data_csv()

    print("Total students:", len(uni.students))
    print("Total courses:", len(uni.courses))

    for student in uni.students.values():
        print(student.name, "enrolled in:")
        for course, grade in student.courses.items():
            print("  ", course.course_code, "-", grade)

    def demo(self):
        """Demonstration of the program"""
        with open("university_data.csv", newline="") as f:
            reader = csv.reader(f)

            

